Changed
-------

-   Use uv for venv creation and check-jsonschema execution.

    On Windows hosts, this reduced check-jsonschema setup and execution
    from ~15 seconds down to ~5 seconds.
    It also reduced virtual environment creation from ~18 seconds to ~3 seconds.
