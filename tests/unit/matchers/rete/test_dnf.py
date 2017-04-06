"""
Tests on Rule DNF
"""
import pytest


def test_or_inside_and():
    from pyknow import Fact, Rule, AND, OR
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(AND(Fact(a=1), OR(Fact(a=2), Fact(a=3))))
    output = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=1), Fact(a=3))))
    assert dnf(input_[0]) == output[0]


def test_and_inside_or():
    from pyknow import Fact, Rule, AND, OR
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=3), Fact(a=4))))
    output = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=3), Fact(a=4))))
    assert dnf(input_[0]) == output[0]


def test_and_inside_and():
    from pyknow import Fact, Rule, AND
    from pyknow.matchers.rete.dnf import dnf

    input_ = AND(Fact(a=1), AND(Fact(a=3), Fact(a=4)))
    output = AND(Fact(a=1), Fact(a=3), Fact(a=4))
    assert dnf(input_) == output


def test_or_inside_or():
    from pyknow import Fact, Rule, OR
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(OR(Fact(a=1), OR(Fact(a=3), Fact(a=4))))
    output = Rule(OR(Fact(a=1), Fact(a=3), Fact(a=4)))
    assert dnf(input_) == output


def test_or_and_fact_inside_or():
    from pyknow import Fact, OR, Rule
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(OR(Fact(a=1), OR(Fact(a=2), Fact(a=3))))
    output = Rule(OR(Fact(a=1), Fact(a=2), Fact(a=3)))
    assert dnf(input_) == output


def test_or_inside_or_inside_and():
    from pyknow import Fact, OR, AND, Rule
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(AND(Fact(b=1), OR(Fact(a=1), OR(Fact(a=3), Fact(a=4)))))
    output = Rule(OR(AND(Fact(b=1), Fact(a=1)),
                     AND(Fact(b=1), Fact(a=3)),
                     AND(Fact(b=1), Fact(a=4))))
    result = dnf(input_)
    assert result == output


def test_and_inside_rule():
    from pyknow import Fact, Rule, AND
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=1), AND(Fact(b=2), Fact(c=3)))
    output = Rule(Fact(a=1), Fact(b=2), Fact(c=3))

    result = dnf(input_)
    assert result == output


def test_or_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) | L(2),
                       b=3))
    output = Rule(OR(Fact(a=L(1), b=3),
                     Fact(a=L(2), b=3)))

    result = dnf(input_)
    assert set(result[0]) == set(output[0])


def test_multiple_or_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) | L(2),
                       b=L(3) | L(4)))
    output = Rule(OR(Fact(a=L(1), b=L(3)),
                     Fact(a=L(1), b=L(4)),
                     Fact(a=L(2), b=L(3)),
                     Fact(a=L(2), b=L(4))))

    result = dnf(input_)
    assert set(result[0]) == set(output[0])


def test_double_not_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=~~L(1)))
    output = Rule(Fact(a=L(1)))

    result = dnf(input_)
    assert result == output


def test_not_and_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=~(L(1) & L(2))))
    output = Rule(OR(Fact(a=~L(1)), Fact(a=~L(2))))

    result = dnf(input_)
    assert result == output


def test_not_or_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.fieldconstraint import ANDFC, NOTFC
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=~(L(1) | L(2))))
    output = Rule(Fact(a=ANDFC(NOTFC(L(1)),
                                NOTFC(L(2)))))

    result = dnf(input_)
    assert result == output


def test_and_inside_and_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.fieldconstraint import ANDFC
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) & (L(2) & L(3))))
    output = Rule(Fact(a=ANDFC(L(1), L(2), L(3))))

    result = dnf(input_)
    assert result == output


def test_or_inside_or_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) | (L(2) | L(3))))
    output = Rule(OR(Fact(a=L(1)),
                     Fact(a=L(2)),
                     Fact(a=L(3))))

    result = dnf(input_)
    assert result == output


def test_or_inside_and_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.fieldconstraint import ANDFC
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) & (L(2) | L(3))))
    output = Rule(OR(Fact(a=ANDFC(L(1), L(2))),
                     Fact(a=ANDFC(L(1), L(3)))))

    result = dnf(input_)
    assert result == output


def test_and_inside_or_inside_fact():
    from pyknow import Fact, OR, Rule, L
    from pyknow.fieldconstraint import ANDFC
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=L(1) | (L(2) & L(3))))
    output = Rule(OR(Fact(a=L(1)),
                     Fact(a=ANDFC(L(2), L(3)))))

    result = dnf(input_)
    assert result == output


def test_multiple_or_inside_rule():
    from pyknow import Fact, OR, Rule, AND
    from pyknow.matchers.rete.dnf import dnf

    input_ = Rule(Fact(a=1),
                  OR(Fact(b=1),
                     Fact(b=2)),
                  OR(Fact(c=1),
                     Fact(c=2)))
    output_ = Rule(OR(AND(Fact(a=1), Fact(b=1), Fact(c=1)),
                      AND(Fact(a=1), Fact(b=1), Fact(c=2)),
                      AND(Fact(a=1), Fact(b=2), Fact(c=1)),
                      AND(Fact(a=1), Fact(b=2), Fact(c=2))))

    result = dnf(input_)
    assert result == output_
