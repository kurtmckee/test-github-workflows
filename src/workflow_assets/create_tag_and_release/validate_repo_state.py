# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import os
import subprocess
import sys
import typing as t


def main() -> None:
    tag_name = os.environ["TAG_NAME"]
    head_sha = _get_head_sha()
    existing_tag_sha = _get_existing_tag_sha(tag_name)
    if existing_tag_sha is None:
        tag_exists = False
    elif existing_tag_sha == head_sha:
        tag_exists = True
    else:
        msg = (
            f"The {tag_name} tag commit SHA ({existing_tag_sha})"
            f" doesn't match HEAD ({head_sha})."
        )
        exit_with_error(msg)

    with open(os.environ["GITHUB_OUTPUT"], "a") as file:
        file.write(f"tag-exists={str(tag_exists).lower()}\n")


def _get_head_sha() -> str:
    """Get the SHA of HEAD."""

    _, stdout, _ = _run_command("git", "rev-parse", "HEAD")
    return stdout.strip()


def _get_existing_tag_sha(tag_name: str) -> str | None:
    """Validate the project version and git repo state are compatible.

    "Compatibility" is defined as one of:

    *   The project version has no corresponding git tag ref.
    *   A git tag ref exists for the project version,
        and its commit SHA matches the SHA currently checked out in HEAD.
    """

    # Check if a tag exists.
    cmd = ("git", "rev-list", "-n", "1", f"tags/{tag_name}", "--")
    rc, stdout, stderr = _run_command(*cmd)
    if rc == 128 and "bad revision" in stderr:
        # The tag doesn't exist locally. This is the expected case.
        return None

    # The output must be a commit SHA.
    tag_commit_sha = stdout.strip()
    try:
        int(tag_commit_sha, base=16)
    except ValueError:
        msg = "Something unexpected happened."
        exit_with_error(msg, rc, stdout, stderr)

    # A git tag already exists.
    return tag_commit_sha


def _run_command(*args: str, timeout: int = 10) -> tuple[int, str, str]:
    """Run a command."""

    process = subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def exit_with_error(
    msg: str,
    rc: int | None = None,
    stdout: str | None = None,
    stderr: str | None = None,
) -> t.NoReturn:
    print(f"::error::{msg}", file=sys.stderr)
    if rc is not None:
        print(f"Return code:\n{rc}", file=sys.stderr)
    if stdout is not None:
        print(f"STDOUT:\n{stdout}", file=sys.stderr)
    if stderr is not None:
        print(f"STDERR:\n{stderr}", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
