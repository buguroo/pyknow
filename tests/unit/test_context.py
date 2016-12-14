"""
    Basic tests for captured values
"""

from hypothesis import given
from conftest import random_kwargs


def test_context_not_defined_on_simple_rules():
    """
        test that a captured value is added to context, wich can
        be externally added so we'll be able to have a general context
        for all the facts in a rule
    """
    from pyknow.fact import Fact, C
    from pyknow.rule import Rule

    rule = Rule(Fact(name=C('stuff')))
    assert rule.context is None


def rules_can_be_defined_outside_ke():
    """
        Test that if we define a rule outside the knowledge engine

    """
    from pyknow.fact import Fact, C, L
    from pyknow.rule import Rule
    from pyknow.engine import KnowledgeEngine
    from pyknow.factlist import FactList

    rule = Rule(Fact(name=C('stuff')))
    executed = False

    class TestKE(KnowledgeEngine):
        @rule
        def is_stuff(self):
            nonlocal executed
            executed = True

    ke_ = TestKE()
    ke_.declare(Fact(name=L("foo")))
    ke_.run()

    assert ke_.context
    assert rule.context
    assert executed

    fl_ = FactList()
    fl_.declare(Fact(name=L('foo')))

    rule.get_activations(fl_)
    assert rule.context == {'name': 'stuff'}


def test_rule_inherit_ke_context():
    """
        KnowledgeEngine has context and rules assigned to it inherit it
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, V, L
    from collections import defaultdict
    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(name=C("name_p")))
        def rule1(self, name_p):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(name=V("name_p")))
        def rule2(self, name_p):
            """ Second rule, only something=3 """
            nonlocal executions
            executions.append('rule2')

    ke_ = Test()
    ke_.reset()

    to_declare = []

    for i in range(1, 10):
        to_declare.append(L(i))

    to_declare = dict(enumerate(to_declare))

    for k, n in to_declare.items():
        ke_.declare(Fact(name=n))

    results = defaultdict(list)
    acts = []
    for activation in ke_.agenda.activations:
        acts.append(activation)
        results[''.join([str(to_declare[a - 1].resolve())
                         for a in activation.facts])].append(1)

    ke_.run()

    for act in acts:
        assert act.rule.context is ke_.context


def test_can_capture_values():
    """
        KnowledgeEngine has context
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, V, L
    from collections import defaultdict
    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(name=C("name_p")))
        def rule1(self, name_p):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(name=V("name_p")))
        def rule2(self, name_p):
            """ Second rule, only something=3 """
            nonlocal executions
            executions.append('rule2')

    ke_ = Test()
    ke_.reset()

    to_declare = []

    for i in range(1, 10):
        to_declare.append(L(i))

    to_declare = dict(enumerate(to_declare))

    for k, n in to_declare.items():
        ke_.declare(Fact(name=n))

    results = defaultdict(list)
    acts = []
    for activation in ke_.agenda.activations:
        acts.append(activation)
        results[''.join([str(to_declare[a - 1].resolve())
                         for a in activation.facts])].append(1)

    ke_.run()

    for act in acts:
        assert act.rule.context is ke_.context

    print(ke_.context)
    assert ke_.context


@given(kwargs=random_kwargs)
def test_cv_rhs_arguments(kwargs):
    """
    Tests Capture context being passed as kwargs

    """

    from pyknow.fact import Fact, C, L
    from pyknow.rule import Rule
    from pyknow.engine import KnowledgeEngine

    class TestKE(KnowledgeEngine):
        @Rule(Fact(name=C('stuff')))
        def is_stuff(self, stuff):
            assert stuff == "foo"

    ke_ = TestKE()
    ke_.declare(Fact(name=L("foo")))
    ke_.run()
