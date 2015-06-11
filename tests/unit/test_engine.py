import pytest


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


def test_KnowledgeEngine_retract_retracts_fact():
    from pyknow.engine import KnowledgeEngine
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke._facts = mock
        ke.retract(0)
        assert mock.retract.called


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


# @pytest.mark.wip
# def test_KnowledgeEngine_has_run():
#     from pyknow.engine import KnowledgeEngine
#     assert hasattr(KnowledgeEngine, 'run')
# 
# 
# def test_KnowledgeEngine_run_set_running():
#     from pyknow.engine import KnowledgeEngine
# 
#     ke = KnowledgeEngine()
#     assert not ke.running
# 
#     ke.run()
#     assert ke.running
# 
# 
# def test_KnowledgeEngine_has_reset():
#     from pyknow.engine import KnowledgeEngine
#     assert hasattr(KnowledgeEngine, 'reset')
# 
# 
# def test_KnowledgeEngine_reset_resets_running():
#     from pyknow.engine import KnowledgeEngine
#     ke = KnowledgeEngine()
# 
#     ke.run()
#     assert ke.running
# 
#     ke.reset()
#     assert not ke.running
# 
# 
# def test_KnowledgeEngine_reset_resets_agenda():
#     from pyknow.engine import KnowledgeEngine
#     ke = KnowledgeEngine()
#     ke.agenda = None
# 
#     ke.reset()
#     assert ke.agenda is not None
# 
# 
# def test_KnowledgeEngine_reset_resets_facts():
#     from pyknow.engine import KnowledgeEngine
#     ke = KnowledgeEngine()
#     ke._facts = None
# 
#     ke.reset()
#     assert ke._facts is not None
#
# @pytest.mark.wip
# def test_KnowledgeEngine_get_matching_rules_exists():
#     from pyknow.engine import KnowledgeEngine
# 
#     assert hasattr(KnowledgeEngine, 'get_matching_rules')
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_get_matching_get_rules_returns_dict():
#     from pyknow.engine import KnowledgeEngine
# 
#     ke = KnowledgeEngine()
# 
#     assert isinstance(ke.get_matching_rules(), dict)
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_get_matching_get_rules__no_rules():
#     from pyknow.engine import KnowledgeEngine
# 
#     ke = KnowledgeEngine()
# 
#     assert ke.get_matching_rules() == {}
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_get_matching_get_rules__matching_rule():
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
# 
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.NOT_DEFINED)
#         def myrule(self):
#             pass
# 
#     ke = Test()
#     matching_rules = ke.get_matching_rules()
# 
#     assert 'myrule' in matching_rules
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_get_matching_get_rules__multiple_match():
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
# 
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.NOT_DEFINED)
#         def myrule1(self):
#             pass
# 
#         @AND(fact2=fs.NOT_DEFINED)
#         def myrule2(self):
#             pass
# 
#         @AND(fact3=fs.DEFINED)
#         def myrule3(self):
#             pass
# 
#     ke = Test()
#     matching_rules = ke.get_matching_rules()
# 
#     assert 'myrule1' in matching_rules
#     assert 'myrule2' in matching_rules
#     assert 'myrule3' not in matching_rules
# 
# 
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_run_1_modify_agenda_if_needed():
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
#     
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.DEFINED)
#         def rule1(self):
#             self.declare('fact2', True)
# 
#         @AND(fact2=fs.DEFINED)
#         def rule2(self):
#             pass
# 
#     ke = Test()
#     current_agenda = ke.agenda
#     ke.declare('fact1', True)
#     ke.run(1)
# 
#     assert current_agenda != ke.agenda
# 
# 
# @pytest.mark.wip
# def test_KnowledgeEngine_run_consumes_agenda():
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
#     
#     executed = False
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.DEFINED)
#         def rule1(self):
#             executed = True
# 
#     ke = Test()
#     current_agenda = ke.agenda
#     ke.declare('fact1', True)
#     ke.run()  # If this runs forever, then run is not consuming the agenda.
# 
#     assert executed
