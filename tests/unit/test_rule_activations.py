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


def test_Rule_empty_doesnt_match_empty_factlist():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    r = Rule()
    fl = FactList()

    assert r.get_activations(fl) == tuple()


def test_Rule_empty_matches_with_initial_fact():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import InitialFact
    from pyknow.activation import Activation

    r = Rule()
    fl = FactList()
    idx = fl.declare(InitialFact())

    assert Activation(r, (0,)) in r.get_activations(fl)


def test_Rule_with_empty_Fact_matches_all_Facts():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L
    from pyknow.activation import Activation

    r = Rule(Fact())
    fl = FactList()

    fl.declare(Fact(something=L(True)))
    fl.declare(Fact(something=L(False)))
    fl.declare(Fact(something=L(3)))

    activations = r.get_activations(fl)
    assert len(activations) == 3
    for i in range(3):
        assert Activation(r, (i, )) in activations


def test_Rule_multiple_criteria_generates_activation_with_matching_facts():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r = Rule(Fact(a=L(1)), Fact(b=L(2)))
    fl = FactList()
    fl.declare(Fact(a=L(1)))
    fl.declare(Fact(b=L(2)))

    activations = r.get_activations(fl)
    assert len(activations) == 1
    assert {0, 1} == set(activations[0].facts)
