# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import json
import os

with open("config.json") as file:
    config = json.load(file)

# Transform the tox environments for convenience.
# "pre-environments" and "post-environments" will be injected into "environments",
# together with a full list of CPython and PyPy interpreter versions.
# Since these keys are mutually-exclusive with "environments",
# no config data are lost in this transformation.
if {"pre-environments", "post-environments"} & config.get("tox", {}).keys():
    environments = config["tox"].pop("pre-environments", [])
    environments.extend(f"py{version}" for version in config.get("cpythons", []))
    if "cpython-beta" in config:
        environments.append(f"py{config['cpython-beta']}")
    environments.extend(f"pypy{version}" for version in config.get("pypys", []))
    environments.extend(config["tox"].pop("post-environments", []))
    config["tox"]["environments"] = environments

output = json.dumps(config, sort_keys=True, separators=(",", ":"))
with open(os.environ["GITHUB_OUTPUT"], "a") as file:
    file.write(f"config={output}")
