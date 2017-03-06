import pytest


@pytest.mark.wip
def test_conflictsetchange_exists():
    try:
        from pyknow.rete.nodes import ConflictSetNode
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_conflictsetchange_is_abstractnode():
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rete.abstract import OneInputNode

    assert issubclass(ConflictSetNode, OneInputNode)


@pytest.mark.wip
def test_conflictsetchange_interface():
    from pyknow.rete.nodes import ConflictSetNode

    assert hasattr(ConflictSetNode, 'get_activations')


@pytest.mark.wip
def test_conflictsetchange_accepts_rule():
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rule import Rule

    # MUST NOT RAISE
    ConflictSetNode(Rule())

    with pytest.raises(TypeError):
        ConflictSetNode('NOTARULE')


@pytest.mark.wip
def test_conflictsetchange_valid_adds_to_memory():
    from pyknow.fact import Fact
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rete.token import Token, TokenInfo
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())

    csn.activate(Token.valid(Fact(test='data'),
                             {'mycontextdata': 'data'}))

    assert TokenInfo([Fact(test='data')],
                     {'mycontextdata': 'data'}) in csn.memory


@pytest.mark.wip
def test_conflictsetchange_invalid_removes_from_memory():
    from pyknow.fact import Fact
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rete.token import Token, TokenInfo
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())
    csn.memory.append(TokenInfo([Fact(test='data')],
                                {'mycontextdata': 'data'}))

    csn.activate(Token.invalid(Fact(test='data'),
                               {'mycontextdata': 'data'}))

    assert not csn.memory


@pytest.mark.wip
def test_conflictsetchange_get_activations_data():
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rete.token import TokenInfo
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.activation import Activation

    rule = Rule()
    csn = ConflictSetNode(rule)
    csn.memory.append(TokenInfo([Fact(first=1)], {'data': 'test'}))

    activations = csn.get_activations()
    assert len(activations) == 1
    assert activations[0].rule is rule
    assert Fact(first=1) in activations[0].facts
    assert activations[0].context == {'data': 'test'}
