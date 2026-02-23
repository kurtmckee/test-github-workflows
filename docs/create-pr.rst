..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


``create-pr.yaml``
##################

This reusable workflow runs a defined tox label to create changes to files,
then commits all of the changes and creates a draft PR.

The reusable workflow takes two inputs:

*   ``config``, which must be a serialized JSON object with keys described below.
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

In addition, GitHub will block the GitHub Actions bot from opening PRs
unless a checkbox in the repository settings is ticked:

..  code-block:: text

    Settings > Actions > General > Allow GitHub Actions to create and approve pull requests


Required config keys
====================

*   ``tox-label-create-changes``:
    The tox label to run to generate changes that will be committed. Must be a string.

    Example:

    ..  code-block:: yaml

        tox-label-create-changes: "prep-release"

    When tox is run, two environment variables will be available:

    *   ``PR_BODY_OUTPUT_PATH``, which a tox environment can write a PR body to
    *   ``VERSION``, which will contain the optional ``version`` input value

    These should be passed to the tox environments using the tox ``pass_env`` config.

    Example:

    ..  code-block:: ini

        [testenv:prep-release]
        description = Make the changes needed to create a new release PR
        skip_install = true
        deps =
            poetry
            scriv
        pass_env =
            PR_BODY_OUTPUT_PATH
            VERSION
        commands =
            # Fail if $VERSION is not set.
            python -Ec 'import os; assert (v := os.getenv("VERSION")) is not None, v'
            poetry version "{env:VERSION}"
            scriv collect
            scriv print --version "{env:VERSION}" --output "{env:PR_BODY_OUTPUT_PATH:{env:VERSION}.rst}"


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
    pass_env =
        VERSION
    deps =
        poetry
    commands =
        poetry version {env:VERSION}


Optional config keys
====================


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

*   ``pr-body-input-format``:
    The format of the PR body. Must be a string.

    Currently only ``gfm`` and ``rst`` are allowed values.
    The default is ``rst``.


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
              - tox-label-create-changes: "update"

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
                commit-title: "Update project metadata for v$VERSION"
                pr-title: "Release v$VERSION"
                tox-label-create-changes: "prep-release"

        uses: "kurtmckee/github-workflows/.github/workflows/create-pr.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"
          version: "${{ inputs.version }}"
