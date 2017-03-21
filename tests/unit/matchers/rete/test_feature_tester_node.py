import pytest


def test_featuretesternode_exists():
    try:
        from pyknow.matchers.rete.nodes import FeatureTesterNode
    except ImportError as exc:
        assert False, exc


def test_featuretesternode_is_oneinputnode():
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.abstract import OneInputNode

    assert issubclass(FeatureTesterNode, OneInputNode)


def test_featuretesternode_accepts_callable():
    from pyknow.matchers.rete.nodes import FeatureTesterNode

    # MUST NOT RAISE
    FeatureTesterNode(lambda x: True)

    with pytest.raises(TypeError):
        FeatureTesterNode('NONCALLABLE')


def test_featuretesternode_pass_when_callable_succeed(TestNode):
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: True)
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True))

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    assert tn1.added == tn2.added == [token]


def test_featuretesternode_pass_when_callable_fail(TestNode):
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    ftn = FeatureTesterNode(lambda f: False)
    tn1 = TestNode()
    tn2 = TestNode()

    token = Token.valid(Fact(test=True))

    ftn.add_child(tn1, tn1.activate)
    ftn.add_child(tn2, tn2.activate)

    ftn.activate(token)

    assert tn1.added == tn2.added == []


def test_featuretesternode_pass_when_callable_adds_context(TestNode):
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
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


def test_featuretesternode_pass_when_callable_modify_context(TestNode):
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
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


def test_featuretesternode_pass_when_callable_dont_modify_context(TestNode):
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
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


def test_featuretesternode_pass_fact_to_matcher():
    from pyknow.matchers.rete.nodes import FeatureTesterNode
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    fact = Fact(this_is_my_fact=True)

    def _matcher(f):
        nonlocal fact
        assert f is fact

    ftn = FeatureTesterNode(_matcher)

    ftn.activate(Token.valid(fact))
