..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Kurt McKee's GitHub Workflows
#############################

*Reusable workflows that reduce maintenance effort.*

---------------------------------------------------------------------------

I use tox to manage testing in my Python projects,
and I use GitHub workflows to set up and execute tox.

This repo allows me to centralize most of my CI workflows
so I only need to define a testing/configuration matrix in my other projects.


``tox.yaml``
============

The ``tox.yaml`` workflow captures best practices I found over the years
that optimize test suite execution, including tools, plugins, and caching.

It has the following features:

*   Configurable runners
*   Multiple CPython/PyPy interpreter versions per runner
*   Selectable tox environments
*   Schema validation of the inputs passed to the workflow
*   Fast tox environment creation using the ``tox-uv`` plugin
*   Built-in caching of tox and virtual environments with strong cache-busting

For information about how to configure the ``tox.yaml`` workflow,
please see `the tox workflow documentation`_ in the ``docs/`` directory.

..  _the tox workflow documentation: docs/tox.rst


``create-pr.yaml``
==================

The ``create-pr.yaml`` workflow allows me to cut release PRs
and to automate regular update PRs as needed.

It has the following features:

*   A ``version`` workflow input, suitable for cutting new releases
*   Settings for customizing branches, commits, and PRs
*   Verified commits via the GitHub Actions bot account
*   Schema validation of the inputs passed to the workflow

For information about how to configure the ``create-pr.yaml`` workflow,
please see `the create-pr workflow documentation`_ in the ``docs/`` directory.

..  _the create-pr workflow documentation: docs/create-pr.rst
