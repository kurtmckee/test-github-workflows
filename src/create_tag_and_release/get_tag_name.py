# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import os
import pathlib
import tomllib


def main() -> None:
    toml = tomllib.loads(pathlib.Path("pyproject.toml").read_text())
    version = toml["project"]["version"]
    with open(os.environ["GITHUB_ENV"], "a") as file:
        file.write(f"TAG_NAME=v{version}\n")
    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        file.write(f"project-version={version}\n")
        file.write(f"tag-name=v{version}\n")


if __name__ == "__main__":
    main()
