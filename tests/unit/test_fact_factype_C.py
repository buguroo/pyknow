import pytest
from hypothesis import given
from conftest import random_kwargs

"""
    Tests for basic Capture / Value FactTypes
"""


@pytest.mark.wip
@given(kwargs=random_kwargs)
def test_fact_cv_categorized(kwargs):
    """
        Tests a basic capture / value fact rule
    """

    from pyknow.fact import ValValueSet, V, C, L
    from pyknow.fact import CapValueSet
    vval = ValValueSet()
    vval.add("something", V('foo'))
    vval.add("something", C('foo'))
    vval.add("something", L('foo'))
    assert len(vval.value) == 1

    vval = CapValueSet()
    vval.add("something", V('foo'))
    vval.add("something", C('foo'))
    vval.add("something", L('foo'))
    assert len(vval.value) == 1
