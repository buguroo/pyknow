"""
Tests with callables
"""

import pytest


@pytest.mark.wip
def test_and_match():
    import pyknow.rete.network.callables as callables
    assert callables.and_match(set(["foo", 1]), set(["foo", 1]))
    assert not callables.and_match(set(["foo", 1]), set(["foo", 2]))
    assert callables.and_match(set(), set(["foo", 1]))
    assert not callables.and_match(set(["foo", 1]), set())
    assert not callables.and_match(set(["foo", 1]), set(["bar", 1]))


@pytest.mark.wip
def test_match_W():
    import pyknow.rete.network.callables as callables
    matcher = callables.match_W("foo", True)
    assert matcher({"foo": 1})
    assert not matcher({"bar": 1})
    matcher = callables.match_W("foo", False)
    assert not matcher({"foo": 1})
    assert matcher({"bar": 1})


@pytest.mark.wip
def test_match_V():
    import pyknow.rete.network.callables as callables
    matcher = callables.match_V("foo", "bar")
    assert matcher({"foo": "bar"}) == {"bar": "bar"}

    matcher = callables.match_V("foo", "bar")
    assert matcher({"bar": "bar"}) == {}


@pytest.mark.wip
def test_match_T():
    import pyknow.rete.network.callables as callables
    matcher = callables.match_T("foo", lambda x: x.startswith("foo"))
    assert not matcher({"foo": "bar"})
    assert matcher({"foo": "foobar"})


@pytest.mark.wip
def test_match_L():
    import pyknow.rete.network.callables as callables
    matcher = callables.match_L("foo", "bar")
    assert not matcher({"foo": "barbar"})
    assert matcher({"foo": "bar"})


@pytest.mark.wip
def test_has_key():
    import pyknow.rete.network.callables as callables
    matcher = callables.match_L("foo", "bar")
    assert not matcher({"foo": "barbar"})
    assert matcher({"foo": "bar"})


@pytest.mark.wip
def test_same_class():
    import pyknow.rete.network.callables as callables

    class ParentClass:
        pass

    class ChildClass(ParentClass):
        pass

    matcher = callables.same_class(ParentClass())
    assert matcher(ParentClass())
    assert not matcher(ChildClass())
    assert not matcher(False)


@pytest.mark.wip
def test_compatible_facts():
    import pyknow.rete.network.callables as callables
    matcher = callables.compatible_facts({"foo": "bar", "bar": "baz"})
    assert not matcher({"foo": "bar"})
    assert matcher({"foo": "bar", "bar": "baz", "stuff": "qu"})
    assert matcher({"foo": "bar", "bar": "baz"})


@pytest.mark.wip
def test_get_callable():
    from pyknow.rete.network import get_callable
    from pyknow.fact import W, T, V

    def _get_func_name(method):
        return method.__repr__().split('.')[0].split(' ')[1].strip()

    assert _get_func_name(get_callable("foo", T(lambda x: x))) == "match_T"
    assert _get_func_name(get_callable("foo", V("foo"))) == "match_V"
    assert _get_func_name(get_callable("foo", W(True))) == "match_W"
    assert _get_func_name(get_callable("foo", "foo")) == "match_L"
    assert _get_func_name(get_callable("foo", 1)) == "match_L"
    assert _get_func_name(get_callable("foo", False)) == "match_L"
