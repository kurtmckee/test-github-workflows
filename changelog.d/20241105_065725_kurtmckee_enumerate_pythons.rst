Changed
-------

-   Guarantee that a stable CPython interpreter is available for tox to use.

    Because tox only offers "best effort" support for PyPy,
    and might not support a given CPython alpha or beta,
    CPython 3.12 will now be set up automatically for tox to use.

    Just prior to running tox, ``actions/setup-python`` will be run again
    to ensure that only the requested Python interpreters are on the PATH.
