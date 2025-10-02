..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2025 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


``tox.yaml``
############

This reusable workflow puts a lot of engineering effort into this one task:
running tox.

It captures years of experience for speedy test suite execution in a CI environment,
and is configured via a single workflow input named ``config``,
which must be a JSON object serialized via GitHub's ``toJSON()`` workflow function.


Table of contents
=================

*   `Config keys`_
*   `Passing the config to the workflow`_
*   `Workflow examples`_


..  config-keys:

Config keys
===========

*   ``runner``:
    The runner to use.

    ..  code-block:: yaml

        runner: "ubuntu-latest"

*   ``cpythons``:
    An array of CPython interpreter versions to install. Items must be strings.

    ..  code-block:: yaml

        cpythons:
          - "3.11"
          - "3.12"

*   ``cpython-beta``:
    The CPython interpreter beta to install. Must be a string.

    Example:

    ..  code-block:: yaml

        cpython-beta: "3.13"

*   ``pypys``:
    An array of PyPy interpreter versions to install. Items must be strings.

    Example:

    ..  code-block:: yaml

        pypys:
          - "3.9"
          - "3.10"

*   ``tox-environments``:
    An array of tox environments to run. Items must be strings.

    Mutually-exclusive with:

    *   ``tox-environments-from-pythons``
    *   ``tox-factors``
    *   ``tox-pre-environments``
    *   ``tox-post-environments``
    *   ``tox-skip-environments``
    *   ``tox-skip-environments-regex``

    Example:

    ..  code-block:: yaml

        tox-environments:
          - "docs"
          - "mypy"

    Resulting tox command:

    ..  code-block::

        tox run -e "docs,mypy"
                    ^^^^ ^^^^

*   ``tox-environments-from-pythons``:
    A boolean flag that controls whether the configured Python interpreters
    will be converted to a list of specific tox environments to execute.

    If configured, the only allowed value is ``true``.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.12"
          - "3.13"
        cpython-beta: "3.14"
        pypys:
          - "3.10"
        tox-environments-from-pythons: true

    Resulting tox command:

    ..  code-block::

        tox run -e "py3.12,py3.13,py3.14,pypy3.10"
                    ^^^^^^ ^^^^^^ ^^^^^^ ^^^^^^^^

*   ``tox-factors``:
    An array of factors to add to the ends of generated tox environment names.

    Configuring this key automatically enables ``tox-environments-from-pythons``.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.12"
          - "3.13"
        tox-factors:
          - "ci"

    Resulting tox command:

    ..  code-block::

        tox run -e "py3.12-ci,py3.13-ci"
                          ^^^       ^^^

*   ``tox-pre-environments``:
    An array of tox environments to run
    before a generated list of all configured Python interpreters as tox environments.

    Configuring this key automatically enables ``tox-environments-from-pythons``.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.11"
        pypys:
          - "3.10"
        tox-pre-environments:
          - "flake8"

    Resulting tox command:

    ..  code-block::

        tox run -e "flake8,py3.11,pypy3.10"
                    ^^^^^^

*   ``tox-post-environments``:
    An array of tox environments to run
    after a generated list of all configured Python interpreters as tox environments.

    Configuring this key automatically enables ``tox-environments-from-pythons``.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.11"
        pypys:
          - "3.10"
        tox-post-environments:
          - "coverage"

    Resulting tox command:

    ..  code-block::

        tox run -e "py3.11,pypy3.10,coverage"
                                    ^^^^^^^^

*   ``tox-skip-environments``:
    An array of tox environment names to skip.

    The names will be sorted, escaped, and combined into a regular expression.
    Current tox behavior is to *match* -- not *search* -- names against the pattern,
    so if this option is used, the names must exactly match tox environment names.

    For true regular expression matching, see ``tox-skip-environments-regex`` below.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.13"
        tox-skip-environments:
          - "coverage-html"
          - "docs"

    Resulting tox command:

    ..  code-block::

        export TOX_SKIP_ENVS='coverage-html|docs'
                              ^^^^^^^^^^^^^ ^^^^
        tox

