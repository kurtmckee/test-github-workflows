# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import base64
import textwrap
import typing
import unittest.mock

import pytest

from workflow_assets.create_pr import create_commit_request_body


@pytest.fixture(autouse=True, scope="session")
def git_status() -> typing.Iterator[None]:
    stdout = textwrap.dedent("""\
        ?? new_file
        D  subdir/deleted_file
        M  modified_file
        """).strip()
    with unittest.mock.patch("subprocess.check_output", lambda _: stdout.encode()):
        yield


def test_generate_file_changes(fs):
    fs.create_file("new_file", contents="?" * 1000)
    fs.create_file("modified_file", contents=b"\xfe\xef\x00")
    file_changes = create_commit_request_body.calculate_file_changes()

    # Ensure that file paths are POSIX-normalized.
    assert file_changes["deletions"] == [{"path": "subdir/deleted_file"}]

    # new_file is long; it must be base64-encoded with no newlines.
    assert file_changes["additions"][0]["path"] == "new_file"
    assert "?" not in file_changes["additions"][0]["contents"]
    assert "\n" not in file_changes["additions"][0]["contents"]

    # modified_file is binary; ensure it decodes as expected.
    assert file_changes["additions"][1]["path"] == "modified_file"
    assert base64.b64decode(file_changes["additions"][1]["contents"]) == b"\xfe\xef\x00"


def test_version_injection(monkeypatch):
    monkeypatch.setenv("VERSION", "1.2.3")
    assert create_commit_request_body.inject_version("v") == "v"
    assert create_commit_request_body.inject_version("v$VERSION") == "v1.2.3"
    assert create_commit_request_body.inject_version("v$version") == "v1.2.3"
