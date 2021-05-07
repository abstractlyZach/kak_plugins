import abc

import pytest


class Animal(abc.ABC):
    @abc.abstractmethod
    def make_sound(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass


def test_abc_raises_error():
    """Woops just an empty class"""

    class EmptyAnimal(Animal):
        pass

    with pytest.raises(TypeError):
        EmptyAnimal()


def test_need_method():
    """You must implement an abstractmethod"""

    class SilentAnimal(Animal):
        @property
        def name(self):
            return "spot"

    with pytest.raises(TypeError):
        SilentAnimal()


def test_needs_a_name():
    """What happens if we don't have a name for the animal?"""

    class NoisyNamelessAnimal(Animal):
        def make_sound(self):
            return "AWOOGA"

    with pytest.raises(TypeError):
        NoisyNamelessAnimal()


def test_defined_all_things():
    """No exception raised"""

    class Dog(Animal):
        def make_sound(self):
            return "woof"

        @property
        def name(self):
            return "dog"

    Dog()


def test_doesnt_implement_property_correctly():
    """Aw man, there's no checking for proper property definitions."""

    class WeirdAnimal(Animal):
        def make_sound(self):
            return "hi there"

        def name(self):
            """I don't have an @property decorator, but I should"""
            return "this is my name"

    weird_animal = WeirdAnimal()
    assert not isinstance(weird_animal.name, str)
