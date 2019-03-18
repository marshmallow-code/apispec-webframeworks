# -*- coding: utf-8 -*-
import pytest

from flask import Flask
from flask.views import MethodView

from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin, DocumentedBlueprint

from .utils import get_paths


@pytest.fixture(params=('2.0', '3.0.0'))
def spec(request):
    return APISpec(
        title='Swagger Petstore',
        version='1.0.0',
        openapi_version=request.param,
        plugins=(FlaskPlugin(),),
    )


@pytest.yield_fixture()
def app():
    _app = Flask(__name__)
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


class TestPathHelpers:

    def test_path_from_view(self, app, spec):
        @app.route('/hello')
        def hello():
            return 'hi'

        spec.path(
            view=hello,
            operations={'get': {'parameters': [], 'responses': {'200': {}}}},
        )
        paths = get_paths(spec)
        assert '/hello' in paths
        assert 'get' in paths['/hello']
        expected = {'parameters': [], 'responses': {'200': {}}}
        assert paths['/hello']['get'] == expected

    def test_path_from_method_view(self, app, spec):
        class HelloApi(MethodView):
            """Greeting API.
            ---
            x-extension: global metadata
            """

            def get(self):
                """A greeting endpoint.
                ---
                description: get a greeting
                responses:
                    200:
                        description: said hi
                """
                return 'hi'

            def post(self):
                return 'hi'

        method_view = HelloApi.as_view('hi')
        app.add_url_rule('/hi', view_func=method_view, methods=('GET', 'POST'))
        spec.path(view=method_view)
        expected = {
            'description': 'get a greeting',
            'responses': {200: {'description': 'said hi'}},
        }
        paths = get_paths(spec)
        assert paths['/hi']['get'] == expected
        assert paths['/hi']['post'] == {}
        assert paths['/hi']['x-extension'] == 'global metadata'

    def test_path_with_multiple_methods(self, app, spec):
        @app.route('/hello', methods=['GET', 'POST'])
        def hello():
            return 'hi'

        spec.path(
            view=hello, operations=dict(
                get={'description': 'get a greeting', 'responses': {'200': {}}},
                post={'description': 'post a greeting', 'responses': {'200': {}}},
            ),
        )
        paths = get_paths(spec)
        get_op = paths['/hello']['get']
        post_op = paths['/hello']['post']
        assert get_op['description'] == 'get a greeting'
        assert post_op['description'] == 'post a greeting'

    def test_methods_from_rule(self, app, spec):
        class HelloApi(MethodView):
            """Greeting API.
            ---
            x-extension: global metadata
            """

            def get(self):
                """A greeting endpoint.
                ---
                description: get a greeting
                responses:
                    200:
                        description: said hi
                """
                return 'hi'

            def post(self):
                return 'hi'

            def delete(self):
                return 'hi'

        method_view = HelloApi.as_view('hi')
        app.add_url_rule('/hi', view_func=method_view, methods=('GET', 'POST'))
        spec.path(view=method_view)
        paths = get_paths(spec)
        assert 'get' in paths['/hi']
        assert 'post' in paths['/hi']
        assert 'delete' not in paths['/hi']

    def test_integration_with_docstring_introspection(self, app, spec):
        @app.route('/hello')
        def hello():
            """A greeting endpoint.

            ---
            x-extension: value
            get:
                description: get a greeting
                responses:
                    200:
                        description: a pet to be returned
                        schema:
                            $ref: #/definitions/Pet

            post:
                description: post a greeting
                responses:
                    200:
                        description: some data

            foo:
                description: not a valid operation
                responses:
                    200:
                        description:
                            more junk
            """
            return 'hi'

        spec.path(view=hello)
        paths = get_paths(spec)
        get_op = paths['/hello']['get']
        post_op = paths['/hello']['post']
        extension = paths['/hello']['x-extension']
        assert get_op['description'] == 'get a greeting'
        assert post_op['description'] == 'post a greeting'
        assert 'foo' not in paths['/hello']
        assert extension == 'value'

    def test_path_is_translated_to_swagger_template(self, app, spec):
        @app.route('/pet/<pet_id>')
        def get_pet(pet_id):
            return 'representation of pet {pet_id}'.format(pet_id=pet_id)

        spec.path(view=get_pet)
        assert '/pet/{pet_id}' in get_paths(spec)


