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

    *   `Runners`_
    *   `Python interpreters`_
    *   `Tox environments`_
    *   `Caching`_

*   `Passing the config to the workflow`_
*   `Workflow examples`_
*   `Controlling the job name`_


Config keys
===========


Runners
-------

*   ``runner``:
    The runner to use.

    ..  code-block:: yaml

        runner: "ubuntu-latest"


Python interpreters
-------------------

*   ``cpythons``:
    An array of CPython interpreter versions to install. Items must be strings.

    ..  code-block:: yaml

        cpythons:
          - "3.12"
          - "3.13"

*   ``cpython-beta``:
    A CPython interpreter beta to install. Must be a string.

    Tox will *never* be installed using a beta CPython interpreter.
    The workflow will install a non-beta CPython interpreter if necessary
    to avoid installing and executing tox on a beta CPython interpreter,
    so it may be necessary to specify which tox environments to run
    if the goal is to exclusively run the test suite with the beta interpreter.

    Example:

    ..  code-block:: yaml

        cpython-beta: "3.14"

*   ``pypys``:
    An array of PyPy interpreter versions to install. Items must be strings.

    Tox will *never* be installed using a PyPy interpreter.
    The workflow will install a CPython interpreter if necessary
    to avoid installing and executing tox on a PyPy interpreter,
    so it may be necessary to specify which tox environments to run
    if the goal is to exclusively run the test suite with the PyPy interpreters.

    Example:

    ..  code-block:: yaml

        pypys:
          - "3.10"
          - "3.11"


Tox environments
----------------

*   ``tox-environments``:
    An array of tox environments to run. Items must be strings.

    If provided, only the given environment names will be run.

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
          - "3.11"
        tox-environments-from-pythons: true

    Resulting tox command:

    ..  code-block::

        tox run -e "py3.12,py3.13,py3.14,pypy3.11"
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
          - "3.13"
        pypys:
          - "3.11"
        tox-pre-environments:
          - "flake8"

    Resulting tox command:

    ..  code-block::

        tox run -e "flake8,py3.13,pypy3.11"
                    ^^^^^^

*   ``tox-post-environments``:
    An array of tox environments to run
    after a generated list of all configured Python interpreters as tox environments.

    Configuring this key automatically enables ``tox-environments-from-pythons``.

    Mutually-exclusive with ``tox-environments``.

    Example:

    ..  code-block:: yaml

        cpythons:
          - "3.12"
        pypys:
          - "3.11"
        tox-post-environments:
          - "coverage"

    Resulting tox command:

    ..  code-block::

        tox run -e "py3.12,pypy3.11,coverage"
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

        export TOX_SKIP_ENV='coverage-html|docs'
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

        export TOX_SKIP_ENV='coverage-html|docs|mypy-.*'
                             ^^^^^^^^^^^^^ ^^^^ ^^^^^^^
        tox


Caching
-------

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
          - ["3.13"]

    uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
    with:
      config: "${{ toJSON(matrix) }}"

There is one ``runner`` value (the string ``"ubuntu-latest"``)
and one ``cpythons`` value (the list ``["3.12"]``),
so this matrix will result in only one JSON config:

..  code-block:: json

    {
      "runner": "ubuntu-latest",
      "cpythons": ["3.13"]
    }


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

            # The single value in this `include` section will be added to each runner.
            include:
              - cpythons:
                  - "3.10"
                  - "3.11"
                  - "3.12"
                  - "3.13"
                cpython-beta: "3.14"
                pypys:
                  - "3.10"
                  - "3.11"

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"

There are three ``runner`` values in the matrix
and the single ``include`` object does not have a ``runner`` value,
so this results in three JSON configurations, one for each given ``runner``.
An example of the ``"ubuntu-latest"`` runner's JSON config is shown below:

..  code-block:: json

    {
      "runner": "ubuntu-latest",
      "cpythons": ["3.10", "3.11", "3.12", "3.13"],
      "cpython-beta": "3.14",
      "pypys": ["3.10", "3.11"]
    }


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
                  - "3.10"
                  - "3.11"
                  - "3.12"
                  - "3.13"

              # Test only the highest and lowest Pythons on Windows.
              - runner: "windows-latest"
                cpythons:
                  - "3.10"
                  - "3.13"

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v1"
        with:
          config: "${{ toJSON(matrix) }}"


Controlling the job name
========================

When using a ``matrix``, GitHub automatically appends matrix values
to the job name to help differentiate the matrix configuration from each other.

Consider a matrix like the following:

..  code-block:: yaml

    name: "🧪 Test"
    jobs:
      test:
        name: "Linux"
        strategy:
          matrix:
            include:
              - runner: "ubuntu-latest"
                cpythons: ["3.13"]


GitHub will combine the name of the workflow (``"🧪 Test"``),
the name of the job (``"Linux"``), and the name of the tox workflow.
However, it will also append matrix values to the job name in parantheses,
resulting in this check name:

..  code-block::

    🧪 Test / Linux (ubuntu-latest, 3.13) / tox


As the number matrix values grow, so too will the length of the job name.

This behavior can be suppressed by referencing a ``matrix`` value in the job name.

#.  The name can be hard-coded in the job name,
    and a bogus matrix value can be referenced.

    ..  code-block:: yaml

        jobs:
          test:
            name: "${{ 'Linux' || matrix.bogus }}"
            strategy:
              matrix:
                include:
                  - name: "Linux"
                    runner: "ubuntu-latest"
                    cpythons: ["3.13"]

    This results in the following check name:

    ..  code-block::

        🧪 Test / Linux / tox


#.  The name can be hard-coded into the matrix and referenced.

    ..  code-block:: yaml

        jobs:
          test:
            name: "${{ matrix.name }}"
            strategy:
              matrix:
                include:
                  - name: "Linux"
                    runner: "ubuntu-latest"
                    cpythons: ["3.13"]

    This results in the following check name:

    ..  code-block::

        🧪 Test / Linux / tox

#.  For a more complicated workflow,
    the name can be calculated based on matrix values.

    ..  code-block::

        jobs:
          test:
            name:
              "${{
                (startswith(matrix.runner, 'ubuntu') && 'Linux')
                || (startswith(matrix.runner, 'macos') && 'macOS')
                || (startswith(matrix.runner, 'windows') && 'Windows')
              }}"
            strategy:
              matrix:
                runner:
                  - "ubuntu-latest"
                  - "macos-latest"
                  - "windows-latest"
                include:
                  - cpythons: ["3.13"]

    This results in the following check names:

    ..  code-block::

        🧪 Test / Linux / tox
        🧪 Test / macOS / tox
        🧪 Test / Windows / tox
