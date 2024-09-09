Kurt McKee's GitHub Workflows
#############################

*Reusable workflows that reduce maintenance effort.*

---------------------------------------------------------------------------

I use tox to manage testing in my Python projects,
and I use GitHub workflows to set up and execute tox.

This repo allows me to centralize most of my CI workflows
so I only need to define a testing matrix in my other projects.


``tox.yaml`` workflow features
==============================

The ``tox.yaml`` workflow in this repo has the following features:

*   Configurable runners
*   Multiple CPython/PyPy interpreter versions per runner
*   Selectable tox environments
*   Schema validation of the inputs passed to the workflow
*   Built-in caching of tox and virtual environments with strong cache-busting


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
    Mutually-exclusive with ``tox-pre-environments`` and ``tox-post-environments``.

    Example:

    ..  code-block:: yaml

        tox-environments:
          - "docs"
          - "mypy"

    Resulting tox command:

    ..  code-block::

        tox run -e "docs,mypy"

*   ``tox-pre-environments``:
    An array of of tox environments to run
    before a generated list of all CPython and PyPy environments.
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

*   ``tox-post-environments``:
    An array of of tox environments to run
    after a generated list of all CPython and PyPy environments.
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

*   ``cache-hash-files``:
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
          - ["3.12"]

    uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v0.2"
    with:
      config: "${{ toJSON(matrix) }}"


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

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v0.2"
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

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v0.2"
        with:
          config: "${{ toJSON(matrix) }}"


Run individual configurations
-----------------------------

..  code-block:: yaml

    jobs:
      test:
        strategy:
          matrix:
            config:
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

        uses: "kurtmckee/github-workflows/.github/workflows/tox.yaml@v0.2"
        with:
          config: "${{ toJSON(matrix.config) }}"
