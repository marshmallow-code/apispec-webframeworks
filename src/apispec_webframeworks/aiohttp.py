"""Aiohttp plugin. Includes a path helper that allows you to pass an AbstractRoute.
Takes the method from the route and docstring from the route handler.
::

    from aiohttp import web
    from apispec import APISpec
    from pprint import pprint


    async def hello(request):
        '''Get a greeting endpoint.
        ---
        description: Get a greeting
        responses:
          200:
            description: A greeting to the client
            content:
                text/plain:
                    schema:
                        $ref: '#/definitions/Greeting'
        '''
        return web.Response(text="hello")


    app = web.Application()
    app.add_routes([web.get("/hello", hello)])

    # Add all aiohttp routes to the APISpec
    for route in app.router.routes():
        # Don't include HEAD mehods in OpenAPI spec
        if route.method == "HEAD":
            continue

        spec.path(
            route=route,
        )

    pprint(spec.to_dict()["paths"])
    # {'/hello': {'get': {'description': 'Get a greeting',
    #                    'responses': {'200': {'content': {'text/plain': {'schema': {'$ref': '#/definitions/Greeting'}}},
    #                                          'description': 'A greeting to the '
    #                                                         'client'}}}}}

"""  # noqa: E501

from typing import Any, List, Optional

from aiohttp.web import AbstractRoute
from apispec import BasePlugin, yaml_utils


class AiohttpPlugin(BasePlugin):
    def path_helper(
        self,
        path: Optional[str] = None,
        operations: Optional[dict] = None,
        parameters: Optional[List[dict]] = None,
        *,
        route: Optional[AbstractRoute] = None,
        **kwargs: Any,
    ) -> Optional[str]:
        """Path helper that allows passing a aiohttp AbstractRoute"""
        assert operations is not None
        assert route is not None

        docstring = route.handler.__doc__ or ""
        operations.update(
            {route.method.lower(): yaml_utils.load_yaml_from_docstring(docstring)}
        )
        return route.resource.canonical
