..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Kurt McKee's GitHub Workflows
#############################

*Reusable workflows that reduce maintenance effort.*

---------------------------------------------------------------------------

This repo centralizes many of my CI workflows.

In many cases, workflows in my other repositories can be minimized
to a set of configuration values and a reference to the workflows here.


Table of contents
=================

*   `tox`_
*   `create-pr`_
*   `create-tag-and-release`_
*   `build-python-package`_


tox
===

The ``tox.yaml`` workflow captures best practices I have found over the years
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


create-pr
=========

The ``create-pr.yaml`` workflow cuts release PRs
and automates regular update PRs as needed.

It has the following features:

*   A ``version`` workflow input, suitable for cutting new releases
*   Settings for customizing branches, commits, and PRs
*   Verified commits via the GitHub Actions bot account
*   Schema validation of the inputs passed to the workflow

For information about how to use the ``create-pr.yaml`` workflow,
please see `the create-pr workflow documentation`_ in the ``docs/`` directory.

..  _the create-pr workflow documentation: docs/create-pr.rst


create-tag-and-release
======================

The ``create-tag-and-release.yaml`` workflow creates a git tag and a GitHub release.

It has the following features:

*   The project version is extracted from ``pyproject.toml``.
*   The version's CHANGELOG entry is extracted using scriv.
*   An annotated git tag named ``v$VERSION`` is created.
    The tag body contains the CHANGELOG entry in GitHub-formatted Markdown.
*   A GitHub release, also named ``v$VERSION``, is created.

For information about how te use the ``create-tag-and-release.yaml`` workflow,
please see `the create-tag-and-release workflow documentation`_
in the ``docs/`` directory.

..  _the create-tag-and-release workflow documentation: docs/create-tag-and-release.rst


build-python-package
====================

The ``build-python-package.yaml`` workflow builds a Python sdist and wheel,
and uploads an artifact containing these.

It has the following features:

*   The project is built using the ``build`` module.
*   An artifact is uploaded to GitHub, suitable for download and publication to PyPI.

For information about how te use the ``build-python-package.yaml`` workflow,
please see `the build-python-package workflow documentation`_
in the ``docs/`` directory.

..  _the build-python-package workflow documentation: docs/build-python-package.rst
