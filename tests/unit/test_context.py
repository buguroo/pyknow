"""
    Basic tests for captured values
"""

from hypothesis import given
from conftest import random_kwargs
import pytest


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
        def is_stuff(self, stuff):
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
        def rule2(self):
            """ Second rule, only something=3 """
            nonlocal executions
            executions.append('rule2')

        @Rule(Fact(other=L('foo')))
        def rule3(self):
            """ third rule, check that name_p is not here """
            pass

        @Rule(Fact(name=L("name_p")))
        def rule4(self):
            """
                Fourth rule, check that if we match against name_p
                with a literal, it does NOT pass it as an argument
            """
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
    from pyknow.fact import Fact, C, V, T, L
    from collections import defaultdict
    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(n=L(1), name=C("name_p")))
        def rule1(self, name_p):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(n=L(1), name=C('name_p')), Fact(n=L(1), name=V("name_p")))
        def rule2(self, name_p):
            """
            Second rule, only when when we can capture a name.
            """
            nonlocal executions
            executions.append('rule2')

        @Rule(Fact(other=L('foo')))
        def rule3(self):
            """ third rule, check that name_p is not here """
            pass

        @Rule(Fact(name=T(lambda c, x: True)))
        def rule4(self):
            """
            Fourth rule, test if we match name against another type
            it wont have params
            """
            nonlocal executions
            executions.append('rule4')

        @Rule(Fact(n=L(1), name=V("name_p")))
        def rule5(self):
            """
            Fifth rule, we should only match against the captured
            value in the first rule, wich should be 1.
            """
            nonlocal executions
            executions.append('rule5')

    ke_ = Test()
    ke_.reset()

    to_declare = []

    for i in range(1, 10):
        to_declare.append(L(i))

    to_declare = dict(enumerate(to_declare))

    for k, n in to_declare.items():
        ke_.declare(Fact(n=L(k), name=n))

    results = defaultdict(list)
    acts = []
    for activation in ke_.agenda.activations:
        acts.append(activation)
        results[''.join([str(to_declare[a - 1].resolve())
                         for a in activation.facts])].append(1)

    ke_.run()

    for act in acts:
        assert act.rule.context is ke_.context

    assert ke_.context
    print(executions)
    assert executions.count('rule4') == len(to_declare)
    assert executions.count('rule1') == 1
    assert executions.count('rule5') == 1
    assert executions.count('rule2') == 1
    assert len(executions) == len(to_declare) + 3


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


@given(kwargs=random_kwargs)
def test_cv_rhs_arguments_not_on_others(kwargs):
    """
    Tests that fact does pass kwargs to another
    activations

    """
    from pyknow.fact import Fact, C, T, L
    from pyknow.rule import Rule
    from pyknow.engine import KnowledgeEngine

    class TestKE(KnowledgeEngine):
        @Rule(Fact(name=C('stuff')))
        def is_stuff(self, stuff):
            assert stuff == "foo"

        @Rule(Fact(name=T(lambda c, x: x)))
        def is_foo(self):
            assert True

    ke_ = TestKE()
    ke_.declare(Fact(name=L("foo")))
    ke_.run()


def test_can_produce_values():
    """
        KnowledgeEngine has context
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, NOT
    from pyknow.fact import Fact, C, L, V

    executions = []

    class FooFact(Fact):
        pass

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(name=C('name_p')),
              NOT(Fact(other=V("name_p"))))
        def rule2(self, name_p):
            """
            Second rule, only something=3
            THIS ONE SHOULD NOT BE EXECUTED
            """
            nonlocal executions
            executions.append('rule2')

    ke_ = Test()
    ke_.reset()

    ke_.declare(Fact(name=L("Foo"), other=L("asdf")))
    ke_.declare(Fact(name=L("Foo"), other=L("Foo")))

    ke_.run()

    assert executions.count('rule2') == 1
    print(executions)


def test_V_with_context():
    """
    Basic test V operator
    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, L, V
    from pyknow.engine import KnowledgeEngine

    executions = []

    class PeopleEngine(KnowledgeEngine):
        @Rule(Fact(name=C('name_t'), surname=V('name_t')))
        def name_is_same_as_surname(self, name_t):
            nonlocal executions
            executions.append(name_t)
            print("Name {} has the same surname".format(name_t))

    engine = PeopleEngine()
    engine.reset()
    engine.declare(Fact(name=L("David"), surname=L("Francos")))
    engine.declare(Fact(name=L("Rodriguez"), surname=L("Rodriguez")))
    engine.run()
    assert executions == ["Rodriguez"]


def test_C_with_context_alone():
    """
    Basic test C operator alone
    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, L, V
    from pyknow.engine import KnowledgeEngine

    executions = []

    class PeopleEngine(KnowledgeEngine):
        @Rule(Fact(name=C('name_t')))
        def name_is_same_as_surname(self, name_t):
            nonlocal executions
            executions.append(name_t)

    engine = PeopleEngine()
    engine.reset()
    engine.declare(Fact(name=L("David"), surname=L("Francos")))
    engine.declare(Fact(name=L("Rodriguez"), surname=L("Rodriguez")))
    engine.run()
    assert len(executions) == 2
