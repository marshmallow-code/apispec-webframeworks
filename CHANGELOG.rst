Changelog
---------

1.2.0 (2024-09-16)
++++++++++++++++++

Features:

* TornadoPlugin: Ensure consistent ordering for HTTP path keys
  (:pr:`159`). Thanks :user:`bhperry` for the PR.

1.1.0 (2024-03-18)
++++++++++++++++++

Features:

- Add ``apispec_webframeworks.aiohttp`` plugin (:issue:`100`, :pr:`136`).
  Thanks :user:`S4mw1s3` for the PR.


1.0.0 (2024-01-17)
++++++++++++++++++

Features:

* Add and publish type information (:issue:`103`, :pr:`104`).
  Thanks :user:`kasium` for the PR.

Fixes:

* Fix a warning with setuptools.
  Thanks :user:`felixonmars` for the catch and patch.

Other:

* Support Python 3.8-3.12 and apispec>=6.0.0. Older versions are no longer supported.
* *Backwards-incompatible*: Remove ``apispec_webframeworks.__version__`` attribute.
  Use ``importlib.metadata.version("apispec-webframeworks")`` instead.

0.5.2 (2019-11-21)
++++++++++++++++++

* BottlePlugin: Fix support for typed path arguments (:issue:`16`).
  Thanks :user:`genbits` for reporting and thanks :user:`elfjes` for the fix.

0.5.1 (2019-11-18)
++++++++++++++++++

* TornadoPlugin: Allow decorators to modify method signatures (:issue:`61`).
  Thanks :user:`elfjes` for the catch and patch.

0.5.0 (2019-09-19)
++++++++++++++++++

* Fix compatibility with apispec 3.0.
* Drop support for Python 2.7 and Python 3.5. Only Python>=3.6 is supported.
* Drop support for apispec<2.

0.4.0 (2019-03-21)
++++++++++++++++++

* FlaskPlugin: Allow passing an app to ``spec.path`` (:pr:`33`).
  Thanks :user:`ramshaw888`.

0.3.0 (2019-01-31)
++++++++++++++++++

* FlaskPlugin: Don't add APPLICATION_ROOT to paths (:issue:`19`).

0.2.0 (2018-11-06)
++++++++++++++++++

* Fix compatibility with apispec 1.0.0b5. Older versions are not supported.

0.1.0 (2018-10-28)
++++++++++++++++++

* Test against Python 3.7.
* Rework dev environment for consistency with apispec and marshmallow.
  This also makes it easier for apispec to run tests against this
  project's test suite

0.0.2 (2018-10-23)
++++++++++++++++++

* Include tests in the package so that they can be
  run with the apispec test suite.

0.0.1 (2018-10-22)
++++++++++++++++++

* Initial release to PyPI.
