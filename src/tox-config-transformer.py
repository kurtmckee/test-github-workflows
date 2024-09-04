# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import json
import os
import pathlib
import typing

runner_temp = pathlib.Path(os.environ["RUNNER_TEMP"])


def load_raw_config() -> dict[str, typing.Any]:
    raw_config_path = runner_temp / "tox-config.raw.json"
    return json.loads(raw_config_path.read_text())


def transform_config(config: dict[str, typing.Any]):
    # Transform the tox environments for convenience.
    # pre- and post-environments will be assembled into "tox-environments",
    # together with a full list of CPython and PyPy interpreter versions.
    # Since these keys are mutually-exclusive with "tox-environments",
    # no config data are lost in this transformation.
    if {"tox-pre-environments", "tox-post-environments"} & config.keys():
        environments = config.pop("tox-pre-environments", [])
        environments.extend(f"py{version}" for version in config.get("cpythons", []))
        if "cpython-beta" in config:
            environments.append(f"py{config['cpython-beta']}")
        environments.extend(f"pypy{version}" for version in config.get("pypys", []))
        environments.extend(config.pop("tox-post-environments", []))
        config["tox-environments"] = environments


def write_config(config: dict[str, typing.Any]) -> None:
    output = json.dumps(config, sort_keys=True, separators=(",", ":"))
    with open(os.environ["GITHUB_ENV"], "a") as file:
        file.write(f"tox-config={output}")
    (runner_temp / "tox-config.json").write_text(output)


def main() -> None:
    config = load_raw_config()
    transform_config(config)
    write_config(config)


if __name__ == "__main__":
    main()
