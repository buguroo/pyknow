import pytest
from hypothesis import given
from hypothesis import strategies as st

from pyknow.fact import Fact

from conftest import random_kwargs


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
