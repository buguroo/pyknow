import pytest


def test_InitialFact_exists():
    from pyknow import fact

    assert hasattr(fact, 'InitialFact')


def test_InitialFact_is_Fact():
    from pyknow.fact import Fact, InitialFact

    assert issubclass(InitialFact, Fact)
