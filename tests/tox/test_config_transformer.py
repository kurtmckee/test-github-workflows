# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import re

import pytest

import workflow_assets.tox.config_transformer


def test_tox_pre_post_environments():
    """Verify tox pre- and post- environment keys are transformed."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
        "tox-pre-environments": ["spin-up"],
        "tox-post-environments": ["spin-down"],
        "cache-key-prefix": "lint",
        "cache-key-hash-files": ["mypy.ini", "requirements/*/requirements.txt"],
        "cache-key-paths": [".mypy_cache"],
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert "tox-environments-from-pythons" not in config
    assert "tox-factors" not in config
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "spin-up",
        "py3.12",
        "py3.13",
        "pypy3.10",
        "spin-down",
    ]


def test_tox_environments():
    """Verify explicit tox environments are not transformed."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
        "tox-environments": ["a", "c", "b"],
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert "tox-environments-from-pythons" not in config
    assert "tox-factors" not in config
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "a",
        "c",
        "b",
    ]


def test_tox_pythons_as_environments():
    """Verify Pythons are used to generate a list of tox environments."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.13"],
        "cpython-beta": "3.14",
        "pypys": ["3.10"],
        "tox-environments-from-pythons": True,
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert "tox-environments-from-pythons" not in config
    assert "tox-factors" not in config
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "py3.13",
        "py3.14",
        "pypy3.10",
    ]


def test_tox_factors():
    """Verify factors are only appended to generated tox environment names."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.13"],
        "cpython-beta": "3.14",
        "pypys": ["3.10"],
        "tox-factors": ["a", "b"],
        "tox-pre-environments": ["pre"],
        "tox-post-environments": ["post"],
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert "tox-environments-from-pythons" not in config
    assert "tox-factors" not in config
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "pre",
        "py3.13-a-b",
        "py3.14-a-b",
        "pypy3.10-a-b",
        "post",
    ]


@pytest.mark.parametrize(
    "key, value, expected",
    (
        ("cpython-beta", "3.14", "3.14"),
        ("pypys", ["3.10"], "pypy3.10"),
    ),
)
def test_tox_stable_cpython_injection(key, value, expected):
    """Verify that a stable CPython version is injected."""

    config = {
        "runner": "ubuntu-latest",
        key: value,
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert config["python-versions-requested"] == expected
    assert config["python-versions-required"] == expected + "\n3.13"


def test_tox_stable_cpython_injection_unnecessary():
    """Verify that no stable CPython is injected when stable CPythons are available."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.13"],
    }

    workflow_assets.tox.config_transformer.transform_config(config)
    assert config["python-versions-requested"] == "3.13"
    assert config["python-versions-required"] == "3.13"


@pytest.mark.parametrize(
    "strings, pattern, expected",
    (
        (["x.y.z", "abc"], None, r"abc|x\.y\.z"),
        (None, "mypy-.*", "mypy-.*"),
        (["x.y.z", "abc"], "mypy-.*", r"abc|x\.y\.z|mypy-.*"),
    ),
)
def test_tox_skip_environments(strings, pattern, expected):
    """Verify that skipped environments are sorted, escaped, and combined correctly.

    Note that it is expected that the explicit regex pattern will always be at the end;
    for visibility it is not sorted in with the list of literal environments.
    """

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.13"],
    }
    if strings is not None:
        config["tox-skip-environments"] = strings
    if pattern is not None:
        config["tox-skip-environments-regex"] = pattern

    workflow_assets.tox.config_transformer.transform_config(config)
    assert config["tox-skip-environments-regex"] == expected
    assert re.compile(config["tox-skip-environments-regex"])
