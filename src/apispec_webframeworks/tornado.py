"""Tornado plugin. Includes a path helper that allows you to pass an urlspec (path-handler pair)
object to `path`.
::

    from pprint import pprint

    from tornado.web import RequestHandler

    class HelloHandler(RequestHandler):
        def get(self):
            '''Get a greeting endpoint.
            ---
            description: Get a greeting
            responses:
                200:
                    description: A greeting to the client
                    schema:
                        $ref: '#/definitions/Greeting'
            '''
            self.write("hello")

    urlspec = (r'/hello', HelloHandler)
    spec.path(urlspec=urlspec)
    pprint(spec.to_dict()['paths'])
    # {'/hello': {'get': {'description': 'Get a greeting',
    #                     'responses': {200: {'description': 'A greeting to the '
    #                                                     'client',
    #                                         'schema': {'$ref': '#/definitions/Greeting'}}}}}}

"""
import inspect
from tornado.web import URLSpec

from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError


class TornadoPlugin(BasePlugin):
    """APISpec plugin for Tornado"""

    @staticmethod
    def _operations_from_methods(handler_class):
        """Generator of operations described in handler's http methods

        :param handler_class:
        :type handler_class: RequestHandler descendant
        """
        for httpmethod in yaml_utils.PATH_KEYS:
            method = getattr(handler_class, httpmethod)
            operation_data = yaml_utils.load_yaml_from_docstring(method.__doc__)
            if operation_data:
                operation = {httpmethod: operation_data}
                yield operation

    @staticmethod
    def tornadopath2openapi(urlspec, method):
        """Convert Tornado URLSpec to OpenAPI-compliant path.

        :param urlspec:
        :type urlspec: URLSpec
        :param method: Handler http method
        :type method: function
        """
        try:
            regex = urlspec.matcher.regex
            path_tpl = urlspec.matcher._path
        except AttributeError:  # tornado<4.5
            regex = urlspec.regex
            path_tpl = urlspec._path
        if regex.groups:
            if regex.groupindex:
                # urlspec path uses named groups
                sorted_pairs = sorted(
                    ((k, v) for k, v in regex.groupindex.items()), key=lambda kv: kv[1]
                )
                args = [pair[0] for pair in sorted_pairs]
            else:
                args = list(inspect.signature(method).parameters.keys())[1:]

            params = tuple(f"{{{arg}}}" for arg in args)
            path = path_tpl % params
        else:
            path = path_tpl
        if path.count("/") > 1:
            path = path.rstrip("/?*")
        return path

    @staticmethod
    def _extensions_from_handler(handler_class):
        """Returns extensions dict from handler docstring

        :param handler_class:
        :type handler_class: RequestHandler descendant
        """
        return yaml_utils.load_yaml_from_docstring(handler_class.__doc__)

    def path_helper(self, operations, *, urlspec, **kwargs):
        """Path helper that allows passing a Tornado URLSpec or tuple."""
        if not isinstance(urlspec, URLSpec):
            urlspec = URLSpec(*urlspec)
        for operation in self._operations_from_methods(urlspec.handler_class):
            operations.update(operation)
        if not operations:
            raise APISpecError(f"Could not find endpoint for urlspec {urlspec}")
        params_method = getattr(urlspec.handler_class, list(operations.keys())[0])
        operations.update(self._extensions_from_handler(urlspec.handler_class))
        return self.tornadopath2openapi(urlspec, params_method)
