import pytest


def test_Rule_nesting():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact

    r = Rule(Fact(a=1),
             Rule(Fact(b=2),
                  Fact(c=3),
                  Rule(Fact(d=4))))
    fl = FactList()
    fl.declare(Fact(a=1))
    fl.declare(Fact(b=2))
    fl.declare(Fact(c=3))
    fl.declare(Fact(d=4))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    assert {0, 1, 2, 3} == set(activations[0].facts)


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
