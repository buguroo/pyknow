import pytest
from hypothesis import given

from conftest import random_types


def test_Rule_get_activations_exists():
    from pyknow.rule import Rule

    assert hasattr(Rule, 'get_activations')


@given(data=random_types)
def test_Rule_get_activations_needs_factlist(data):
    from pyknow.rule import Rule

    r = Rule()

    with pytest.raises(ValueError):
        r.get_activations(data)


def test_Rule_empty_dont_match_empty_factlist():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    r = Rule()
    fl = FactList()

    assert r.get_activations(fl) == []
