# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib
import textwrap

from workflow_assets.create_tag_and_release import get_tag_name


def test_get_tag_name(fs, monkeypatch):
    version = "1.2.3"
    fs.create_file(
        "pyproject.toml",
        contents=textwrap.dedent(f"""
            [project]
            version = "{version}"
            """),
    )
    monkeypatch.setenv("GITHUB_ENV", "github-env.txt")
    monkeypatch.setenv("GITHUB_OUTPUT", "github-output.txt")

    get_tag_name.main()

    envvars = pathlib.Path("github-env.txt").read_text().strip().splitlines()
    assert f"TAG_NAME=v{version}" in envvars  # with 'v' prefix

    outputs = pathlib.Path("github-output.txt").read_text().strip().splitlines()
    assert f"project-version={version}" in outputs  # without 'v' prefix
    assert f"tag-name=v{version}" in outputs  # with 'v' prefix
