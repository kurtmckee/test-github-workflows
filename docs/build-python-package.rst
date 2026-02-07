..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


``build-python-package.yaml``
#############################

This reusable workflow builds a Python package and uploads an artifact.

The repository is checked out at the git commit SHA that triggered the run.

It currently takes no inputs.


Table of contents
=================

*   `Requirements`_
*   `Permissions`_
*   `Outputs`_
*   `Workflow example`_


Requirements
============

*   The project must be buildable solely using the Python ``build`` module.

    No additional dependencies are pre-installed for building.


Permissions
===========

The workflow requires the GitHub token to have read permissions for ``contents``.

This is the default, but it is recommended that permissions be explicitly set.

..  code-block:: yaml

    permissions:
      contents: "read"


Outputs
=======

*   ``artifact-id``

    The ID of the artifact that was uploaded.

    This can be downloaded by a publishing workflow.

*   ``packages-path``

    The directory that the packages were built in.


Workflow example
================

..  code-block:: yaml

    name: "Build and publish"
    on:
      push:
        branches:
          - "releases"

    jobs:
      build:
        name: "Build"

        permissions:
          contents: "read"

        uses: "kurtmckee/github-workflows/.github/workflows/build-python-package.yaml@..."

      publish:
        name: "Publish"
        needs:
          - "build"

        steps:
          - name: "Download artifact"
            uses: "actions/download-artifact@..."
            with:
              artifact-ids: "${{ needs.build.outputs.artifact-id }}"
