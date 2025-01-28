..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2025 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


``create-pr.yaml``
##################

This reusable workflow runs a defined tox label to create changes to files,
then commits all of the changes and creates a PR.

The reusable workflow takes two inputs:

*   ``config``, which must be a serialized JSON object with keys described below
*   ``version``, which is an optional string that can be referenced by ``config`` values
    and by tox environments.


Table of contents
=================

*   `Permissions`_
*   `Required config keys`_
*   `Optional version input`_
*   `Optional config keys`_
*   `Passing the config to the workflow`_
*   `Workflow examples`_


..  permissions:

Permissions
===========

The workflow requires the GitHub token to have two write permissions:

*   ``contents``
*   ``pull-requests``

These must be set on the calling workflow:

..  code-block:: yaml

    permissions:
      contents: "write"
      pull-requests: "write"


..  required-config-keys:

Required config keys
====================

*   ``tox-label-create-changes``:
    The tox label to run to generate changes that will be committed. Must be a string.

    Example:

    ..  code-block:: yaml

        tox-label-create-changes: "prep-release"


..  optional-version-input:

Optional version input
======================

A ``version`` input may be passed to the workflow, separate from the ``config`` input.
It can then be referenced in several places, including these config keys:

*   ``branch-name`` (example: ``releases/$VERSION``)
*   ``commit-title`` (example: ``Update metadata for v$VERSION``)
*   ``pr-title`` (example: ``Release v$VERSION``)

It will also be available as an environment variable named ``VERSION`` when tox is run.
Tox must be configured to pass ``VERSION`` into the test environment:

..  code-block:: ini

    [testenv:prep-release]
    passenv =
        VERSION
    deps =
        poetry
    commands =
        poetry version {env:VERSION}


..  optional-config-keys:

Optional config keys
====================


*   ``runner``:
    The runner to use.

    ..  code-block:: yaml

        runner: "ubuntu-latest"

*   ``python-version``:
    The CPython interpreter version to install. Must be a string.

    ..  code-block:: yaml

        python-version: "3.13"

*   ``commit-title``:
    The first line of the commit message to use. Must be a string.

    This supports a ``$VERSION`` substitution.

    Examples:

    ..  code-block:: yaml

        commit-title: "Update tool versions"

    ..  code-block:: yaml

        commit-title: "Update project metadata for v$VERSION"

*   ``pr-base``:
    The name of the branch that the PR will be configured to merge to.
    Must be a string.

    The default is ``main``.

    Example:

    ..  code-block:: yaml

        pr-base: "releases"

*   ``pr-title``:
    The title of the PR to open. Must be a string.

    This supports a ``$VERSION`` substitution.

    Examples:

    ..  code-block:: yaml

        pr-title: "Update pre-commit hooks and additional dependencies"

    ..  code-block:: yaml

        pr-title: "Release v$VERSION"

*   ``pr-body``:
    The body of the PR to open. Must be a string.

    This supports a ``$VERSION`` substitution.

    Example:

    ..  code-block:: yaml

        pr-body: "Exactly what it says on the tin."


..  passing-the-config-to-the-workflow:

Passing the config to the workflow
==================================

The workflow requires a JSON-serialized input named ``"config"``.

The easiest way to accomplish this is by using a matrix configuration,
and using the ``toJSON()`` function to serialize it as a workflow input:

..  code-block:: yaml

    strategy:
      matrix:
        include:
          - tox-label-create-changes: "update"

    # ...

    uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
    with:
      config: "${{ toJSON(matrix) }}"


..  workflow-examples:

Workflow examples
=================


Trivial example
---------------

..  code-block:: yaml

    name: "Updates"
    on:
      workflow_dispatch:

    jobs:
      updates:
        name: "${{ 'Updates' || matrix.ignore }}"

        permissions:
          contents: "write"
          pull-requests: "write"

        strategy:
          matrix:
            include:
              - tox-commit-prep-label: "update"

        uses: "kurtmckee/github-workflows/.github/workflows/create-pr.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"


Note that referencing ``matrix`` in the calling workflow name -- which is a no-op here --
tricks GitHub and prevents it from injecting matrix values into the name of each run.
Without this trick, the workflow run would have the generated name "Updates (update)".


Prepare a new release
---------------------

..  code-block:: yaml

    name: "Prep release"
    on:
      workflow_dispatch:
        inputs:
          version:
            description: "The version to release"
            type: "string"
            required: true

    jobs:
      prep-release:
        name: "Prep release v${{ inputs.version }}"

        permissions:
          contents: "write"
          pull-requests: "write"

        strategy:
          matrix:
            include:
              - branch-name: "release/$VERSION"
                commit-title: "Update project metadata"
                pr-title: "Release v$VERSION"
                tox-label-create-changes: "prep-release"

        uses: "kurtmckee/github-workflows/.github/workflows/create-pr.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"
          version: "${{ inputs.version }}"
