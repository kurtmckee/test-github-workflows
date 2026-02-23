# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import functools
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
PRE_COMMIT_CONFIG = ROOT / ".pre-commit-config.yaml"


def main() -> None:
    """Rewrite "additional_dependencies" in the pre-commit config."""

    config = PRE_COMMIT_CONFIG.read_text()

    lines = []
    iterable = iter(config.splitlines())
    for line in iterable:
        lines.append(line)
        if not line.lstrip().startswith("# additional_dependencies source:"):
            continue

        target_requirements_file = line.partition(":")[2].strip()
        indent = len(line) - len(line.lstrip())

        # Consume all list lines under the comment.
        # The last line that isn't a list line (if any) is kept for later use.
        try:
            while (next_line := next(iterable)).startswith(f"{' ' * indent}-"):
                pass
        except StopIteration:
            next_line = None

        for requirement in get_contents(target_requirements_file).splitlines():
            lines.append(f"{' ' * indent}- '{requirement}'")

        if next_line is not None:
            lines.append(next_line)

    new_config = "\n".join(lines) + "\n"
    if new_config != config:
        PRE_COMMIT_CONFIG.write_text(new_config)


@functools.cache
def get_contents(path: str) -> str:
    return (ROOT / path).read_text()


if __name__ == "__main__":
    main()
