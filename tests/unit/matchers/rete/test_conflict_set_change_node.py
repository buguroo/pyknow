import pytest


def test_conflictsetchange_exists():
    try:
        from pyknow.matchers.rete.nodes import ConflictSetNode
    except ImportError as exc:
        assert False, exc


def test_conflictsetchange_is_abstractnode():
    from pyknow.matchers.rete.nodes import ConflictSetNode
    from pyknow.matchers.rete.abstract import OneInputNode

    assert issubclass(ConflictSetNode, OneInputNode)


def test_conflictsetchange_interface():
    from pyknow.matchers.rete.nodes import ConflictSetNode

    assert hasattr(ConflictSetNode, 'get_activations')


def test_conflictsetchange_accepts_rule():
    from pyknow.matchers.rete.nodes import ConflictSetNode
    from pyknow.rule import Rule

    # MUST NOT RAISE
    ConflictSetNode(Rule())

    with pytest.raises(TypeError):
        ConflictSetNode('NOTARULE')


def test_conflictsetchange_valid_adds_to_memory():
    from pyknow.fact import Fact
    from pyknow.matchers.rete.nodes import ConflictSetNode
    from pyknow.matchers.rete.token import Token, TokenInfo
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())

    csn.activate(Token.valid(Fact(__factid__=1, test='data'),
                             {'mycontextdata': 'data'}))

    assert TokenInfo([Fact(__factid__=1, test='data')],
                     {'mycontextdata': 'data'}) in csn.memory


def test_conflictsetchange_invalid_removes_from_memory():
    from pyknow.fact import Fact
    from pyknow.matchers.rete.nodes import ConflictSetNode
    from pyknow.matchers.rete.token import Token, TokenInfo
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())
    csn.memory.append(TokenInfo([Fact(__factid__=1, test='data')],
                                {'mycontextdata': 'data'}))

    csn.activate(Token.invalid(Fact(__factid__=1, test='data'),
                               {'mycontextdata': 'data'}))

    assert not csn.memory


def test_conflictsetchange_get_activations_data():
    from pyknow.matchers.rete.nodes import ConflictSetNode
    from pyknow.matchers.rete.token import Token
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.activation import Activation

    rule = Rule()
    csn = ConflictSetNode(rule)
    csn.activate(Token.valid(Fact(__factid__=1, first=1), {'data': 'test'}))

    added, removed = csn.get_activations()

    assert len(added) == 1
    assert len(removed) == 0

    assert list(added)[0].rule is rule
    assert Fact(__factid__=1, first=1) in list(added)[0].facts
    assert list(added)[0].context == {'data': 'test'}