class TestDocumentedBlueprint:

    def test_document_document_true(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/test', documented=True)
        def test():
            return 'Hello'

        app.register_blueprint(documented_blueprint)

        assert '/test' in get_paths(spec)

    def test_document_document_false(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/test', documented=False)
        def test():
            return 'Hello'

        app.register_blueprint(documented_blueprint)

        assert '/test' not in get_paths(spec)

    def test_docstring_introspection(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/test')
        def test():
            """A test endpoint.
            ---
            get:
                description: Test description
                responses:
                    200:
                        description: Test OK answer
            """
            return 'Test'

        app.register_blueprint(documented_blueprint)

        paths = get_paths(spec)
        assert '/test' in paths
        get_op = paths['/test']['get']
        assert get_op['description'] == 'Test description'

    def test_docstring_introspection_multiple_routes(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/test')
        def test_get():
            """A test endpoint.
            ---
            get:
                description: Get test description
                responses:
                    200:
                        description: Test OK answer
            """
            return 'Test'

        @documented_blueprint.route('/test', methods=['POST'])
        def test_post():
            """A test endpoint.
            ---
            post:
                description: Post test description
                responses:
                    200:
                        description: Test OK answer
            """
            return 'Test'

        app.register_blueprint(documented_blueprint)

        paths = get_paths(spec)
        assert '/test' in paths
        get_op = paths['/test']['get']
        post_op = paths['/test']['post']
        assert get_op['description'] == 'Get test description'
        assert post_op['description'] == 'Post test description'

    def test_docstring_introspection_multiple_http_methods(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/test', methods=['GET', 'POST'])
        def test_get():
            """A test endpoint.
            ---
            get:
                description: Get test description
                responses:
                    200:
                        description: Test OK answer
            post:
                description: Post test description
                responses:
                    200:
                        description: Test OK answer
            """
            return 'Test'

        app.register_blueprint(documented_blueprint)

        paths = get_paths(spec)
        assert '/test' in paths
        get_op = paths['/test']['get']
        post_op = paths['/test']['post']
        assert get_op['description'] == 'Get test description'
        assert post_op['description'] == 'Post test description'

    def test_docstring_introspection_add_url_rule(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        @documented_blueprint.route('/')
        def index():
            """
            Gist detail view.
            ---
            x-extension: metadata
            get:
                description: Get gist detail
                responses:
                    200:
                        schema:
                            $ref: '#/definitions/Gist'
            """
            return 'index'

        documented_blueprint.add_url_rule('/', view_func=index, methods=['POST'])

        app.register_blueprint(documented_blueprint)

        paths = get_paths(spec)
        assert '/' in paths
        get_op = paths['/']['get']
        assert get_op['description'] == 'Get gist detail'

    def test_docstring_introspection_methodview(self, app, spec):
        documented_blueprint = DocumentedBlueprint('test', __name__, spec)

        class Crud(MethodView):
            """
            Crud methodview.
            ---
            x-extension: global metadata
            """

            def get(self):
                """
                Crud get view.
                ---
                description: Crud get view.
                responses:
                    200:
                        schema:
                            $ref: '#/definitions/Crud'
                """
                return 'crud_get'

            def post(self):
                """
                Crud post view.
                ---
                description: Crud post view.
                responses:
                    200:
                        schema:
                            $ref: '#/definitions/Crud'
                """
                return 'crud_get'

        documented_blueprint.add_url_rule('/crud', view_func=Crud.as_view('crud_view'))

        app.register_blueprint(documented_blueprint)

        paths = get_paths(spec)
        assert '/crud' in paths
        get_op = paths['/crud']['get']
        post_op = paths['/crud']['post']
        assert get_op['description'] == 'Crud get view.'
        assert post_op['description'] == 'Crud post view.'
