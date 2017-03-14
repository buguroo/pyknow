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

    input_ = AND(Fact(a=1), AND(Fact(a=3), Fact(a=4)))
    output = AND(Fact(a=1), Fact(a=3), Fact(a=4))
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


def test_and_inside_rule():
    from pyknow.rule import Rule, AND
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=1), AND(Fact(b=2), Fact(c=3)))
    output = Rule(Fact(a=1), Fact(b=2), Fact(c=3))

    result = dnf(input_)
    assert result == output


def test_or_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) | LiteralPCE(2),
                       b=3))
    output = Rule(OR(Fact(a=LiteralPCE(1), b=3),
                     Fact(a=LiteralPCE(2), b=3)))

    result = dnf(input_)
    assert result == output


def test_multiple_or_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) | LiteralPCE(2),
                       b=LiteralPCE(3) | LiteralPCE(4)))
    output = Rule(OR(Fact(a=LiteralPCE(1), b=LiteralPCE(3)),
                     Fact(a=LiteralPCE(1), b=LiteralPCE(4)),
                     Fact(a=LiteralPCE(2), b=LiteralPCE(3)),
                     Fact(a=LiteralPCE(2), b=LiteralPCE(4))))

    result = dnf(input_)
    assert result == output


def test_double_not_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=~~LiteralPCE(1)))
    output = Rule(Fact(a=LiteralPCE(1)))

    result = dnf(input_)
    assert result == output


def test_not_and_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=~(LiteralPCE(1) & LiteralPCE(2))))
    output = Rule(OR(Fact(a=~LiteralPCE(1)), Fact(a=~LiteralPCE(2))))

    result = dnf(input_)
    assert result == output


def test_not_or_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE, ANDPCE, NOTPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=~(LiteralPCE(1) | LiteralPCE(2))))
    output = Rule(Fact(a=ANDPCE(NOTPCE(LiteralPCE(1)),
                                NOTPCE(LiteralPCE(2)))))

    result = dnf(input_)
    assert result == output


def test_and_inside_and_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE, ANDPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) & (LiteralPCE(2) & LiteralPCE(3))))
    output = Rule(Fact(a=ANDPCE(LiteralPCE(1), LiteralPCE(2), LiteralPCE(3))))

    result = dnf(input_)
    assert result == output


def test_or_inside_or_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) | (LiteralPCE(2) | LiteralPCE(3))))
    output = Rule(OR(Fact(a=LiteralPCE(1)),
                     Fact(a=LiteralPCE(2)),
                     Fact(a=LiteralPCE(3))))

    result = dnf(input_)
    assert result == output


def test_or_inside_and_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE, ANDPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) & (LiteralPCE(2) | LiteralPCE(3))))
    output = Rule(OR(Fact(a=ANDPCE(LiteralPCE(1), LiteralPCE(2))),
                     Fact(a=ANDPCE(LiteralPCE(1), LiteralPCE(3)))))

    result = dnf(input_)
    assert result == output


def test_and_inside_or_inside_fact():
    from pyknow.rule import OR, Rule, LiteralPCE, ANDPCE
    from pyknow.fact import Fact
    from pyknow.rete.network.dnf import dnf

    input_ = Rule(Fact(a=LiteralPCE(1) | (LiteralPCE(2) & LiteralPCE(3))))
    output = Rule(OR(Fact(a=LiteralPCE(1)),
                     Fact(a=ANDPCE(LiteralPCE(2), LiteralPCE(3)))))

    result = dnf(input_)
    assert result == output
