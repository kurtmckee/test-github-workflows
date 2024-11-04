import itertools
import json
import pathlib
import re

import jsonschema
import pytest


@pytest.fixture(scope="session")
def tox_schema():
    tox_schema_path = pathlib.Path(__file__).parent.parent / "src/tox-schema.json"
    tox_schema = json.loads(tox_schema_path.read_text())
    yield jsonschema.Draft7Validator(schema=tox_schema)


def test_require_a_python_interpreter(tox_schema):
    msg = "At least one Python interpreter must be present."
    with pytest.raises(jsonschema.ValidationError, match=msg):
        tox_schema.validate({"runner": "ubuntu-latest"})


@pytest.mark.parametrize("pop_key_1", ("cpythons", "cpython-beta", "pypys", None))
@pytest.mark.parametrize("pop_key_2", ("cpythons", "cpython-beta", "pypys", None))
def test_allow_python_interpreter_combinations(tox_schema, pop_key_1, pop_key_2):
    """Verify any combination of Python interpreter keys is valid.

    This tests combinations of between 1 and 3 total keys.
    """

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
    }
    if pop_key_1 in config:
        config.pop(pop_key_1)
    if pop_key_2 in config:
        config.pop(pop_key_2)
    tox_schema.validate(config)


def test_tox_environments_not_required(tox_schema):
    tox_schema.validate({"runner": "ubuntu-latest", "cpythons": ["3.12"]})


def test_tox_environments(tox_schema):
    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "tox-environments": ["py3.12"],
    }
    tox_schema.validate(config)


@pytest.mark.parametrize(
    "pop_key", ("tox-pre-environments", "tox-post-environments", None)
)
def test_allow_tox_pre_post_environments(tox_schema, pop_key):
    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "tox-pre-environments": ["pre"],
        "tox-post-environments": ["post"],
    }
    if pop_key in config:
        config.pop(pop_key)
    tox_schema.validate(config)


mutex_keys = (
    "tox-environments-from-pythons",
    "tox-pre-environments",
    "tox-post-environments",
)
all_mutex_combinations = itertools.chain(
    *[itertools.combinations(mutex_keys, r=r) for r in range(len(mutex_keys))]
)


@pytest.mark.parametrize("pop_keys", all_mutex_combinations)
def test_tox_environments_mutex(tox_schema, pop_keys):
    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "tox-environments": ["in"],
        "tox-environments-from-pythons": True,
        "tox-pre-environments": ["pre"],
        "tox-post-environments": ["post"],
    }
    for pop_key in pop_keys:
        config.pop(pop_key)
    msg = "tox-environments is mutually exclusive"
    with pytest.raises(jsonschema.ValidationError, match=msg):
        tox_schema.validate(config)


def test_tox_environments_from_pythons_false(tox_schema):
    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "tox-environments-from-pythons": False,
    }
    msg = re.escape("False is not one of [True]")
    with pytest.raises(jsonschema.ValidationError, match=msg):
        tox_schema.validate(config)


def test_full_config(tox_schema):
    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
        "tox-environments-from-pythons": True,
        "tox-pre-environments": ["spin-up"],
        "tox-post-environments": ["spin-down"],
        "cache-key-prefix": "lint",
        "cache-key-hash-files": ["mypy.ini", "requirements/*/requirements.txt"],
        "cache-key-paths": [".mypy_cache"],
    }
    tox_schema.validate(config)
