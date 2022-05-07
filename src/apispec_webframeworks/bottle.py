"""Bottle plugin. Includes a path helper that allows you to pass a view function
to `path`.
::

    from bottle import route, default_app
    app = default_app()
    @route('/gists/<gist_id>')
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

    spec.path(view=gist_detail)
    print(spec.to_dict()['paths'])
    # {'/gists/{gist_id}': {'get': {'responses': {200: {'schema': {'$ref': '#/definitions/Gist'}}}}}}
"""
import re
from typing import Any, List, Optional

from bottle import default_app, Bottle

from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError

RE_URL = re.compile(r"<([^<>:]+):?[^>]*>")


_default_app = default_app()


class BottlePlugin(BasePlugin):
    """APISpec plugin for Bottle"""

    @staticmethod
    def bottle_path_to_openapi(path: str) -> str:
        return RE_URL.sub(r"{\1}", path)

    @staticmethod
    def _route_for_view(app: Bottle, view):
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
        path: Optional[str] = None,
        operations: Optional[dict] = None,
        parameters: Optional[List[dict]] = None,
        *,
        view: Optional[Any] = None,
        **kwargs: Any,
    ) -> Optional[str]:
        """Path helper that allows passing a bottle view function."""
        assert operations
        assert view.__doc__, "expect that a function has a docstring"
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
        app = kwargs.get("app", _default_app)
        route = self._route_for_view(app, view)
        return self.bottle_path_to_openapi(route.rule)
