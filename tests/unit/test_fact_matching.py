import pytest
from hypothesis import given, assume
from hypothesis import strategies as st

from pyknow.fact import Fact, L

from conftest import random_kwargs, random_types


def test_same_fact_contain_each_other():
    f0 = Fact(something=L(True))
    f1 = Fact(something=L(True))

    assert f0 in f1
    assert f1 in f0


@given(kwargs=random_kwargs)
def test_empty_fact_match_all(kwargs):
    f0 = Fact()
    f1 = Fact(**{a: L(b) for a, b in kwargs.items()})
    assert f1 in f0


def test_different_fact_types_do_not_match():
    class FactType0(Fact):
        pass

    class FactType1(Fact):
        pass

    f0 = FactType0()
    f1 = FactType1()

    assert f0 not in f1
    assert f1 not in f0


@given(kwargs=random_kwargs)
def test_match_if_all_defined_is_present(kwargs):
    kwargs['ATLEAST1'] = 'VALUE'
    kwsuperset = kwargs.copy()
    kwsuperset.update({'OTHER1': 'VALUE'})

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(**{a: L(b) for a, b in kwsuperset.items()})

    assert f0 not in f1
    assert f1 in f0


def test_FactState_exists():
    from pyknow import fact

    assert hasattr(fact, 'FactState')


def test_FactState_is_Enum():
    from pyknow.fact import FactState
    import enum

    assert issubclass(FactState, enum.Enum)


def test_FactState_DEFINED():
    from pyknow.fact import FactState

    assert hasattr(FactState, 'DEFINED')


def test_FactState_UNDEFINED():
    from pyknow.fact import FactState

    assert hasattr(FactState, 'UNDEFINED')


@given(value=random_types)
def test_match_with_FactState_DEFINED_True(value):
    try:
        hash(value)
    except TypeError:
        assume(False)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(something=L(value))
    f1 = Fact(something=L(fs.DEFINED))

    assert f0 in f1


@given(kwargs=random_kwargs)
def test_match_with_FactState_DEFINED_False(kwargs):
    assume('something' not in kwargs)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(something=L(fs.DEFINED))

    assert f0 not in f1


@given(kwargs=random_kwargs)
def test_match_with_FactState_UNDEFINED_True(kwargs):
    assume('something' not in kwargs)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(**{a: L(b) for a, b in kwargs.items()})
    f1 = Fact(something=L(fs.UNDEFINED))

    assert f0 in f1


@given(value=random_types)
def test_match_with_FactState_UNDEFINED_False(value):
    try:
        hash(value)
    except TypeError:
        assume(False)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(something=L(value))
    f1 = Fact(something=L(fs.UNDEFINED))

    assert f0 not in f1


def test_match_with_testce():
    from pyknow.fact import Fact, T
    assert Fact(name=L('David')) in Fact(name=T(lambda x: x.startswith('D')))
    assert Fact(name=L('Penelope')) not in Fact(
        name=T(lambda x: x.startswith('D')))


def test_facts_are_equal():
    """ We may need to use EQUAL facts that are not the same object but has
        the same values """

    from pyknow.fact import Fact, C, V, L

    assert Fact(a=L("foo")) == Fact(a=L("foo"))
    assert Fact(a=L("foo"), b=C("bar")) == Fact(a=L("foo"), b=C("bar"))
    assert Fact(a=L("foo"), b=C("bar"), c=V("stuff")
                ) == Fact(a=L("foo"), b=C("bar"), c=V("stuff"))
