def test_engine_import():
    try:
        from pyknow import engine
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_KnowledgeEngine_exists():
    from pyknow import engine
    assert hasattr(engine, 'KnowledgeEngine')


def test_KnowledgeEngine_is_class():
    from pyknow import engine
    assert isinstance(engine.KnowledgeEngine, type)


def test_KnowledgeEngine_has__facts():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, '_facts')


def test_KnowledgeEngine__facts_is_FactList():
    from pyknow.engine import KnowledgeEngine
    from pyknow.factlist import FactList

    ke = KnowledgeEngine()
    assert isinstance(ke._facts, FactList)


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
        ke._facts = mock
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
        ke._facts = mock
        ke.retract(0)
        assert mock.retract.called


def test_KnowledgeEngine_retract_matching_retracts_fact():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke._facts = mock
        ke.retract_matching(False)
        assert mock.retract_matching.called


def test_KnowledgeEngine_modify_retracts_and_declares():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        with patch('pyknow.engine.KnowledgeEngine.declare') as declare_mock:
            ke._facts = mock
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

    class Test(KnowledgeEngine):
        @Rule()
        def rule1(self):
            pass

        @Rule()
        def rule2(self):
            pass

    ke = Test()

    rules = ke.get_rules()

    assert len(rules) == 2
    assert all(isinstance(x, Rule) for x in rules)


def test_KnowledgeEngine_get_activations_exists():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'get_activations')


def test_KnowledgeEngine_get_activations_returns_a_list():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()
    assert ke.get_activations() == []


def test_KnowledgeEngine_get_activations_returns_activations():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import InitialFact

    class Test(KnowledgeEngine):
        @Rule()
        def test(self):
            pass

    ke = Test()

    activations = ke.get_activations()
    assert len(activations) == 0

    ke.declare(InitialFact())

    activations = ke.get_activations()
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
    ke._facts = None

    ke.reset()
    assert ke._facts is not None


def test_KnowledgeEngine_reset_declares_InitialFact():
    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import InitialFact

    ke = KnowledgeEngine()
    assert not ke._facts.matches(InitialFact())

    ke.reset()
    assert ke._facts.matches(InitialFact())


def test_KnowledgeEngine_run_1_fires_activation():
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule

    executed = False

    class Test(KnowledgeEngine):
        @Rule()
        def rule1(self):
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
            nonlocal executed
            executed += 1

        @Rule()
        def rule2(self):
            nonlocal executed
            executed += 1

        @Rule()
        def rule3(self):
            nonlocal executed
            executed += 1

    ke = Test()

    ke.reset()
    assert executed == 0

    ke.run()
    assert executed == 3


def test_KnowledgeEngine_has_initialfacts():
    from pyknow.engine import KnowledgeEngine
    assert KnowledgeEngine()._fixed_facts == []


def test_KE_parent():
    from pyknow.engine import KnowledgeEngine
    engine = KnowledgeEngine()
    assert not engine.parent
    parent = KnowledgeEngine
    engine.parent = parent
    assert parent is engine.parent
