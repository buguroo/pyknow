import pytest


def test_KnowledgeEngine_reset_resets_agenda():
    """
        Given a set of fixed facts, they're still there
        after a reset.
        Also, we have in account that InitialFact() is always there.
        And that if we add a normal fact after that, it's not persistent
    """

    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import Fact, L

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.deffacts(Fact(foo=L(1), bar=L(2)))
    ke.reset()

    assert len(ke._facts._facts) == 3

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.declare(Fact(foo=L(9)))
    ke.deffacts(Fact(foo=L(1), bar=L(2)))
    ke.reset()

    assert len(ke._facts._facts) == 3

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.declare(Fact(foo=L(9)))
    ke.reset()

    assert len(ke._facts._facts) == 2
