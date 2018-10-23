*********************
apispec-webframeworks
*********************

.. image:: https://badge.fury.io/py/apispec-webframeoworks.svg
    :target: http://badge.fury.io/py/apispec-webframeworks
    :alt: Latest version

.. image:: https://travis-ci.org/marshmallow-code/apispec-webframeworks.svg?branch=master
    :target: https://travis-ci.org/marshmallow-code/apispec-webframeworks

.. image:: https://img.shields.io/badge/marshmallow-3-blue.svg
    :target: https://marshmallow.readthedocs.io/en/latest/upgrading.html
    :alt: marshmallow 3 compatible

`apispec <https://github.com/marshmallow-code/apispec>`_ plugins for
integrating with various web frameworks.

These plugins used to be in ``apispec.ext`` but have since
been moved to their own package.


Included plugins:

* ``apispec_webframeworks.bottle``
* ``apispec_webframeworks.flask``
* ``apispec_webframeworks.tornado``

Migration from ``apispec<1.0.0``
================================

To migrate from older versions of apispec, install this package
with

.. code-block:: console

    pip install apispec-webframeworks


Change your imports, like so:

.. code-block:: python

    # apispec<1.0.0
    from apispec.ext.flask import FlaskPlugin

    # apispec>=1.0.0
    from apispec_webframeworks.flask import FlaskPlugin

Example Usage
=============

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

Documentation
=============

For documentation for a specific plugin, see its module docstring.

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/marshmallow-code/apispec_webframeworks/blob/master/LICENSE>`_ file for more details.
