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
    from pyknow.fact import Fact, L

    r = NOT(Fact(something=L(True)))
    fl = FactList()
    fl.declare(Fact(something=L(True)))

    assert not r.get_activations(fl)


def test_NOT_match_InitialFact_if_fact_is_not_present():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L

    r = NOT(Fact(something=L(True)))
    fl = FactList()
    fl.declare(InitialFact())

    assert r.get_activations(fl)


def test_NOT_doesnt_match_if_fact_is_not_present_and_InitialFact_neither():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r = NOT(Fact(something=L(True)))
    fl = FactList()
    assert not r.get_activations(fl)


def test_NOT_matches_all_positive_facts_KE():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import NOT
    from pyknow.fact import Fact, L

    class Test(KnowledgeEngine):
        @NOT(Fact(something=L(3)))
        def rule2(self):
            pass

    ke = Test()
    ke.reset()

    ke.declare(Fact(something=L(1)))
    ke.declare(Fact(something=L(2)))

    assert len(ke.agenda.activations) == 1
    ke.run()


def test_NOT_matches_if_fact_does_not_match():
    from pyknow.rule import NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L

    r = NOT(Fact(something=L(1)))

    fl = FactList()
    # Es importante declarar el InitialFact
    fl.declare(InitialFact())
    fl.declare(Fact(something=L(2)))

    assert r.get_activations(fl)
