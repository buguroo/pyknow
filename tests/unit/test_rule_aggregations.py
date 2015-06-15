import pytest


def test_Rule_nesting():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact

    r1 = Rule(Fact(a=1),
              Fact(b=2),
              Fact(c=3))
    r2 = Rule(Fact(a=1),
              Rule(Fact(b=2),
                   Fact(c=3)))
    r3 = Rule(Fact(a=1),
              Rule(Fact(b=2),
                   Rule(Fact(c=3))))
    r4 = Rule(Rule(Fact(a=1)),
              Rule(Fact(b=2)),
              Rule(Fact(c=3)))
    r5 = Rule(Rule(Fact(a=1),
                   Fact(b=2),
                   Fact(c=3)))
              
    fl = FactList()
    fl.declare(Fact(a=1))
    fl.declare(Fact(b=2))
    fl.declare(Fact(c=3))

    for r in (r1, r2, r3, r4, r5):
        activations = r.get_activations(fl)
        assert len(activations) == 1
        assert {0, 1, 2} == set(activations[0].facts)


def test_Rule_and_NOT_nesting():
    from pyknow.rule import Rule, NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact

    r = Rule(Fact(a=1),
             NOT(Fact(b=2)))
    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=1))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    assert {0, 1} == set(activations[0].facts)


def test_Rule_with_only_one_NOT_doesnt_match_if_fact_is_present():
    from pyknow.rule import NOT, Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact

    r = Rule(NOT(Fact(something=True)))
    fl = FactList()
    fl.declare(Fact(something=True))

    assert not r.get_activations(fl)


def test_Rule_with_only_one_NOT_match_InitialFact_if_fact_is_not_present():
    from pyknow.rule import NOT, Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact

    r = Rule(NOT(Fact(something=True)))
    fl = FactList()
    fl.declare(InitialFact())

    assert r.get_activations(fl)


def test_Rule_with_NOT_DEFINED():
    from pyknow.rule import Rule, NOT
    from pyknow.factlist import FactList
    from pyknow.fact import FactState as fs
    from pyknow.fact import Fact, InitialFact

    r = Rule(Fact(a=1),
             NOT(Fact(b=fs.DEFINED)))

    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=1))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    fl.declare(Fact(b='SOMETHING'))
    activations = r.get_activations(fl)
    assert len(activations) == 0

