"""
Tests on Rule DNF
"""

# pylint: disable=missing-docstring


def test_or_inside_and():
    from pyknow.rule import Rule, AND, OR
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(AND(Fact(a=1), OR(Fact(a=2), Fact(a=3))))
    output = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=1), Fact(a=3))))
    assert dnf(input_[0]) == output[0]


def test_and_inside_or():
    from pyknow.rule import Rule, AND, OR
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=3), Fact(a=4))))
    output = Rule(OR(AND(Fact(a=1), Fact(a=2)), AND(Fact(a=3), Fact(a=4))))
    assert dnf(input_[0]) == output[0]


def test_and_inside_and():
    from pyknow.rule import Rule, AND
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(AND(Fact(a=1), AND(Fact(a=3), Fact(a=4))))
    output = Rule(AND(Fact(a=1), Fact(a=3), Fact(a=4)))
    assert dnf(input_) == output


def test_or_inside_or():
    from pyknow.rule import Rule, OR
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(OR(Fact(a=1), OR(Fact(a=3), Fact(a=4))))
    output = Rule(OR(Fact(a=1), Fact(a=3), Fact(a=4)))
    assert dnf(input_) == output


def test_or_and_fact_inside_or():
    from pyknow.rule import OR, Rule
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(OR(Fact(a=1), OR(Fact(a=2), Fact(a=3))))
    output = Rule(OR(Fact(a=1), Fact(a=2), Fact(a=3)))
    assert dnf(input_) == output


def test_or_inside_or_inside_and():
    from pyknow.rule import OR, AND, Rule
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(AND(Fact(b=1), OR(Fact(a=1), OR(Fact(a=3), Fact(a=4)))))
    output = Rule(OR(AND(Fact(b=1), Fact(a=1)),
                     AND(Fact(b=1), Fact(a=3)),
                     AND(Fact(b=1), Fact(a=4))))
    result = dnf(input_)
    assert result == output
