import pytest
from aiohttp import web
from apispec import APISpec

from apispec_webframeworks.aiohttp import AiohttpPlugin

from .utils import get_paths


@pytest.fixture(params=("2.0", "3.0.0"))
def spec(request):
    return APISpec(
        title="Swagger Petstore",
        version="1.0.0",
        openapi_version=request.param,
        plugins=(AiohttpPlugin(),),
    )


class TestPathHelpers:
    def add_routes_to_spec(self, routes, spec):
        for route in routes:
            # Don't include HEAD mehods in OpenAPI spec
            if route.method == "HEAD":
                continue

            spec.path(
                route=route,
            )

    def test_path_from_get_method_handler(self, spec):
        async def hello(request):
            return web.Response(text="hello")

        app = web.Application()
        app.add_routes([web.get("/hello", hello)])

        # Add all aiohttp routes to the APISpec
        self.add_routes_to_spec(app.router.routes(), spec)

        paths = get_paths(spec)
        assert "/hello" in paths
        assert "get" in paths["/hello"]

    def test_path_from_get_decorator_handler(self, spec):
        routes = web.RouteTableDef()

        @routes.get("/hello")
        async def hello(request):
            return web.Response(text="hello")

        app = web.Application()
        app.router.add_routes(routes)

        # Add all aiohttp routes to the APISpec
        self.add_routes_to_spec(app.router.routes(), spec)

        paths = get_paths(spec)
        assert "/hello" in paths
        assert "get" in paths["/hello"]

    def test_path_from_post_method_handler(self, spec):
        async def hello(request):
            return web.Response(text="hello")

        app = web.Application()
        app.add_routes([web.post("/hello", hello)])

        # Add all aiohttp routes to the APISpec
        self.add_routes_to_spec(app.router.routes(), spec)

        paths = get_paths(spec)
        assert "/hello" in paths
        assert "post" in paths["/hello"]
        assert "get" not in paths["/hello"]

    def test_path_from_method_handler_with_docstring_integration(self, spec):
        async def hello(request):
            """Get a greeting endpoint.
            ---
            description: Get a greeting
            responses:
              200:
                description: A greeting to the client
            """
            return web.Response(text="hello")

        app = web.Application()
        app.add_routes([web.get("/hello", hello)])

        # Add all aiohttp routes to the APISpec
        self.add_routes_to_spec(app.router.routes(), spec)

        paths = get_paths(spec)
        assert "/hello" in paths
        assert "get" in paths["/hello"]
        expected = {
            "description": "Get a greeting",
            "responses": {"200": {"description": "A greeting to the client"}},
        }
        assert paths["/hello"]["get"] == expected
