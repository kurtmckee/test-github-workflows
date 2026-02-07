..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


``create-tag-and-release.yaml``
###############################

This reusable workflow creates an annotated git tag and a GitHub release.

The git tag will contain the current version's CHANGELOG fragment
in GitHub-formatted Markdown.

It currently takes no inputs.


Table of contents
=================

*   `Requirements`_
*   `Permissions`_
*   `Outputs`_
*   `Workflow example`_


Requirements
============

*   The project must have ``project.version`` set in ``pyproject.toml``.
    The version cannot be a "dynamic" value.
*   The project must use scriv to manage its CHANGELOG.
*   The CHANGELOG must be in Restructured Text format.


Permissions
===========

The workflow requires the GitHub token to have write permissions for ``contents``.

These must be set on the calling workflow:

..  code-block:: yaml

    permissions:
      contents: "write"


Outputs
=======

*   ``project-version``

    The version of the project extracted from ``project.version`` in ``pyproject.toml``.
    For example, ``v1.2.3``.

*   ``tag-name``

    The name of the git tag that was created.

    This is always the project version string prepended with the letter ``v``.
    For example, ``v1.2.3``.


Workflow example
================

..  code-block:: yaml

    name: "Tag and release"
    on:
      push:
        branches:
          - "releases"

    jobs:
      tag:
        name: "Tag and release"

        permissions:
          contents: "write"

        uses: "kurtmckee/github-workflows/.github/workflows/create-tag-and-release.yaml@..."
