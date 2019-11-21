import pytest

from bottle import route

from apispec import APISpec
from apispec_webframeworks.bottle import BottlePlugin

from .utils import get_paths


@pytest.fixture(params=("2.0", "3.0.0"))
def spec(request):
    return APISpec(
        title="Swagger Petstore",
        version="1.0.0",
        openapi_version=request.param,
        plugins=(BottlePlugin(),),
    )


class TestPathHelpers:
    def test_path_from_view(self, spec):
        @route("/hello")
        def hello():
            return "hi"

        spec.path(
            view=hello, operations={"get": {"parameters": [], "responses": {"200": {}}}}
        )
        paths = get_paths(spec)
        assert "/hello" in paths
        assert "get" in paths["/hello"]
        expected = {"parameters": [], "responses": {"200": {}}}
        assert paths["/hello"]["get"] == expected

    def test_path_with_multiple_methods(self, spec):
        @route("/hello", methods=["GET", "POST"])
        def hello():
            return "hi"

        spec.path(
            view=hello,
            operations=dict(
                get={"description": "get a greeting", "responses": {"200": {}}},
                post={"description": "post a greeting", "responses": {"200": {}}},
            ),
        )
        paths = get_paths(spec)
        get_op = paths["/hello"]["get"]
        post_op = paths["/hello"]["post"]
        assert get_op["description"] == "get a greeting"
        assert post_op["description"] == "post a greeting"

    def test_integration_with_docstring_introspection(self, spec):
        @route("/hello")
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
            return "hi"

        spec.path(view=hello)
        paths = get_paths(spec)
        get_op = paths["/hello"]["get"]
        post_op = paths["/hello"]["post"]
        extension = paths["/hello"]["x-extension"]
        assert get_op["description"] == "get a greeting"
        assert post_op["description"] == "post a greeting"
        assert "foo" not in paths["/hello"]
        assert extension == "value"

    def test_path_is_translated_to_openapi_template(self, spec):
        @route("/pet/<pet_id>")
        def get_pet(pet_id):
            return f"representation of pet {pet_id}"

        spec.path(view=get_pet)
        assert "/pet/{pet_id}" in get_paths(spec)

    @pytest.mark.parametrize(
        "path", ["/pet/<pet_id:int>/<shop_id:re:[a-z]+>", "/pet/<pet_id>/<shop_id>"],
    )
    def test_path_with_params(self, spec, path):
        @route(path, methods=["GET"])
        def handler():
            pass

        spec.path(view=handler)
        assert "/pet/{pet_id}/{shop_id}" in get_paths(spec)
