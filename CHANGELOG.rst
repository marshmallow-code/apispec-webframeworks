Changelog
---------

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
