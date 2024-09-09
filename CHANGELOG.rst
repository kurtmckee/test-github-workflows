..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Kurt McKee's GitHub Workflows
#############################

Unreleased changes
==================

Unreleased changes to the code are documented in
`changelog fragments <https://github.com/kurtmckee/github-workflows/tree/main/changelog.d/>`_
in the ``changelog.d/`` directory on GitHub.

..  scriv-insert-here

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
