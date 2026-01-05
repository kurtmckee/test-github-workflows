# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import json
import os
import pathlib
import re
import typing


def transform_config(config: dict[str, typing.Any]) -> None:
    # Transform the tox environments for convenience.
    # pre- and post-environments will be assembled into "tox-environments",
    # together with a full list of CPython and PyPy interpreter versions.
    # Since these keys are mutually-exclusive with "tox-environments",
    # no config data are lost in this transformation.
    tox_factors = config.pop("tox-factors", [])
    factors = f"-{'-'.join(tox_factors)}" if tox_factors else ""
    cpythons = config.get("cpythons", [])
    cpython_beta = config.get("cpython-beta")
    pypys = config.get("pypys", [])

    if (
        factors
        or config.pop("tox-environments-from-pythons", False)
        or {"tox-pre-environments", "tox-post-environments"} & config.keys()
    ):
        environments = config.pop("tox-pre-environments", [])
        environments.extend(f"py{version}{factors}" for version in cpythons)
        if cpython_beta is not None:
            environments.append(f"py{cpython_beta}{factors}")
        environments.extend(f"pypy{version}{factors}" for version in pypys)
        environments.extend(config.pop("tox-post-environments", []))
        config["tox-environments"] = environments

    python_versions_requested = [f"pypy{version}" for version in pypys]
    if cpython_beta is not None:
        python_versions_requested.append(cpython_beta)
    python_versions_requested.extend(cpythons)

    # Because tox only offers "best effort" PyPy support,
    # and because tox may not support CPython alphas or betas,
    # a stable CPython version must be included during initial Python setup.
    python_versions_required = python_versions_requested.copy()
    if not cpythons:
        python_versions_required.append("3.13")
    config["python-versions-requested"] = "\n".join(python_versions_requested)
    config["python-versions-required"] = "\n".join(python_versions_required)

    # Prepare the environments to skip.
    skip_patterns: list[str] = []
    for environment in config.pop("tox-skip-environments", []):
        skip_patterns.append(re.escape(environment))
    skip_patterns.sort()
    if pattern := config.pop("tox-skip-environments-regex", ""):
        skip_patterns.append(pattern)
    config["tox-skip-environments-regex"] = "|".join(skip_patterns)


def main() -> None:
    # Load
    raw_config_path = pathlib.Path(".tox-config.raw.json")
    config = json.loads(raw_config_path.read_text())

    # Transform in-place
    transform_config(config)

    # Write
    output = json.dumps(config, sort_keys=True, separators=(",", ":"))
    with open(os.environ["GITHUB_ENV"], "a") as file:
        file.write(f"tox-config={output}")


if __name__ == "__main__":
    main()
