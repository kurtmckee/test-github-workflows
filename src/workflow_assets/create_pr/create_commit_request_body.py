# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import typing

RC_SUCCESS = 0
RC_FAILURE = 1

mandatory_environment_variables = {
    "BRANCH_NAME",
    "COMMIT_TITLE",
    "GITHUB_REPOSITORY",
    "GITHUB_SHA",
    "OUTPUT_FILE",
}


def main() -> int:
    # Ensure mandatory environment variables are present.
    if missing_keys := (mandatory_environment_variables - os.environ.keys()):
        for missing_key in missing_keys:
            print(f"`{missing_key}` is a mandatory environment variable.")
        return RC_FAILURE

    # Calculate file changes (and exit if there are none).
    file_changes = calculate_file_changes()
    if not file_changes:
        print("No file changes detected.")
        return RC_FAILURE

    request_body = generate_request_body(file_changes)

    output_file = os.environ["OUTPUT_FILE"]
    if output_file == "-":
        print(json.dumps(request_body, indent=2))
    else:
        with open(output_file, "w") as file:
            file.write(json.dumps(request_body))

    return RC_SUCCESS


def generate_request_body(file_changes: dict[str, typing.Any]) -> dict[str, typing.Any]:
    query = """
        mutation ($input:CreateCommitOnBranchInput!) {
            createCommitOnBranch(input: $input) {
                commit { oid }
            }
        }
    """

    return {
        "query": " ".join(query.split()),
        "variables": {
            "input": {
                "branch": {
                    "branchName": inject_version(os.environ["BRANCH_NAME"]),
                    "repositoryNameWithOwner": os.environ["GITHUB_REPOSITORY"],
                },
                "expectedHeadOid": os.environ["GITHUB_SHA"],
                "fileChanges": file_changes,
                "message": {
                    "headline": inject_version(os.environ["COMMIT_TITLE"]),
                },
            },
        },
    }


def inject_version(text: str) -> str:
    version = os.getenv("VERSION") or "VERSION_NOT_FOUND"
    return re.sub(r"\$version", version, text, flags=re.I)


def calculate_file_changes() -> dict[str, list[dict[str, str]]]:
    cmd = "git status --no-renames --porcelain"

    additions: list[dict[str, str]] = []
    deletions: list[dict[str, str]] = []

    for line in subprocess.check_output(cmd.split()).decode().splitlines():
        path = pathlib.Path(line[3:])

        target = deletions
        info = {"path": path.as_posix()}
        if path.is_file():
            target = additions
            info["contents"] = base64.b64encode(path.read_bytes()).decode()
        target.append(info)

    file_changes = {}
    if additions:
        file_changes["additions"] = additions
    if deletions:
        file_changes["deletions"] = deletions
    return file_changes


if __name__ == "__main__":
    sys.exit(main())
