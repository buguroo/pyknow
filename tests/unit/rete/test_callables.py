"""
Tests with callables
"""

import pytest


@pytest.mark.wip
def test_and_match():
    from pyknow.rete.callables import Callables
    assert Callables.and_match({"foo": 1}, {"foo": 1})
    assert not Callables.and_match({"foo": 1}, {"foo": 2})
    assert Callables.and_match({}, {"foo": 1})
    assert not Callables.and_match({"foo": 1}, {})
    assert not Callables.and_match({"foo": 1}, {"bar": 1})


@pytest.mark.wip
def test_match_W():
    from pyknow.rete.callables import Callables
    matcher = Callables.match_W("foo", True)
    assert matcher({"foo": 1})
    assert not matcher({"bar": 1})
    matcher = Callables.match_W("foo", False)
    assert not matcher({"foo": 1})
    assert matcher({"bar": 1})


@pytest.mark.wip
def test_match_V():
    from pyknow.rete.callables import Callables
    matcher = Callables.match_V("foo", "bar")
    assert matcher({"foo": "bar"}) == {"bar": "bar"}

    matcher = Callables.match_V("foo", "bar")
    assert matcher({"bar": "bar"}) == {}


@pytest.mark.wip
def test_match_T():
    from pyknow.rete.callables import Callables
    matcher = Callables.match_T("foo", lambda x: x.startswith("foo"))
    assert not matcher({"foo": "bar"})
    assert matcher({"foo": "foobar"})


@pytest.mark.wip
def test_match_L():
    from pyknow.rete.callables import Callables
    matcher = Callables.match_L("foo", "bar")
    assert not matcher({"foo": "barbar"})
    assert matcher({"foo": "bar"})


@pytest.mark.wip
def test_has_key():
    from pyknow.rete.callables import Callables
    matcher = Callables.match_L("foo", "bar")
    assert not matcher({"foo": "barbar"})
    assert matcher({"foo": "bar"})


@pytest.mark.wip
def test_same_class():
    from pyknow.rete.callables import Callables

    class ParentClass:
        pass

    class ChildClass(ParentClass):
        pass

    matcher = Callables.same_class(ParentClass())
    assert matcher(ParentClass())
    assert not matcher(ChildClass())
    assert not matcher(False)


@pytest.mark.wip
def test_compatible_facts():
    from pyknow.rete.callables import Callables
    matcher = Callables.compatible_facts({"foo": "bar", "bar": "baz"})
    assert not matcher({"foo": "bar"})
    assert matcher({"foo": "bar", "bar": "baz", "stuff": "qu"})
    assert matcher({"foo": "bar", "bar": "baz"})


@pytest.mark.wip
def test_get_callable():
    from pyknow.rete.callables import Callables
    from pyknow.fact import W, T, V

    lambda_func = Callables.get_callable("foo", T(lambda x: x))
    assert lambda_func.__repr__().split('.')[1] == "match_T"

    lambda_func = Callables.get_callable("foo", V("foo"))
    assert lambda_func.__repr__().split('.')[1] == "match_V"

    lambda_func = Callables.get_callable("foo", W(True))
    assert lambda_func.__repr__().split('.')[1] == "match_W"

    lambda_func = Callables.get_callable("foo", "foo")
    assert lambda_func.__repr__().split('.')[1] == "match_L"

    lambda_func = Callables.get_callable("foo", 1)
    assert lambda_func.__repr__().split('.')[1] == "match_L"

    lambda_func = Callables.get_callable("foo", False)
    assert lambda_func.__repr__().split('.')[1] == "match_L"
