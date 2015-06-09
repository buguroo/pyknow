import pytest


# @pytest.mark.wip
# def test_strategies_exists():
#     try:
#         from pyknow import strategies
#     except ImportError as exc:
#         assert False, exc
#     else:
#         assert True
# 
# 
# @pytest.mark.wip
# def test_Strategy_exists():
#     from pyknow import strategies
# 
#     assert hasattr(strategies, 'Strategy')
# 
# 
# @pytest.mark.wip
# def test_Strategy_is_class():
#     from pyknow.strategies import Strategy
# 
#     assert isinstance(Strategy, type)
# 
# 
# @pytest.mark.wip
# def test_Strategy_is_abstract():
#     from pyknow.strategies import Strategy
# 
#     with pytest.raises(TypeError):
#         Strategy()
# 
# 
# @pytest.mark.wip
# def test_Depth_exists():
#     from pyknow import strategies
# 
#     assert hasattr(strategies, 'Depth')
# 
# 
# @pytest.mark.wip
# def test_Depth_is_Strategy():
#     from pyknow.strategies import Depth, Strategy
# 
#     assert issubclass(Depth, Strategy)
# 
# 
# @pytest.mark.wip
# def test_Depth_has_build_agenda():
#     from pyknow.strategies import Depth
#     assert hasattr(Depth(), 'build_agenda')
# 
# 
# @pytest.mark.wip
# def test_Depth_build_agenda_no_facts_returns_empty_agenda():
#     from pyknow.strategies import Depth
#     from pyknow.engine import KnowledgeEngine
#     from collections import OrderedDict
# 
#     st = Depth()
# 
#     assert st.build_agenda(KnowledgeEngine()) == OrderedDict()
#     
# 
# @pytest.mark.wip
# def test_Depth_build_agenda_one_fact_returns_matching_rules_no_order():
#     from pyknow.strategies import Depth
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
#     from collections import OrderedDict
# 
#     st = Depth()
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.DEFINED)
#         def rule1(self):
#             pass
#         @AND(fact1=True)
#         def rule2(self):
#             pass
#         @AND(fact2=fs.DEFINED)
#         def rule3(self):
#             pass
# 
#     ke = Test()
#     ke.asrt('fact1', True)
#     agenda = st.build_agenda(ke)
# 
#     assert 'rule1' in agenda
#     assert 'rule2' in agenda
#     assert 'rule3' not in agenda
# 
# 
# @pytest.mark.wip
# def test_Depth_build_agenda_asertion_order_affects_agenda_order():
#     from pyknow.strategies import Depth
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
#     from collections import OrderedDict
# 
#     st = Depth()
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.DEFINED)
#         def rule1(self):
#             pass
#         @AND(fact2=fs.DEFINED)
#         def rule2(self):
#             pass
# 
#     ke = Test()
#     ke.asrt('fact1', True)
#     agenda1 = st.build_agenda(ke)
#     ke.asrt('fact2', True)
#     agenda2 = st.build_agenda(ke, current_agenda=agenda1)
#     
#     actual = list(agenda2.keys())
#     assert actual == ['rule1', 'rule2']
# 
# 
#     ke = Test()
#     ke.asrt('fact2', True)
#     agenda1 = st.build_agenda(ke)
#     ke.asrt('fact1', True)
#     agenda2 = st.build_agenda(ke, current_agenda=agenda1)
#     
#     actual = list(agenda2.keys())
#     assert actual == ['rule2', 'rule1']
# 
# 
# @pytest.mark.wip
# def test_Depth_build_agenda_previous_order_not_affected():
#     from pyknow.strategies import Depth
#     from pyknow.engine import KnowledgeEngine
#     from pyknow.rule import AND
#     from pyknow.rule import FactState as fs
#     from collections import OrderedDict
# 
#     st = Depth()
#     class Test(KnowledgeEngine):
#         @AND(fact1=fs.DEFINED)
#         def rule1(self):
#             pass
#         @AND(fact2=fs.DEFINED)
#         def rule2(self):
#             pass
#         @AND(fact3=fs.DEFINED)
#         def rule3(self):
#             pass
# 
#     ke = Test()
#     ke.asrt('fact1', True)
#     ke.asrt('fact2', True)
#     agenda1 = st.build_agenda(ke)
# 
#     ke.asrt('fact3', True)
#     agenda2 = st.build_agenda(ke, current_agenda=agenda1)
#     
#     assert list(agenda2.keys()) == list(agenda1.keys()) + ['rule3']
