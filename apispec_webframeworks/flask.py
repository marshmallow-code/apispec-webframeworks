# -*- coding: utf-8 -*-
"""Flask plugin. Includes a path helper that allows you to pass a view
function to `path`. Inspects URL rules and view docstrings.

Passing a view function::

    from flask import Flask

    app = Flask(__name__)

    @app.route('/gists/<gist_id>')
    def gist_detail(gist_id):
        '''Gist detail view.
        ---
        x-extension: metadata
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        return 'detail for gist {}'.format(gist_id)

    with app.test_request_context():
        spec.path(view=gist_detail)
    print(spec.to_dict()['paths'])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}},
    #                  'x-extension': 'metadata'}}

Passing a method view function::

    from flask import Flask
    from flask.views import MethodView

    app = Flask(__name__)

    class GistApi(MethodView):
        '''Gist API.
        ---
        x-extension: metadata
        '''
        def get(self):
           '''Gist view
           ---
           responses:
               200:
                   schema:
                       $ref: '#/definitions/Gist'
           '''
           pass

        def post(self):
           pass

    method_view = GistApi.as_view('gists')
    app.add_url_rule("/gists", view_func=method_view)
    with app.test_request_context():
        spec.path(view=method_view)
    print(spec.to_dict()['paths'])
    # {'/gists': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}},
    #             'post': {},
    #             'x-extension': 'metadata'}}

Using DocumentedBlueprint:

    from flask import Flask
    from flask.views import MethodView

    app = Flask(__name__)
    documented_blueprint = DocumentedBlueprint('gistapi', __name__)

    @documented_blueprint.route('/gists/<gist_id>')
    def gist_detail(gist_id):
        '''Gist detail view.
        ---
        x-extension: metadata
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        return 'detail for gist {}'.format(gist_id)

    @documented_blueprint.route('/repos/<repo_id>', documented=False)
    def repo_detail(repo_id):
        '''This endpoint won't be documented
        ---
        x-extension: metadata
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Repo'
        '''
        return 'detail for repo {}'.format(repo_id)

    app.register_blueprint(documented_blueprint)

    print(spec.to_dict()['paths'])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}},
    #                  'x-extension': 'metadata'}}

"""
from __future__ import absolute_import
from collections import defaultdict
import re

from flask import current_app, Blueprint
from flask.views import MethodView

from apispec.compat import iteritems
from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError

# from flask-restplus
RE_URL = re.compile(r'<(?:[^:<>]+:)?([^<>]+)>')


class FlaskPlugin(BasePlugin):
    """APISpec plugin for Flask"""

    @staticmethod
    def flaskpath2openapi(path):
        """Convert a Flask URL rule to an OpenAPI-compliant path.

        :param str path: Flask path template.
        """
        return RE_URL.sub(r'{\1}', path)

    @staticmethod
    def _rule_for_view(view):
        view_funcs = current_app.view_functions
        endpoint = None
        for ept, view_func in iteritems(view_funcs):
            if view_func == view:
                endpoint = ept
        if not endpoint:
            raise APISpecError('Could not find endpoint for view {0}'.format(view))

        # WARNING: Assume 1 rule per view function for now
        rule = current_app.url_map._rules_by_endpoint[endpoint][0]
        return rule

    def path_helper(self, operations, view, **kwargs):
        """Path helper that allows passing a Flask view function."""
        rule = self._rule_for_view(view)
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
        if hasattr(view, 'view_class') and issubclass(view.view_class, MethodView):
            for method in view.methods:
                if method in rule.methods:
                    method_name = method.lower()
                    method = getattr(view.view_class, method_name)
                    operations[method_name] = yaml_utils.load_yaml_from_docstring(method.__doc__)
        return self.flaskpath2openapi(rule.rule)


class DocumentedBlueprint(Blueprint):
    """Flask Blueprint which documents every view function defined in it."""

    def __init__(self, name, import_name, spec):
        super(DocumentedBlueprint, self).__init__(name, import_name)
        self.documented_view_functions = defaultdict(list)
        self.spec = spec

    def route(self, rule, documented=True, **options):
        """If documented is set to True, the route will be added to the spec.
        :param bool documented: Whether you want this route to be added to the spec or not.
        """

        return super(DocumentedBlueprint, self).route(rule, documented=documented, **options)

    def add_url_rule(self, rule, endpoint=None, view_func=None, documented=True, **options):
        """Like :meth:`Flask.add_url_rule` but for a blueprint.  The endpoint for
        the :func:`url_for` function is prefixed with the name of the blueprint.
        """
        super(DocumentedBlueprint, self).add_url_rule(rule, endpoint=endpoint, view_func=view_func, **options)
        if documented:
            self.documented_view_functions[rule].append(view_func)

    def register(self, app, options, first_registration=False):
        """Register current blueprint in the app. Add all the view_functions to the spec."""
        super(DocumentedBlueprint, self).register(app, options, first_registration=first_registration)
        with app.app_context():
            for rule, view_functions in self.documented_view_functions.items():
                [self.spec.path(view=f) for f in view_functions]
