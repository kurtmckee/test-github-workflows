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
