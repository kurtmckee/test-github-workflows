# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib
import typing as t

import pytest

from workflow_assets.create_tag_and_release import validate_repo_state


def create_runner_mock(
    config: dict[str, tuple[int, str, str]],
) -> t.Callable[[str, ...], tuple[int, str, str]]:
    """Mock the CLI runner.

    The config keys are arguments found in the CLI runner arguments.
    For example, the config key "rev-parse" will match the CLI invocation
    ["git", "rev-parse", ...].

    The config values are tuples representing the exit code, STDOUT, and STDERR.
    """

    def runner_mock(*args: str) -> tuple[int, str, str]:
        for key, value in config.items():
            if key in args:
                return value

        raise KeyError(f"No args matched the runner mock config: {args}")

    return runner_mock


def test_validate_repo_state_common_case(fs, monkeypatch):
    """If no tag exists, `tag-exists` must be `false`."""

    runner_mock = create_runner_mock(
        {
            "rev-parse": (0, "0000000000000000000000000000000000000000", ""),
            "rev-list": (
                128,
                "",
                "fatal: bad revision 'tags/v1.2.3'",
            ),
        }
    )
    monkeypatch.setenv("TAG_NAME", "v1.2.3")
    monkeypatch.setenv("GITHUB_OUTPUT", "outputs.txt")
    monkeypatch.setattr(validate_repo_state, "_run_command", runner_mock)

    validate_repo_state.main()

    assert "tag-exists=false" in pathlib.Path("outputs.txt").read_text().splitlines()


def test_validate_repo_state_tag_exists(fs, monkeypatch):
    """If a tag exists and matches HEAD, `tag-exists` must be `true`."""

    runner_mock = create_runner_mock(
        {
            "rev-parse": (0, "0" * 40, ""),
            "rev-list": (0, "0" * 40, ""),
        }
    )
    monkeypatch.setenv("TAG_NAME", "v1.2.3")
    monkeypatch.setenv("GITHUB_OUTPUT", "outputs.txt")
    monkeypatch.setattr(validate_repo_state, "_run_command", runner_mock)

    validate_repo_state.main()

    assert "tag-exists=true" in pathlib.Path("outputs.txt").read_text().splitlines()


def test_validate_repo_state_tag_does_not_match_head(fs, monkeypatch, capsys):
    """If a tag exists and does not match HEAD, an error must be raised."""

    runner_mock = create_runner_mock(
        {
            "rev-parse": (0, "0" * 40, ""),
            "rev-list": (0, "1" * 40, ""),
        }
    )
    monkeypatch.setenv("TAG_NAME", "v1.2.3")
    monkeypatch.setenv("GITHUB_OUTPUT", "outputs.txt")
    monkeypatch.setattr(validate_repo_state, "_run_command", runner_mock)

    with pytest.raises(SystemExit):
        validate_repo_state.main()

    assert not pathlib.Path("outputs.txt").is_file()
    stdout, stderr = capsys.readouterr()
    assert not stdout
    msg = (
        f"::error::The v1.2.3 tag commit SHA ({'1' * 40})"
        f" doesn't match HEAD ({'0' * 40})."
    )
    assert msg in stderr


def test_unexpected_git_rev_list_behavior(fs, monkeypatch, capsys):
    """Verify the unexpected git rev-list behavior.

    If `git` doesn't return exit code 128, but STDOUT doesn't contain a SHA,
    then something very wrong has happened.
    For example, the current directory might not be a git repository.
    """

    fatal = "fatal: not a git repository (or any of the parent directories): .git"
    runner_mock = create_runner_mock(
        {
            "rev-parse": (128, "", fatal),
            "rev-list": (128, "", fatal),
        }
    )
    monkeypatch.setenv("TAG_NAME", "v1.2.3")
    monkeypatch.setenv("GITHUB_OUTPUT", "outputs.txt")
    monkeypatch.setattr(validate_repo_state, "_run_command", runner_mock)

    with pytest.raises(SystemExit):
        validate_repo_state.main()

    assert not pathlib.Path("outputs.txt").is_file()

    stdout, stderr = capsys.readouterr()
    assert not stdout
    assert "::error::Something unexpected happened.\n" in stderr
    assert "Return code:\n128\n" in stderr
    assert "STDOUT:\n\n" in stderr
    assert f"STDERR:\n{fatal}" in stderr


def test_run_command_success():
    cmd = ("python", "-V")
    rc, stdout, stderr = validate_repo_state._run_command(*cmd)

    assert rc == 0
    assert "Python" in stdout
    assert stderr == ""


def test_run_command_timeout():
    cmd = ("python", "-c", "import time; time.sleep(1)")
    rc, stdout, stderr = validate_repo_state._run_command(
        *cmd,
        timeout=0,
    )

    assert rc != 0
    assert stdout == ""
    assert stderr == ""
