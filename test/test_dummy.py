import pytest
from src.extensions.foo import Foo


def test_suma():
    suma = 1 + 1
    assert suma == 2

def test_foo():
    assert Foo().baz() == "Hola Mundo!"
