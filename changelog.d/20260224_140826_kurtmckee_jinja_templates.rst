Breaking changes
----------------

*   ``create-pr``: No longer accept a ``runner`` config.

    The workflow would not work on macOS or Windows runners.
    The runner is currently set to ``ubuntu-24.04``.

Fixed
-----

*   ``create-pr``: Ensure that a PR body file always exists.

    This fixes a "does not exist" error from pandoc that occurs
    if the tox label doesn't create a PR body file
    and the ``pr-body`` workflow input is empty.

Changed
-------

*   Lock almost all software dependencies.
*   Update all software dependencies.

Documentation
-------------

*   ``create-pr``: Document the ``pr-body-input-format`` config key.

Development
-----------

*   Use templates to generate standalone reusable workflow files.

    Now, instead of disallowing edits to portions of the workflows,
    the underlying templates are fully editable.

*   Use prek to update pre-commit hook versions.
