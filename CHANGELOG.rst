..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2025 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Kurt McKee's GitHub Workflows
#############################

Unreleased changes
==================

Unreleased changes to the code are documented in
`changelog fragments <https://github.com/kurtmckee/github-workflows/tree/main/changelog.d/>`_
in the ``changelog.d/`` directory on GitHub.

..  scriv-insert-here

.. _changelog-1.7:

1.7 — 2025-11-30
================

Fixed
-----

-   ``tox``: Only pre-create target environments, if any.

    Previously, the list of target environments was unspecified,
    so tox would pre-create *all* tox environments.

.. _changelog-1.6:

1.6 — 2025-11-28
================

Changed
-------

-   ``create-pr``: Support dynamically-generated PR bodies.
-   ``tox``: Separate tox environment creation from execution.
-   Add the tox-gh plugin to group tox environment output.
-   Update check-jsonschema to v0.35.0.
-   Use uv for venv creation and check-jsonschema execution.

    On Windows hosts, this reduced check-jsonschema setup and execution
    from ~15 seconds down to ~5 seconds.
    It also reduced virtual environment creation from ~18 seconds to ~3 seconds.

Documentation
-------------

-   Expand the table of contents in the tox workflow documentation.
-   Fix some typos in the documentation.
-   Document how to control the job name in CI.

Development
-----------

-   Test the project in CI.

.. _changelog-1.5:

1.5 — 2025-10-02
================

Added
-----

-   Support skipping tox environments via two new config keys:
    ``tox-skip-environments`` and ``tox-skip-environments-regex``.

Changed
-------

-   Python 3.13 is now the default interpreter version
    when only PyPy or beta CPython versions or configured for install.
-   Python 3.13 is now used when validating the JSON configurations.

Development
-----------

-   Test type annotations using mypy.
-   Use chipshot to manage headers in the source code.
-   Migrate the flake8 configuration to ``pyproject.toml`` using
    the `flake8-toml-config <https://github.com/kurtmckee/flake8-toml-config>`_ plugin.

.. _changelog-1.4:

1.4 — 2025-01-29
================

Changed
-------

-   ``create-pr``: Open draft PRs.

.. _changelog-1.3:

1.3 — 2025-01-29
================

Fixed
-----

-   ``create-pr``: Fix a bug that prevented the PR base branch from being set correctly.

.. _changelog-1.2:

1.2 — 2025-01-28
================

Fixed
-----

-   ``create-pr``: Fix a typo that prevented the workflow from running correctly.

.. _changelog-1.1:

1.1 — 2025-01-27
================

Added
-----

-   Add a new reusable workflow: ``create-pr.yaml``.

    It is capable of running a tox label, committing all changes, and opening a PR.

Fixed
-----

-   ``tox``: Remove a duplicate write to ``.tox-config.json``.

.. _changelog-1.0:

1.0 — 2024-11-05
================

Added
-----

-   Add a ``tox-environments-from-pythons`` boolean key
    which will cause a list of tox environments to be generated
    from the list of all configured Python interpreters.

-   Add a ``tox-factors`` config option that will auto-append the factors
    to generated tox environment names.

Changed
-------

-   Use the ``tox-uv`` plugin to speed up tox environment creation.

-   Guarantee that a stable CPython interpreter is available for tox to use.

    Because tox only offers "best effort" support for PyPy,
    and might not support a given CPython alpha or beta,
    CPython 3.12 will now be set up automatically for tox to use.

    Just prior to running tox, ``actions/setup-python`` will be run again
    to ensure that only the requested Python interpreters are on the PATH.

Documentation
-------------

-   Fix a typo in the README.

.. _changelog-0.4:

0.4 — 2024-09-09
================

Fixed
-----

-   Fix 'config-is-validated' caching.

    ``actions/cache`` needs the ``path`` values to match between restore and save steps.

.. _changelog-0.3:

0.3 — 2024-09-08
================

Breaking changes
----------------

-   Flatten the configuration options.

    This aligns better with how GitHub action matrices work with ``include`` directives.

Changed
-------

-   Merge the standalone 'Validate config' job into the 'Run tests' job.

    This is likely to reduce billable CI time in paid repos.

Development
-----------

-   Add a test suite.

.. _changelog-0.2:

0.2 — 2024-05-10
================

Fixed
-----

*   Fix ``tox.pre-environments`` and ``tox.post-environments``, which were ignored.
*   Fix ``cache.hash-files`` checksum calculations,
    which relied on a command that's unavailable on macOS.

.. _changelog-0.1:

0.1 — 2024-05-09
================

Initial release
---------------

*   Validate the incoming configuration using a JSON schema.
*   Cache virtual environments and tox environments automatically.
*   Support installation of CPython and PyPy interpreters.
