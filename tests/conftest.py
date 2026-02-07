# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pathlib
import sys

# Add the `src/` directory to the Python path.
src_path = pathlib.Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))
