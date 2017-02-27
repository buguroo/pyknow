"""
Engine tests
"""

# pylint: disable=invalid-name, missing-docstring


def test_KnowledgeEngine_has__facts():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, 'facts')


def test_KnowledgeEngine__facts_is_FactList():
    from pyknow.engine import KnowledgeEngine
    from pyknow.factlist import FactList

    ke = KnowledgeEngine()
    assert isinstance(ke.facts, FactList)


def test_KnowledgeEngine_has_declare():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, 'declare')


def test_KnowledgeEngine_declare_define_fact():
    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import Fact
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke.facts = mock
        ke.declare(Fact())
        assert mock.declare.called


def test_KnowledgeEngine_has_retract():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'retract')


def test_KnowledgeEngine_has_retract_matching():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'retract_matching')


def test_KnowledgeEngine_retract_retracts_fact():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke.facts = mock
        ke.retract(0)
        assert mock.retract.called


def test_KnowledgeEngine_retract_matching_retracts_fact():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke.facts = mock
        ke.retract_matching(False)
        assert mock.retract_matching.called


def test_KnowledgeEngine_modify_retracts_and_declares():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        with patch('pyknow.engine.KnowledgeEngine.declare') as declare_mock:
            ke.facts = mock
            ke.modify(False, False)
            assert mock.retract_matching.called
            assert declare_mock.called


def test_KnowledgeEngine_has_agenda():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, 'agenda')


def test_KnowledgeEngine_agenda_is_Agenda():
    from pyknow.engine import KnowledgeEngine
    from pyknow.agenda import Agenda

    ke = KnowledgeEngine()

    assert isinstance(ke.agenda, Agenda)


def test_KnowledgeEngine_default_strategy_is_Depth():
    from pyknow.engine import KnowledgeEngine
    from pyknow.strategies import Depth

    assert KnowledgeEngine.__strategy__ is Depth


def test_KnowledgeEngine_default_strategy_is_Depth_instance():
    from pyknow.engine import KnowledgeEngine
    from pyknow.strategies import Depth

    assert isinstance(KnowledgeEngine().strategy, Depth)


def test_KnowledgeEngine_has_get_rules_property():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'get_rules')


def test_KnowledgeEngine_get_rules_return_empty_list():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()

    assert ke.get_rules() == []


def test_KnowledgeEngine_get_rules_returns_the_list_of_rules():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import InitialFact

    class Test(KnowledgeEngine):
        @Rule(InitialFact())
        def rule1(self):
            pass

        @Rule(InitialFact())
        def rule2(self):
            pass

    ke = Test()

    rules = ke.get_rules()

    assert len(rules) == 2
    assert all(isinstance(x, Rule) for x in rules)


def test_KnowledgeEngine_get_activations_exists():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'get_activations')


def test_KnowledgeEngine_get_activations_returns_a_generator():
    from pyknow.engine import KnowledgeEngine
    import types

    ke = KnowledgeEngine()
    assert isinstance(ke.get_activations(), types.GeneratorType)


def test_KnowledgeEngine_get_activations_returns_activations():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L

    class Test(KnowledgeEngine):
        # pylint: disable=too-few-public-methods
        @Rule(Fact(a=L(1)))
        def test(self):
            # pylint: disable=no-self-use
            pass

    ke = Test()
    ke.deffacts(Fact(a=L(1)))
    ke.reset()
    activations = list(ke.get_activations())
    assert len(activations) == 1


def test_KnowledgeEngine_has_run():
    from pyknow.engine import KnowledgeEngine
    assert hasattr(KnowledgeEngine, 'run')


def test_KnowledgeEngine_has_reset():
    from pyknow.engine import KnowledgeEngine
    assert hasattr(KnowledgeEngine, 'reset')


def test_KnowledgeEngine_reset_resets_agenda():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    ke.agenda = None

    ke.reset()
    assert ke.agenda is not None


def test_KnowledgeEngine_reset_resets_facts():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    ke.facts = None

    ke.reset()
    assert ke.facts is not None


def test_KnowledgeEngine_run_1_fires_activation():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule

    executed = False

    class Test(KnowledgeEngine):
        # pylint: disable=too-few-public-methods
        @Rule()
        def rule1(self):
            # pylint: disable=no-self-use
            nonlocal executed
            executed = True

    ke = Test()

    ke.reset()
    assert not executed

    ke.run(1)
    assert executed


def test_KnowledgeEngine_run_fires_all_activation():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule

    executed = 0

    class Test(KnowledgeEngine):
        @Rule()
        def rule1(self):
            # pylint: disable=no-self-use
            nonlocal executed
            executed += 1

        @Rule()
        def rule2(self):
            # pylint: disable=no-self-use
            nonlocal executed
            executed += 1

        @Rule()
        def rule3(self):
            # pylint: disable=no-self-use
            nonlocal executed
            executed += 1

    ke = Test()

    ke.reset()
    assert executed == 0

    ke.run()
    assert executed == 3


def test_KnowledgeEngine_has_initialfacts():
    from pyknow.engine import KnowledgeEngine
    # pylint: disable=protected-access
    assert KnowledgeEngine()._fixed_facts == []


def test_KE_parent():
    from pyknow.engine import KnowledgeEngine
    engine = KnowledgeEngine()
    assert not engine.parent
    parent = KnowledgeEngine()
    engine.parent = parent
    assert parent is engine.parent


def test_KnowledgeEngine_reset():
    """
    Given a set of fixed facts, they're still there
    after a reset.
    Also, we have in account that InitialFact() is always there.
    And that if we add a normal fact after that, it's not persistent
    """

    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import Fact, L

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.deffacts(Fact(foo=L(1), bar=L(2)))
    ke.reset()

    assert len(ke.facts.facts) == 3

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.declare(Fact(foo=L(9)))
    ke.deffacts(Fact(foo=L(1), bar=L(2)))
    ke.reset()

    assert len(ke.facts.facts) == 3

    ke = KnowledgeEngine()
    ke.deffacts(Fact(foo=L(1)))
    ke.declare(Fact(foo=L(9)))
    ke.reset()

    assert len(ke.facts.facts) == 2
