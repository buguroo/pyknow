import pytest


@pytest.mark.wip
def test_abstractnodes_exists():
    try:
        from pyknow.matchers.rete.abstract import AbstractNode
        from pyknow.matchers.rete.abstract import OneInputNode
        from pyknow.matchers.rete.abstract import TwoInputNode
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_abstractnode_interface():
    from pyknow.matchers.rete.abstract import AbstractNode

    assert {'_reset', 'add_child'} <= AbstractNode.__abstractmethods__


@pytest.mark.wip
def test_oneinputnode_interface():
    from pyknow.matchers.rete.abstract import OneInputNode

    assert {'_activate'} <= OneInputNode.__abstractmethods__


@pytest.mark.wip
def test_twoinputnode_interface():
    from pyknow.matchers.rete.abstract import TwoInputNode

    assert {'_activate_left',
            '_activate_right'} <= TwoInputNode.__abstractmethods__
