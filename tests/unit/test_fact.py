"""
Fact methods
"""

import pytest
from hypothesis import given
from conftest import random_kwargs
# pylint: disable=invalid-name


@pytest.mark.parametrize("facttype", ("L", "T", "V", "W"))
@given(kwargs=random_kwargs)
def test_fact_attributes(facttype, kwargs):
    """ Empty fact matches against all. InitialFact should be this case """
    import pyknow.fact
    fact = pyknow.fact.Fact(
        **{a: getattr(pyknow.fact, facttype)(b) for a, b in kwargs.items()})
    print(fact)

    for kwarg, kwvalue in kwargs.items():
        assert getattr(fact, kwarg) == getattr(pyknow.fact, facttype)(kwvalue)
