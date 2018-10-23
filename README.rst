*********************
apispec-webframeworks
*********************


`apispec <https://github.com/marshmallow-code/apispec>`_ plugins for
integrating with various web frameworks.

These plugins used to be in ``apispec.ext`` but have since
been moved to their own package.


Included plugins:

* ``apispec_webframeworks.bottle``
* ``apispec_webframeworks.flask``
* ``apispec_webframeworks.tornado``

Example usage:

.. code-block:: python

    from flask import Flask
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from apispec_webframeworks.flask import FlaskPlugin
    from marshmallow import Schema, fields

    spec = APISpec(
       title='Gisty',
       version='1.0.0',
       info=dict(
           description='A minimal gist API'
       ),
       plugins=[
          FlaskPlugin(),
          MarshmallowPlugin(),
       ]
    )


    app = Flask(__name__)

    class GistParameter(Schema):
       gist_id = fields.Int()

    class GistSchema(Schema):
       id = fields.Int()
       content = fields.Str()

    @app.route('/gists/<gist_id>')
    def gist_detail(gist_id):
       """Gist detail view.
       ---
       get:
          parameters:
                - in: path
                schema: GistParameter
          responses:
                200:
                   schema: GistSchema
       """
       return 'details about gist {}'.format(gist_id)

    # Since add_path inspects the view and its route,
    # we need to be in a Flask request context
    with app.test_request_context():
       spec.add_path(view=gist_detail)

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/marshmallow-code/apispec_webframeworks/blob/master/LICENSE>`_ file for more details.
