from typing import NamedTuple


class Employee(NamedTuple):
    name: str
    id: int


def test_instantiate_with_dict():
    """You can unpack a dict to insert named fields into a NamedTuple constructor"""
    bob = Employee(**{"name": "Bob", "id": 123})
    assert bob == Employee(name="Bob", id=123)
