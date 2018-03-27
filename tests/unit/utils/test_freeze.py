import pytest
from frozendict import frozendict

from pyknow.utils import freeze


def test_freeze_hashable():
    test_frozenset = frozenset({1, 2, 3})
    assert freeze(test_frozenset) is test_frozenset

    test_tuple = (1, 2, 3)
    assert freeze(test_tuple) is test_tuple

    test_frozendict = frozendict({"a": 1, "b": 2})
    assert freeze(test_frozendict) is test_frozendict


def test_freezedicts():
    assert freeze({"a": 1, "b": 2}) == frozendict({"a": 1, "b": 2})


def test_freezelist():
    assert freeze([1, 2, 3]) == (1, 2, 3)


def test_freezeset():
    assert freeze({1, 2, 3}) == frozenset({1, 2, 3})


def test_implement_freeze():
    class MyClass:
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __eq__(self, other):
            """
            Defining __eq__ without defining __hash__ makes this class
            unhashable.

            """
            return self.a == other.a and self.b == other.b

    with pytest.raises(TypeError):
        freeze(MyClass(1, 2))

    @freeze.register(MyClass)
    def _freeze_myclass(obj):
        return (obj.a, obj.b)

    assert freeze(MyClass(1, 2)) == (1, 2)
