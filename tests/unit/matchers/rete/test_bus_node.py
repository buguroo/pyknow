import pytest


def test_busnode_exists():
    try:
        from pyknow.matchers.rete.nodes import BusNode
    except ImportError as exc:
        assert False, exc


def test_busnode_is_node():
    from pyknow.matchers.rete.nodes import BusNode
    from pyknow.matchers.rete.abstract import Node

    assert issubclass(BusNode, Node)


def test_busnode_interface():
    from pyknow.matchers.rete.nodes import BusNode

    assert hasattr(BusNode, 'add')
    assert hasattr(BusNode, 'remove')


def test_busnode_add_child(TestNode):
    from pyknow.matchers.rete.nodes import BusNode
    from pyknow.fact import Fact

    bn = BusNode()
    tn = TestNode()

    bn.add_child(tn, tn.activate)
    assert list(bn.children)[0].node is tn


def test_busnode_add(TestNode):
    from pyknow.matchers.rete.nodes import BusNode
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    bn = BusNode()
    tn1 = TestNode()
    tn2 = TestNode()

    bn.add_child(tn1, tn1.activate)
    bn.add_child(tn2, tn2.activate)

    bn.add(Fact())

    assert tn1.added == [Token.valid(Fact())]
    assert tn2.added == [Token.valid(Fact())]


def test_busnode_remove(TestNode):
    from pyknow.matchers.rete.nodes import BusNode
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    bn = BusNode()
    tn1 = TestNode()
    tn2 = TestNode()

    bn.add_child(tn1, tn1.activate)
    bn.add_child(tn2, tn2.activate)

    bn.remove(Fact())

    assert tn1.added == [Token.invalid(Fact())]
    assert tn2.added == [Token.invalid(Fact())]
