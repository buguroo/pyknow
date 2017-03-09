"""
EngineWalker related tests

"""
import pytest


@pytest.mark.wip
def test_alpha_network_first_is_class_check():
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.engine import KnowledgeEngine

    class SampleEngine(KnowledgeEngine):
        @Rule(Fact(a=1), Fact(b=1))
        def sample(self):
            pass

    engine = SampleEngine()
    input_node = engine.matcher.walker.input_nodes[0]
    same_class_condition = input_node.matcher
    assert same_class_condition(Fact())
    assert not same_class_condition(False)


@pytest.mark.wip
def test_alpha_network_get_callables_L():
    from pyknow.fact import Fact
    from pyknow.rete.walker import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_L']
    callables = EngineWalker.get_callables(Fact(a=1))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_alpha_network_get_callables_W():
    from pyknow.fact import Fact, W
    from pyknow.rete.walker import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_W']
    callables = EngineWalker.get_callables(Fact(a=W(True)))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_alpha_network_get_callables_T():
    from pyknow.fact import Fact, T
    from pyknow.rete.walker import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_T']
    callables = EngineWalker.get_callables(Fact(a=T(lambda x: x)))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_get_alpha_branch():
    from collections import namedtuple
    from pyknow.rete.walker import EngineWalker
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.engine import KnowledgeEngine
    from pyknow.rete.nodes import BusNode

    executions = []

    class SampleEngine(KnowledgeEngine):
        @Rule(Fact(a=1))
        def sample(self):
            pass

    class FakeFeatureTesterNode(namedtuple("Fake", "value")):
        def add_child(self, child, method):
            nonlocal executions
            executions.append(child.value.__repr__().split('.')[1])

        def _activate(self):
            pass

    engine = SampleEngine()
    branch_walker = EngineWalker(engine, BusNode())
    branch = branch_walker.get_alpha_branch(FakeFeatureTesterNode, Fact(a=1))

    # We return the last node
    assert [a.__repr__().split('.')[1] for a in branch] == ["match_L"]

    # And we have added as children all nodes except the first one.
    assert executions == ['compatible_facts', 'has_key', 'match_L']

    # The first one is, however, to be found in input nodes of the branch
    # First node should always check for same class.
    input_node = branch_walker.input_nodes[0]
    input_node_callable = input_node.value.__repr__().split('.')[1]

    assert input_node_callable == "same_class"


@pytest.mark.wip
def test_get_node():
    from pyknow.rete.walker import EngineWalker
    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import Fact
    from unittest.mock import patch
    from pyknow.rete.nodes import BusNode

    with patch.object(EngineWalker, "get_alpha_branch",
                      return_value=[]) as mock:
        walker = EngineWalker(KnowledgeEngine(), BusNode)
        walker.get_node(Fact(a=1))
        mock.assert_called()


@pytest.mark.wip
def test_network_generation():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.rete.nodes import ConflictSetNode

    class FooEngine(KnowledgeEngine):
        @Rule(Fact(a=1))
        def foo(self):
            pass

    walker = FooEngine().matcher.walker

    def _get_node(node):
        if not isinstance(node, ConflictSetNode):
            yield node.matcher.__repr__().split('.')[1].split(' ')[0].strip()
        else:
            yield "ConflictSetNode"
        for child in node.children:
            yield from _get_node(child.node)

    expected = ['same_class', 'compatible_facts', 'has_key', 'match_L',
                'ConflictSetNode']

    assert list(_get_node(walker.input_nodes[0])) == expected