*   ``tox-skip-environments-regex``:
    A regular expression of tox environment names to skip.

    If used with ``tox-skip-environments``, the patterns will be combined.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.13"
        tox-skip-environments:
          - "coverage-html"
          - "docs"
        tox-skip-environments-regex: "mypy-.*"

    Resulting tox command:

    ..  code-block::

        export TOX_SKIP_ENVS='coverage-html|docs|mypy-.*'
                              ^^^^^^^^^^^^^ ^^^^ ^^^^^^^
        tox

*   ``cache-paths``:
    An array of additional paths to cache.

    By default, a virtual environment is created in ``.venv/`` with tox installed,
    and tox virtual environments are created when tox runs in ``.tox/``.
    These two directories are always cached and can be augmented by ``cache-paths``.

    Example:

    ..  code-block:: yaml

        cache-paths:
          - ".mypy_cache/"

    Resulting ``actions/cache`` configuration:

    ..  code-block:: yaml

        uses: "actions/cache@???"
        with:
          path: |
            .tox/
            .venv/
            .mypy_cache/

*   ``cache-key-prefix``:
    The string prefix to use with the cache. Defaults to ``"tox"``.

    Example:

    ..  code-block:: yaml

        cache-key-prefix: "docs"

    Resulting ``actions/cache`` configuration:

    ..  code-block:: yaml

        uses: "actions/cache@???"
        with:
          key: "docs-..."

*   ``cache-key-hash-files``:
    An array of paths (or glob patterns) to hash and include in the cache key
    for cache-busting.

    Note that the existence of the path or glob patterns is validated;
    if paths do not exist, or the glob patterns match nothing, the workflow will fail.

    Example:

    ..  code-block:: yaml

        cache-key-hash-files:
          - "pyproject.toml"
          - "requirements/*/*.txt"

    A file named ``.hash-files.sha`` will be generated containing SHA-1 checksums.
    The resulting ``actions/cache`` configuration will be:

    ..  code-block:: yaml

        uses: "actions/cache@???"
        with:
          key: "...${{ hashFiles('.python-identifiers', '.workflow-config.json', 'tox.ini', '.hash-files.sha') }}"


..  passing-the-config-to-the-workflow:

Passing the config to the workflow
==================================

The workflow requires a JSON-serialized input named ``"config"``.

The easiest way to accomplish this is by using a matrix configuration,
and using the ``toJSON()`` function to serialize it as a workflow input:

..  code-block:: yaml

    strategy:
      matrix:
        runner:
          - "ubuntu-latest"
        cpythons:
          - ["3.12"]

    uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
    with:
      config: "${{ toJSON(matrix) }}"


..  workflow-examples:

Workflow examples
=================

Test all Python versions on each operating system
-------------------------------------------------

..  code-block:: yaml

    jobs:
      test:
        strategy:
          matrix:
            runner:
              - "ubuntu-latest"
              - "macos-latest"
              - "windows-latest"

            # Use a nested list syntax with the "cpythons" key.
            cpythons:
              - - "3.8"
                - "3.9"
                - "3.10"
                - "3.11"
                - "3.12"

            # Test a beta CPython version.
            cpython-beta:
              - "3.13"

            # Use a nested list syntax with the "pypys" key.
            pypys:
              - - "3.8"
                - "3.9"
                - "3.10"

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"


Similar to above, but add lint tests
------------------------------------

..  code-block:: yaml

    jobs:
      test:
        strategy:
          matrix:
            runner:
              - "ubuntu-latest"

            cpythons:
              - - "3.11"
                - "3.12"

            include:
              - runner: "ubuntu-latest"
                cpythons:
                  - "3.12"
                tox-environments:
                  - "docs"
                  - "mypy"
                cache-key-prefix: "lint"
                cache-paths:
                  - ".mypy_cache/"

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"


Run individual configurations
-----------------------------

..  code-block:: yaml

    jobs:
      test:
        strategy:
          matrix:
            include:
              # Test all Python versions on Ubuntu.
              - runner: "ubuntu-latest"
                cpythons:
                  - "3.8"
                  - "3.9"
                  - "3.10"
                  - "3.11"
                  - "3.12"

              # Test only the highest and lowest Pythons on Windows.
              - runner: "windows-latest"
                cpythons:
                  - "3.8"
                  - "3.12"

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"
