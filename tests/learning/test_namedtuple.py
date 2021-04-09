from typing import NamedTuple

import pytest


class Employee(NamedTuple):
    name: str
    id: int


def test_instantiate_with_dict():
    """You can unpack a dict to insert named fields into a NamedTuple constructor"""
    bob = Employee(**{"name": "Bob", "id": 123})
    assert bob == Employee(name="Bob", id=123)


def test_instantiate_with_dict_with_too_many_items():
    with pytest.raises(TypeError):
        Employee(**{"name": "Bob", "id": 123, "extra": "woops"})
