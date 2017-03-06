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

    class SampleEngine(KnowledgeEngine):
        @Rule(Fact(a=1))
        def sample(self):
            pass

    engine = SampleEngine()
    branch = EngineWalker(engine)
    list(branch.get_network())
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


def test_get_alpha_branch():
    pass


def test_get_beta_node():
    pass


def get_node():
    pass
