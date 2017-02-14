import pytest


def test_Rule_nesting_issubclass():
    """
        This actually tests that nesting a Rule is permitted.
        Rule nesting can be useful for meta-stuff, and
    """
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r1 = Rule(Fact(a=L(1)),
              Fact(b=L(2)),
              Fact(c=L(3)))
    r2 = Rule(Fact(a=L(1)),
              Rule(Fact(b=L(2)),
                   Fact(c=L(3))))
    r3 = Rule(Fact(a=L(1)),
              Rule(Fact(b=L(2)),
                   Rule(Fact(c=L(3)))))
    r4 = Rule(Rule(Fact(a=L(1))),
              Rule(Fact(b=L(2))),
              Rule(Fact(c=L(3))))
    r5 = Rule(Rule(Fact(a=L(1)),
                   Fact(b=L(2)),
                   Fact(c=L(3))))

    fl = FactList()
    fl.declare(Fact(a=L(1)))
    fl.declare(Fact(b=L(2)))
    fl.declare(Fact(c=L(3)))

    for r in (r1, r2, r3, r4, r5):
        activations = r.get_activations(fl)
        assert len(activations) == 1
        assert {0, 1, 2} == set(activations[0].facts)


def test_Rule_and_NOT_nesting():
    from pyknow.rule import Rule, NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L

    r = Rule(Fact(a=L(1)),
             NOT(Fact(b=L(2))))
    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=L(1)))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    assert {0, 1} == set(activations[0].facts)


def test_Rule_and_AND_nesting():
    from pyknow.rule import Rule, AND
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r = Rule(AND(Fact(a=L(2)), Fact(b=L(1))))

    fl = FactList()
    fl.declare(Fact(a=L(2)))
    fl.declare(Fact(b=L(1)))

    activations = r.get_activations(fl)
    assert len(activations) == 1
    assert {0, 1} == set(activations[0].facts)


def test_Rule_with_only_one_NOT_doesnt_match_if_fact_is_present():
    from pyknow.rule import NOT, Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r = Rule(NOT(Fact(something=L(True))))
    fl = FactList()
    fl.declare(Fact(something=L(True)))

    assert not r.get_activations(fl)


def test_Rule_with_only_one_NOT_match_InitialFact_if_fact_is_not_present():
    from pyknow.rule import NOT, Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L

    r = Rule(NOT(Fact(something=L(True))))
    fl = FactList()
    fl.declare(InitialFact())

    assert r.get_activations(fl)


def test_Rule_with_NOT_DEFINED():
    from pyknow.rule import Rule, NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L, W

    r = Rule(Fact(a=L(1)),
             NOT(Fact(b=W(True))))

    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=L(1)))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    fl.declare(Fact(b=L('SOMETHING')))
    activations = r.get_activations(fl)
    assert len(activations) == 0


def test_rule_with_NOT_testce():
    from pyknow.rule import Rule, NOT
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, InitialFact, L, T

    r = Rule(Fact(a=L(1)),
             NOT(Fact(b=T(lambda c, x: x.startswith('D')))))

    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=L(1)))

    activations = r.get_activations(fl)
    assert len(activations) == 1

    fl.declare(Fact(b=L('David')))
    activations = r.get_activations(fl)
    assert len(activations) == 0

    fl = FactList()
    fl.declare(InitialFact())
    fl.declare(Fact(a=L(1)))
    fl.declare(Fact(b=L('Penelope')))
    activations = r.get_activations(fl)
    assert len(activations) == 1
