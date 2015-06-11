import pytest


def test_NOT_exists():
    from pyknow import rule

    assert hasattr(rule, 'NOT')


def test_NOT_is_subclass_of_Rule():
    from pyknow.rule import NOT, Rule

    assert issubclass(NOT, Rule)


def test_NOT_doesnt_match_if_fact_is_present():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact

    r = NOT(Fact(something=True))
    fl = FactList()
    fl.declare(Fact(something=True))

    assert not r.get_activations(fl)


def test_NOT_match_InitialFact_if_fact_is_not_present():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact

    r = NOT(Fact(something=True))
    fl = FactList()
    fl.declare(InitialFact())

    assert r.get_activations(fl)


def test_NOT_doesnt_match_if_fact_is_not_present_and_InitialFact_neither():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact

    r = NOT(Fact(something=True))
    fl = FactList()
    assert not r.get_activations(fl)
