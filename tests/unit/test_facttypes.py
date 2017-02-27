"""
Tests related to Fact's Facttypes.
"""
from hypothesis import given, assume
from conftest import random_kwargs

# pylint: disable=invalid-name, missing-docstring


@given(kwargs=random_kwargs)
def test_match_if_all_defined_is_present(kwargs):
    from pyknow.fact import Fact, L
    kwargs['ATLEAST1'] = 'VALUE'
    kwsuperset = kwargs.copy()
    kwsuperset.update({'OTHER1': 'VALUE'})

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(**{a: L(b) for a, b in kwsuperset.items()})

    assert not f1.matches(f0, {})
    assert f0.matches(f1, {})


@given(kwargs=random_kwargs)
def test_match_with_W_False(kwargs):
    assume('something' not in kwargs)

    from pyknow.fact import Fact, W, L

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(something=W(True))

    assert not f1.matches(f0, {})


@given(kwargs=random_kwargs)
def test_match_with_W_True(kwargs):
    assume('something' not in kwargs)

    from pyknow.fact import Fact, W, L

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(something=W(False))

    assert f1.matches(f0, {})


def test_facts_are_equal():
    """ We may need to use EQUAL facts that are not the same object but has
        the same values """

    from pyknow.fact import Fact, C, L

    assert Fact(a=L("foo")) == Fact(a=L("foo"))
    assert Fact(a=L("foo"), b=C("bar")) == Fact(a=L("foo"), b=C("bar"))


def test_T_resolve():
    """ Test T Resolve """
    from pyknow.fact import Fact, T, L
    assert T(lambda c, x: x).resolve(Fact(foo=L("foo")), "foo", {}) == "foo"


def test_N_resolve():
    """ Test N Resolve """
    from pyknow.fact import Fact, N, L
    key = "key_test"
    context = {key: True}
    not_fact = N(key)
    against_fact = Fact(**{key: L(False)})
    assert not_fact.resolve(against_fact, key, context)


def test_C_resolve():
    """ Test C Resolve """
    from pyknow.fact import C
    assert C('foo').resolve() == 'foo'


def test_V_resolve():
    """ Test V Resolve """
    from pyknow.fact import Fact, V, L
    key = "key_test"
    context = {key: True}
    not_fact = V(key)
    against_fact = Fact(**{key: L(True)})
    assert not_fact.resolve(against_fact, key, context)


def test_L_resolve():
    """ Test N Resolve """
    from pyknow.fact import L
    assert L('foo').resolve() == 'foo'
