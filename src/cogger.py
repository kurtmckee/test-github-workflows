# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT


import itertools
import pathlib

root = pathlib.Path(__file__).parent.parent


def output(file_path: str) -> None:
    """Print this file's contents so cog can inject it into the workflow.

    This function is run by cog in a pre-commit hook.
    """

    path = root / file_path
    content = path.read_text()

    iterator = itertools.dropwhile(
        lambda line: line.startswith("# "),
        content.splitlines(),
    )
    content = "\n".join(iterator).lstrip()

    print("# DO NOT EDIT THIS CODE BLOCK!")
    print(f"# INSTEAD, EDIT {file_path}.")
    print()
    print(content)
