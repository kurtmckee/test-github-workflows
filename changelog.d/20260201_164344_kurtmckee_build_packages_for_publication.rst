Added
-----

*   Add a workflow named ``create-tag-and-release``.

    The initial version has the following features:

    *   The project version is extracted from ``pyproject.toml``.
    *   The version's CHANGELOG entry is extracted using scriv.
    *   An annotated git tag named ``v$VERSION`` is created.
        The tag body contains the CHANGELOG entry in GitHub-formatted Markdown.
    *   A GitHub release, also named ``v$VERSION``, is created.

*   Add a workflow named ``build-python-package``.

    The initial version has the following features:

    *   The project is built using the ``build`` module.
    *   An artifact is uploaded to GitHub, suitable for download and publication to PyPI.
