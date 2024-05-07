# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import itertools
import pathlib
import sys
import textwrap

FILE_NOT_MODIFIED = 0
FILE_MODIFIED = 1

ROOT = pathlib.Path(__file__).parent.parent


def main() -> int:
    files_modified = False

    for yaml_file in (ROOT / ".github/workflows").glob("*.yaml"):
        files_modified |= _handle_yaml_file(yaml_file)

    return files_modified


def _handle_yaml_file(yaml_file: pathlib.Path) -> bool:
    file_modified = False

    # Load the YAML file and find content blocks to synchronize.
    # Note that content blocks always have one line of padding on each side.
    # The padding lines are not necessarily blank.
    yaml = yaml_file.read_text()

    index = 0
    while (index := yaml.find("START: ", index)) != -1:
        block_start = yaml.find("\n", index) + 1
        file = ROOT / "src" / yaml[index:block_start].split()[-1]
        end_line = f"END: {file.name}"
        block_end = yaml.rfind("\n", block_start, yaml.find(end_line, block_start))
        destination_contents = yaml[block_start:block_end]
        indent = len(destination_contents) - len(destination_contents.lstrip())

        # Load the file contents and strip leading comments and blank lines.
        source_contents = "\n".join(
            itertools.dropwhile(
                lambda x: x.startswith("#") or not x, file.read_text().splitlines()
            )
        )
        source_contents = textwrap.indent(source_contents, " " * indent)

        # Modify the YAML file contents, if needed.
        if source_contents != destination_contents:
            yaml = yaml[:block_start] + source_contents + yaml[block_end:]
            file_modified = True

        # Update the index.
        index = block_end

    # Write changes back to the YAML file if needed.
    if file_modified:
        yaml_file.write_text(yaml, encoding="utf-8", newline="\n")

    return file_modified


if __name__ == "__main__":
    sys.exit(main())
