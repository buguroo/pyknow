import pytest


@pytest.mark.wip
def test_abstractnode_exists():
    try:
        from pyknow.rete.abstract import AbstractNode
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_abstractnode_is_abstract():
    from pyknow.rete.abstract import AbstractNode

    with pytest.raises(TypeError):
        AbstractNode()
