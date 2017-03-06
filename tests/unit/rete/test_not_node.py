import pytest


@pytest.mark.wip
def test_notnode_exists():
    try:
        from pyknow.rete.nodes import NotNode
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_notnode_is_abstractnode():
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.abstract import TwoInputNode

    assert issubclass(NotNode, TwoInputNode)


@pytest.mark.wip
def test_notnode_accepts_callable():
    from pyknow.rete.nodes import NotNode

    # MUST NOT RAISE
    NotNode(lambda l, r: True)

    with pytest.raises(TypeError):
        NotNode('NONCALLABLE')


@pytest.mark.wip
def test_notnode_left_activate_valid_empty_right(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))
    nn.activate_left(token)

    assert tn1.added == [token]
    assert tn2.added == [token]
    assert nn.left_memory[token.to_info()] == 0


@pytest.mark.wip
def test_notnode_left_activate_valid_non_matching(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: False)
    nn.right_memory.append(Token.valid(Fact(test='data1')).to_info())
    nn.right_memory.append(Token.valid(Fact(test='data2')).to_info())

    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))
    nn.activate_left(token)

    assert tn1.added == [token]
    assert tn2.added == [token]
    assert nn.left_memory[token.to_info()] == 0


@pytest.mark.wip
def test_notnode_left_activate_valid_matching(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    nn.right_memory.append(Token.valid(Fact(test='data')).to_info())

    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))
    nn.activate_left(token)

    assert not tn1.added
    assert not tn2.added
    assert nn.left_memory[token.to_info()] == 1


@pytest.mark.wip
def test_notnode_right_activate_valid_empty(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))
    nn.activate_right(token)

    assert not tn1.added
    assert not tn2.added
    assert token.to_info() in nn.right_memory


@pytest.mark.wip
def test_notnode_right_activate_invalid_match_more_than_one(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.invalid(Fact(test='data'))

    nn.left_memory[token.to_info()] = 2

    nn.activate_right(token)

    assert not tn1.added
    assert not tn2.added
    assert nn.left_memory[token.to_info()] == 1


@pytest.mark.wip
def test_notnode_right_activate_invalid_match_just_one(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.invalid(Fact(test='data'))

    nn.left_memory[token.to_info()] = 1

    nn.activate_right(token)

    assert Token.valid(Fact(test='data')) in tn1.added
    assert Token.valid(Fact(test='data')) in tn2.added
    assert nn.left_memory[token.to_info()] == 0


@pytest.mark.wip
def test_notnode_right_activate_valid_match_more_than_one(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))

    nn.left_memory[token.to_info()] = -1

    nn.activate_right(token)

    assert not tn1.added
    assert not tn2.added
    assert nn.left_memory[token.to_info()] == 0


@pytest.mark.wip
def test_notnode_right_activate_valid_match_just_one(TestNode):
    from pyknow.rete.nodes import NotNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    nn = NotNode(lambda l, r: True)
    tn1 = TestNode()
    tn2 = TestNode()

    nn.add_child(tn1, tn1.activate)
    nn.add_child(tn2, tn2.activate)

    token = Token.valid(Fact(test='data'))

    nn.left_memory[token.to_info()] = 0

    nn.activate_right(token)

    assert Token.invalid(Fact(test='data')) in tn1.added
    assert Token.invalid(Fact(test='data')) in tn2.added
    assert nn.left_memory[token.to_info()] == 1
