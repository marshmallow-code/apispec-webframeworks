*********************
apispec-webframeworks
*********************

.. image:: https://badgen.net/pypi/v/apispec-webframeworks
    :target: https://pypi.org/project/apispec-webframeworks/
    :alt: PyPI version

.. image:: https://dev.azure.com/sloria/sloria/_apis/build/status/marshmallow-code.apispec-webframeworks?branchName=master
    :target: https://dev.azure.com/sloria/sloria/_build/latest?definitionId=9&branchName=master
    :alt: Build status

.. image:: https://badgen.net/badge/marshmallow/2,3?list=1
    :target: https://marshmallow.readthedocs.io/en/latest/upgrading.html
    :alt: marshmallow 2/3 compatible

.. image:: https://badgen.net/badge/code%20style/black/000
    :target: https://github.com/ambv/black
    :alt: code style: black

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

The plugins search the docstrings for lines that start with 3 dashes,
and assume anything after such line may be YAML for the OpenAPI spec.

.. code-block:: python

    from flask import Flask
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from apispec_webframeworks.flask import FlaskPlugin
    from marshmallow import Schema, fields

    spec = APISpec(
        title="Gisty",
        version="1.0.0",
        info=dict(description="A minimal gist API"),
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )


    app = Flask(__name__)


    class GistParameter(Schema):
        gist_id = fields.Int()


    class GistSchema(Schema):
        id = fields.Int()
        content = fields.Str()


    @app.route("/gists/<gist_id>")
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
        return "details about gist {}".format(gist_id)


    # Since `path` inspects the view and its route,
    # we need to be in a Flask request context
    with app.test_request_context():
        spec.path(view=gist_detail)

Documentation
=============

For documentation for a specific plugin, see its module docstring.

Integration with Sphinx' autodoc
================================

When using Sphinx' autodoc to generate documentation, the YAML in the
docstrings may yield errors like *"WARNING: Unexpected indentation"* and
*"WARNING: Block quote ends without a blank line; unexpected unindent"*,
or fail with *"LaTeX Error: Too deeply nested"*.

To mitigate that one can make autodoc find the YAML just like apispec's
``load_yaml_from_docstring``, and remove or format it. In Sphinx's
``conf.py`` add:

.. code-block:: python

    def handle_apispec_in_docstring(app, what, name, obj, options, lines):
        """
        Handle embedded OpenAPI YAML fragments, as optionally defined
        in a docstring after a line starting with 3 dashes.
        """
        for index, line in enumerate(lines):
            line = line.strip()
            if line.startswith("---"):
                idx = index
                break
        else:
            return

        # Discard the separator line and the (assumed) YAML
        del lines[idx:]


    def setup(app):
        app.connect("autodoc-process-docstring", handle_apispec_in_docstring)


Or, to preserve and format the YAML:

.. code-block:: python

    def handle_apispec_in_docstring(app, what, name, obj, options, lines):

        ...

        # Discard the separator line, indent the (assumed) YAML, and
        # prepend reST instructions
        del lines[idx]
        lines[idx:] = map(lambda s: "    {}".format(s), lines[idx:])
        lines[idx:idx] = textwrap.dedent(
            """
            This defines the following OpenAPI fragment:

            .. code-block:: yaml

            """
        ).splitlines()

Development
===========

* Clone and cd into this repo
* Create and activate a virtual environment
* Install this package (in editable mode) and the development
  dependencies

::

    $ pip install '.[dev]'

* Install pre-commit hooks

::

    $ pre-commit install


Running tests
-------------

To run all tests: ::

    $ pytest

To run syntax checks: ::

    $ tox -e lint

(Optional) To run tests in all supported Python versions in their own virtual environments (must have each interpreter installed): ::

    $ tox

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/marshmallow-code/apispec_webframeworks/blob/master/LICENSE>`_ file for more details.
