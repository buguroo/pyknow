import pytest
from hypothesis import given, assume
from hypothesis import strategies as st

from pyknow.fact import Fact

from conftest import random_kwargs, random_types


def test_same_fact_contain_each_other():
    f0 = Fact(something=True)
    f1 = Fact(something=True)

    assert f0 in f1
    assert f1 in f0


@given(kwargs=random_kwargs)
def test_empty_fact_match_all(kwargs):
    f0 = Fact()
    f1 = Fact(**kwargs)
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

    f0 = Fact(**kwargs)
    f1 = Fact(**kwsuperset)

    assert f0 in f1
    assert f1 not in f0


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

    f0 = Fact(something=value)
    f1 = Fact(something=fs.DEFINED)

    assert f0 in f1


@given(kwargs=random_kwargs)
def test_match_with_FactState_DEFINED_False(kwargs):
    assume(not 'something' in kwargs)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(**kwargs)
    f1 = Fact(something=fs.DEFINED)

    assert f0 not in f1


@given(kwargs=random_kwargs)
def test_match_with_FactState_UNDEFINED_True(kwargs):
    assume(not 'something' in kwargs)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(**kwargs)
    f1 = Fact(something=fs.UNDEFINED)

    assert f0 in f1


@given(value=random_types)
def test_match_with_FactState_UNDEFINED_False(value):
    try:
        hash(value)
    except TypeError:
        assume(False)

    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact

    f0 = Fact(something=value)
    f1 = Fact(something=fs.UNDEFINED)

    assert f0 not in f1
