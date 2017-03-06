import pytest


@pytest.mark.wip
def test_featuretesternode_exists():
    try:
        from pyknow.rete.nodes import FeatureTesterNode
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_featuretesternode_is_oneinputnode():
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.abstract import OneInputNode

    assert issubclass(FeatureTesterNode, OneInputNode)


@pytest.mark.wip
def test_featuretesternode_accepts_callable():
    from pyknow.rete.nodes import FeatureTesterNode

    # MUST NOT RAISE
    FeatureTesterNode(lambda x: True)

    with pytest.raises(TypeError):
        FeatureTesterNode('NONCALLABLE')


@pytest.mark.wip
def test_featuretesternode_pass_when_callable_succeed(TestNode):
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: True)
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True))

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    assert tn1.added == tn2.added == [token]


@pytest.mark.wip
def test_featuretesternode_pass_when_callable_fail(TestNode):
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: False)
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True))

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    assert tn1.added == tn2.added == []


@pytest.mark.wip
def test_featuretesternode_pass_when_callable_adds_context(TestNode):
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: {'something': True})
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True))

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    newtoken = token.copy()
    newtoken.context['something'] = True

    assert tn1.added == tn2.added == [newtoken]


@pytest.mark.wip
def test_featuretesternode_pass_when_callable_modify_context(TestNode):
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: {'something': True})
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True), {'something': False})

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    newtoken = token.copy()
    newtoken.context['something'] = True

    assert tn1.added == tn2.added == []


@pytest.mark.wip
def test_featuretesternode_pass_when_callable_dont_modify_context(TestNode):
    from pyknow.rete.nodes import FeatureTesterNode
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: {'something': True})
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True), {'something': True})

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    newtoken = token.copy()
    newtoken.context['something'] = True

    assert tn1.added == tn2.added == [newtoken]
