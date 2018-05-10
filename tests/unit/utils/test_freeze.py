import pytest

from pyknow.utils import freeze, unfreeze, frozenlist, frozendict


def test_freeze_hashable():
    test_frozenset = frozenset({1, 2, 3})
    assert freeze(test_frozenset) == test_frozenset

    test_tuple = (1, 2, 3)
    assert freeze(test_tuple) == test_tuple

    test_frozendict = frozendict({"a": 1, "b": 2})
    assert freeze(test_frozendict) == test_frozendict


def test_freezedicts():
    actual = freeze({"a": 1, "b": 2})
    expected = frozendict({"a": 1, "b": 2})
    assert actual == expected
    assert isinstance(actual, type(expected))


def test_freezelist():
    actual = freeze([1, 2, 3])
    expected = frozenlist([1, 2, 3])
    assert actual == expected
    assert isinstance(actual, type(expected))


def test_freezeset():
    actual = freeze({1, 2, 3})
    expected = frozenset({1, 2, 3})
    assert actual == expected
    assert isinstance(actual, type(expected))


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


def test_unfreeze_frozendict():
    actual = unfreeze(frozendict({"a": 1, "b": 2}))
    expected = {"a": 1, "b": 2}
    assert actual == expected
    assert isinstance(actual, type(expected))


def test_unfreeze_frozenlist():
    actual = unfreeze(frozenlist([1, 2, 3]))
    expected = [1, 2, 3]
    assert actual == expected
    assert isinstance(actual, type(expected))


def test_unfreeze_frozenset():
    actual = unfreeze(frozenset({1, 2, 3}))
    expected = {1, 2, 3}
    assert actual == expected
    assert isinstance(actual, type(expected))
