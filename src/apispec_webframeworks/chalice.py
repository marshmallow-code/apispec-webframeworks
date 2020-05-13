"""Chalice plugin. Includes a path helper that allows you to pass a view function
to `path`.
::

    from chalice import Chalice
    app = Chalice(__name__)

    @app.route('/gists/{gist_id}')
    def gist_detail(gist_id):
        '''Gist detail view.
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        return 'detail for gist {}'.format(gist_id)

    spec.path(view=gist_detail, app=app)
    print(spec.to_dict()['paths'])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}}}}
"""

from chalice import Chalice

from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError


class ChalicePlugin(BasePlugin):
    """APISpec plugin for Chalice"""

    @staticmethod
    def _route_for_view(app, operations, view):
        # iterate through the routes and create a list of operations + routes for this view function
        routes = {}
        # iterate through all route entries
        for path in app.routes.keys():
            methods = app.routes[path]
            for method in methods.keys():
                entry = methods[method]
                if entry.view_function == view:
                    routes[method] = path
        # get the route
        route = list(routes.values())[0]
        # make sure all of the methods point to the same route for sanity checking
        if list(routes.values()).count(route) != len(routes):
            raise APISpecError(f"Method mismatch for route {view}")
        return route

    def path_helper(self, operations, *, view, app, **kwargs):
        """Path helper that allows passing a chalice view function."""
        # parse through the documentation string to see what operations are defined
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
        # find the route for this view function
        route = self._route_for_view(app, operations, view)
        # if we didn't throw an exception then the view function handles all operations found in the docs
        return route
