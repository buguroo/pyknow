"""
EngineWalker related tests

"""
import pytest


@pytest.mark.wip
def test_alpha_network_first_is_class_check():
    from pyknow.rete.alpha import EngineWalker
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from pyknow.engine import KnowledgeEngine
    from pyknow.rete.nodes import BusNode

    class SampleEngine(KnowledgeEngine):
        @Rule(Fact(a=1))
        def sample(self):
            pass

    engine = SampleEngine()
    branch = EngineWalker(engine, BusNode())
    branch.build_network()
    same_class_condition = branch.input_nodes[0].matcher
    assert same_class_condition(Fact())
    assert not same_class_condition(False)


@pytest.mark.wip
def test_alpha_network_get_callables_L():
    from pyknow.fact import Fact
    from pyknow.rete.alpha import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_L']
    callables = EngineWalker.get_callables(Fact(a=1))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_alpha_network_get_callables_W():
    from pyknow.fact import Fact, W
    from pyknow.rete.alpha import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_W']
    callables = EngineWalker.get_callables(Fact(a=W(True)))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_alpha_network_get_callables_T():
    from pyknow.fact import Fact, T
    from pyknow.rete.alpha import EngineWalker
    expected = ['same_class', 'compatible_facts', 'has_key', 'match_T']
    callables = EngineWalker.get_callables(Fact(a=T(lambda x: x)))
    callable_names = [a[0].__repr__().split('.')[1] for a in callables]
    assert callable_names == expected


@pytest.mark.wip
def test_get_alpha_branch():
    from collections import namedtuple
    from pyknow.rete.alpha import EngineWalker
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
def test_get_beta_node():
    from unittest.mock import MagicMock
    from pyknow.rete.alpha import EngineWalker
    from pyknow.engine import KnowledgeEngine
    from pyknow.rete.nodes import BusNode, FeatureTesterNode

    EngineWalker.get_node = lambda s, node: FeatureTesterNode(node._activate)

    left_node = MagicMock()
    right_node = MagicMock()

    walker = EngineWalker(KnowledgeEngine(), BusNode())
    beta = walker.get_beta_node(left_node, right_node)

    assert left_node.add_child.called_with(beta, beta._activate_left)
    assert right_node.add_child.called_with(beta, beta._activate_right)


def test_get_node():
    from pyknow.rete.alpha import EngineWalker
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact
    from unittest.mock import patch
    from pyknow.rete.nodes import BusNode

    with patch.object(EngineWalker, "get_beta_node", return_value=[]) as mock:
        walker = EngineWalker(KnowledgeEngine(), BusNode())
        # TODO: What happens if we pass here Fact(a=1) and not b?
        walker.get_node(Rule(Fact(a=1), Fact(b=1)))
        mock.assert_called()

    with patch.object(EngineWalker, "get_alpha_branch",
                      return_value=[]) as mock:
        walker = EngineWalker(KnowledgeEngine())
        walker.get_node(Fact(a=1))
        mock.assert_called()
