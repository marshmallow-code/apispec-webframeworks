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
        # iterate through the routes and look for a match to the view function 
        route = None
        # in the app objet for each path there's a dict with key=method and value=entry
        # for each operation that we're iterested in see if there's an entry
        for path in app.routes.keys():
            # get the map of method -> entry
            methods = app.routes[path]
            # loop through the methodsoperations indicated in the specification 
            for method in methods.keys():
                # see if there's a match for the operation 
                if len(operations) == 0 or method.lower() in operations:
                    # there's an entry so see if the view methods match
                    entry = methods[method]
                    if entry.view_function == view:                        
                        # store the path if this is the first match 
                        if route is None:
                             route = path
                        # if the view natches a different path something is wrong
                        elif route != path:
                            raise APISpecError(f"Duplicate route found for method {view}")
        # make sure we found one
        if route is None:
            raise APISpecError(f"No route found for method {view}")
        # success 
        return route

    def path_helper(self, operations, *, view, app, **kwargs):
        """Path helper that allows passing a chalice view function."""
        if not isinstance(app, Chalice):
            raise APISpecError(f"app must be an instance of Chalice")
        # parse through the documentation string to see what operations are defined
        operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
        # find the route for this view function
        route = self._route_for_view(app, operations, view)
        # if we didn't throw an exception then the view function handles all operations found in the docs
        return route
