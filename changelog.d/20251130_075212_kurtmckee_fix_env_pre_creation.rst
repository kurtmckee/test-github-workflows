Fixed
-----

-   ``tox``: Only pre-create target environments, if any.

    Previously, the list of target environments was unspecified,
    so tox would pre-create *all* tox environments.
