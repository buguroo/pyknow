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
    from pyknow.rete.token import Token
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())

    csn.activate(Token.valid(Fact(test='data'),
                             {'mycontextdata': 'data'}))

    assert ({Fact(test='data')}, {'mycontextdata': 'data'}) in csn.memory


@pytest.mark.wip
def test_conflictsetchange_invalid_removes_from_memory():
    from pyknow.fact import Fact
    from pyknow.rete.nodes import ConflictSetNode
    from pyknow.rete.token import Token
    from pyknow.rule import Rule

    csn = ConflictSetNode(Rule())
    csn.memory.append(({Fact(test='data')}, {'mycontextdata': 'data'}))

    csn.activate(Token.invalid(Fact(test='data'),
                               {'mycontextdata': 'data'}))

    assert not csn.memory
