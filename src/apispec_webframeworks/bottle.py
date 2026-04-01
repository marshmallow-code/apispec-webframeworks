"""Bottle plugin. Includes a path helper that allows you to pass
a view function to `path`.
::

    from bottle import route, default_app

    app = default_app()


    @route("/gists/<gist_id>")
    def gist_detail(gist_id):
        '''Gist detail view.
        ---
        get:
            responses:
                200:
                    schema:
                        $ref: '#/definitions/Gist'
        '''
        return "detail for gist {}".format(gist_id)


    spec.path(view=gist_detail)
    print(spec.to_dict()["paths"])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}}}}
"""  # noqa: E501

import re
from collections.abc import Callable
from typing import Any

from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError
from bottle import Bottle, Route, default_app

RE_URL = re.compile(r"<([^<>:]+):?[^>]*>")


_default_app = default_app()


class BottlePlugin(BasePlugin):
    """APISpec plugin for Bottle"""

    @staticmethod
    def bottle_path_to_openapi(path: str) -> str:
        return RE_URL.sub(r"{\1}", path)

    @staticmethod
    def _route_for_view(app: Bottle, view: Callable[..., Any]) -> Route:
        endpoint = None
        for route in app.routes:
            if route.callback == view:
                endpoint = route
                break
        if not endpoint:
            raise APISpecError(f"Could not find endpoint for route {view}")
        return endpoint

    def path_helper(
        self,
        path: str | None = None,
        operations: dict | None = None,
        parameters: list[dict] | None = None,
        *,
        view: Any | None = None,
        **kwargs: Any,
    ) -> str | None:
        """Path helper that allows passing a bottle view function."""
        assert operations is not None
        assert view is not None

        docstring = view.__doc__ or ""
        operations.update(yaml_utils.load_operations_from_docstring(docstring))
        app = kwargs.get("app", _default_app)
        route = self._route_for_view(app, view)
        return self.bottle_path_to_openapi(route.rule)
