Fixed
-----

*   Fix ``tox.pre-environments`` and ``tox.post-environments``, which were ignored.
*   Fix ``cache.hash-files`` checksum calculations,
    which relied on a command that's unavailable on macOS.
