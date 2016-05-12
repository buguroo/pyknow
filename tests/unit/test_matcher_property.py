import pytest


def test_matcher_property():
    """
        That that, when a Fact has a property that is
        not a literal, is considered a matcher

    """
    from pyknow.fact import Fact, C, L, V, T

    assert Fact(a=C("foo")).is_matcher
    assert not Fact(a=L("foo")).is_matcher
    assert Fact(a=V("foo")).is_matcher
    assert Fact(a=T("foo")).is_matcher


def test_cannot_directly_declare_matchers():
    """
        Test that, when a fact is a matcher, cannot be directly
        declared in a KnowledgeEngine
    """
    from pyknow.fact import Fact, C, L, V, T
    from pyknow.engine import KnowledgeEngine

    ke_ = KnowledgeEngine()
    with pytest.raises(TypeError):
        ke_.declare(Fact(a=C('foo')))

    with pytest.raises(TypeError):
        ke_.declare(Fact(a=T('foo')))

    with pytest.raises(TypeError):
        ke_.declare(Fact(a=V('foo')))

    ke_.declare(Fact(a=L('foo')))
    assert ke_._facts
