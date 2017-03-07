import pytest

from pyknow.abstract import AbstractMatcher


@pytest.mark.wip
def test_retematcher_exists():
    try:
        from pyknow.rete import ReteMatcher
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_retematcher_is_matcher():
    from pyknow.rete import ReteMatcher

    assert issubclass(ReteMatcher, AbstractMatcher)


@pytest.mark.wip
def test_retematcher_is_not_abstract():
    from pyknow.rete import ReteMatcher
    from pyknow.engine import KnowledgeEngine

    # MUST NOT RAISE
    ReteMatcher(KnowledgeEngine())


@pytest.mark.wip
def test_retematcher_has_root_node():
    from pyknow.rete import ReteMatcher
    from pyknow.engine import KnowledgeEngine
    from pyknow.rete.nodes import BusNode

    matcher = ReteMatcher(KnowledgeEngine())
    assert hasattr(matcher, 'root_node')
    assert isinstance(matcher.root_node, BusNode)


#
# TODO (@dfrancos) walking into the engine building the network
#
