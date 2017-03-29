"""
Engine tests
"""

import pytest

from hypothesis import given
from hypothesis import strategies as st


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
    from pyknow import Fact
    from unittest.mock import patch

    ke = KnowledgeEngine()
    with patch('pyknow.factlist.FactList') as mock:
        ke.facts = mock
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
        ke.facts = mock
        ke.retract({'__factid__': (0, )})
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
    from pyknow.strategies import DepthStrategy

    assert KnowledgeEngine.__strategy__ is DepthStrategy


def test_KnowledgeEngine_default_strategy_is_Depth_instance():
    from pyknow.engine import KnowledgeEngine
    from pyknow.strategies import DepthStrategy

    assert isinstance(KnowledgeEngine().strategy, DepthStrategy)


def test_KnowledgeEngine_has_get_rules_property():
    from pyknow.engine import KnowledgeEngine

    assert hasattr(KnowledgeEngine, 'get_rules')


def test_KnowledgeEngine_get_rules_return_empty_list():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()

    assert ke.get_rules() == []


def test_KnowledgeEngine_get_rules_returns_the_list_of_rules():
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule
    from pyknow import InitialFact

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


def test_KnowledgeEngine_get_activations_returns_a_list():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()

    res = ke.get_activations()

    assert isinstance(res, tuple)
    assert isinstance(res[0], list)
    assert isinstance(res[1], list)


def test_KnowledgeEngine_get_activations_returns_activations_added():
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule
    from pyknow import Fact

    class Test(KnowledgeEngine):
        @Rule(Fact(a=1),
              Fact(b=1),
              Fact(c=1))
        def test(self):
            pass

    ke = Test()

    ke.reset()

    ke.declare(Fact(a=1))
    ke.declare(Fact(b=1))
    ke.declare(Fact(c=1))

    assert len(ke.agenda.activations) == 1


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
    from pyknow import Rule

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
    from pyknow import Rule

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
    from pyknow import InitialFact

    assert list(KnowledgeEngine()._declare_initial_fact()) == [InitialFact()]


def test_KnowledgeEngine_reset():
    """
    Given a set of fixed facts, they're still there
    after a reset.
    Also, we have in account that InitialFact() is always there.
    And that if we add a normal fact after that, it's not persistent
    """

    from pyknow.engine import KnowledgeEngine
    from pyknow.deffacts import DefFacts
    from pyknow import Fact

    class KE1(KnowledgeEngine):
        @DefFacts()
        def some_facts(self):
            yield Fact(foo=1)

    ke = KE1()
    ke.declare(Fact(bar=9))
    ke.declare(Fact(bar=7))
    ke.declare(Fact(bar=8))
    ke.reset()

    assert len(ke.facts) == 2  # Initialfact + Fact(foo=1)

    ke = KE1()
    ke.reset()
    ke.declare(Fact(foo=2))
    ke.declare(Fact(foo=3, bar=4))

    assert len(ke.facts) == 4


@pytest.mark.slow
@given(to_declare_random=st.lists(st.integers()))
def test_rules_are_executed_once(to_declare_random):
    from random import shuffle
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule, DefFacts
    from pyknow import Fact, L

    executions = []
    to_declare = list(set(to_declare_random + [1, 2, 3]))
    shuffle(to_declare)

    class Test(KnowledgeEngine):
        @DefFacts()
        def tested_deffacts(self):
            for i in to_declare:
                yield Fact(something=i)

        @Rule(Fact(something=L(1)),
              Fact(something=L(2)))
        def rule1(self):
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(something=L(3)))
        def rule2(self):
            nonlocal executions
            executions.append('rule2')

    ke = Test()
    ke.reset()
    ke.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1


def test_default_is_and():
    """
    Test that AND is the default behavior
    """
    from collections import defaultdict
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule, DefFacts
    from pyknow import Fact, L

    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @DefFacts()
        def test_facts(self):
            for n in (1, 2, 3):
                yield Fact(something=n)

        @Rule(Fact(something=1),
              Fact(something=2))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(something=3))
        def rule2(self):
            """ Second rule, only something=3 """
            nonlocal executions
            executions.append('rule2')

    ke = Test()
    ke.reset()
    ke.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1


def test_or_notmatching_operator():
    """
    Test OR operator
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule, OR, DefFacts
    from pyknow import Fact, L

    class Test(KnowledgeEngine):
        """ Test KE """
        @DefFacts()
        def some_facts(self):
            yield Fact(other=1)
            yield Fact(other=2)

        @Rule(OR(Fact(something=1),
                 Fact(something=2)))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            pass

    ke_ = Test()
    ke_.reset()
    assert len(ke_.agenda.activations) == 0


def test_or_operator():
    """
    Test OR operator
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow import Rule, OR
    from pyknow import Fact, L

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(OR(Fact(something=L(1)),
                 Fact(something=L(2))))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            pass

    ke_ = Test()
    ke_.reset()
    ke_.declare(Fact(something=1))
    assert len(ke_.agenda.activations) == 1

    ke_ = Test()
    ke_.reset()
    ke_.declare(Fact(something=2))
    assert len(ke_.agenda.activations) == 1

    ke_ = Test()
    ke_.reset()
    ke_.declare(Fact(something=3))
    assert len(ke_.agenda.activations) == 0


def test_ke_inheritance():
    from pyknow import Rule
    from pyknow import Fact, L
    from pyknow.engine import KnowledgeEngine

    executed = False

    class Person(Fact):
        pass

    class Base(KnowledgeEngine):
        @Rule(Person(name=L('pepe')))
        def is_pepe(self):
            self.declare(Person(drinks="coffee"))

    class Test(Base):
        @Rule(Person(drinks=L("coffee")))
        def drinks_coffee(self):
            nonlocal executed
            executed = True

    ke_ = Test()
    ke_.reset()
    ke_.declare(Person(name='pepe'))
    ke_.run()

    assert executed


def test_nested_declarations():
    from pyknow import Rule
    from pyknow import Fact, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executed = False

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=L("David")))
        def david(self):
            self.declare(Person(name="Pepe"))

        @Rule(Person(name=L("Pepe")))
        def pepe(self):
            nonlocal executed
            executed = True

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="David"))
    ke_.run()
    assert executed


def test_matching_different_number_of_arguments():
    from pyknow import Rule
    from pyknow import Fact, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executed = False

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=L("David")))
        def david(self):
            self.declare(Person(name="Pepe", apellido="stuff"))

        @Rule(Person(name=L("Pepe")))
        def pepe(self):
            nonlocal executed
            executed = True

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="David"))
    ke_.run()
    assert executed


def test_matching_captured_different_facts_AND():
    from pyknow import Rule
    from pyknow import Fact, W, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=W("name")), Person(surname=W("name")))
        def same_name(self, name="lala"):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="NotAName", surname='surname'))
    ke_.declare(Person(name='name', surname="NotAName"))
    ke_.run()
    assert executions == ["NotAName"]


def test_matching_captured_same_facts_AND():
    """
    CLIPs behaves like this::

        (watch all)

        (deftemplate person
           (slot name)
           (slot surname)
        )

        (defrule test_clips
         (foo (name ?thename))
         (foo (surname ?thename))
        => (printout t "found " ?valor_1 crlf ))

        (deffacts thenames
            (person (name NotAName) (surname NotAName))
            (person (name name) (surname NotAName))
        )

        (reset)
        (run)

    Result:

        FIRE    1 test_clips: f-1,f-2

    """
    from pyknow import Rule
    from pyknow import Fact, L, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=W("name"), surname=W('name')))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name='NotAName', surname="NotAName"))
    ke_.declare(Person(name='name', surname="NotAName"))
    ke_.run()
    assert executions == ["NotAName"]


def test_matching_captured_different_facts_NOT_positive():
    """
    Declaring a NOT() using C/V should be a factlist-wide
    comparision.

    Positive test (returning activation because there were
    NO matches (the NOT is therefore executed).
    """
    from pyknow import Rule, NOT
    from pyknow import Fact, L, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=W("name")),
              NOT(Person(surname=W('name'))))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name='name', surname="NotAName"))
    ke_.run()
    assert executions == ["name"]


def test_matching_captured_different_facts_NOT_negative():
    """
    Declaring a NOT() using C/V should be a factlist-wide
    comparision.

    Negative test (returning no activation because there were
    matches (the NOT is therefore not executed).
    """
    from pyknow import Rule, NOT
    from pyknow import Fact, W, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=W("name")),
              NOT(Person(surname=W('name'))))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name='name', surname="NotAName"))
    ke_.declare(Person(name='name', surname="name"))
    ke_.run()
    assert executions == []


def test_and_negated_variable__bad_definition():
    from pyknow import Rule, NOT
    from pyknow import Fact, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(age=~W('age')),
              Person(age=W('age')))
        def same_name(self, age):
            nonlocal executions
            executions.append(age)

    ke_ = Person_KE()
    ke_.reset()

    with pytest.raises(RuntimeError):
        ke_.declare(Person(age=15))


def test_and_negated_variable__positive_match():
    from pyknow import Rule, NOT
    from pyknow import Fact, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(age=W('age')),
              Person(age=~W('age')))
        def same_name(self, age):
            nonlocal executions
            executions.append(age)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name="name2", age=19))
    ke_.run()
    assert set(executions) == {18, 19}


def test_and_negated_variable__negative_match():
    from pyknow import Rule, NOT
    from pyknow import Fact, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(age=W('age')),
              Person(age=~W("age")))
        def same_name(self, age):
            nonlocal executions
            executions.append(age)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name="name2", age=18))
    ke_.run()
    assert executions == []


def test_not_aggregation():
    from pyknow import Rule, NOT, AND
    from pyknow import Fact, W
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    class ConflictResolver(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(NOT(ConflictResolver(resolved=True)),
              AND(Person(age=W('age')),
                  Person(age=~W("age"))))
        def same_name(self, age):
            nonlocal executions
            executions.append(age)

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name='name2', age=19))
    ke_.declare(ConflictResolver(resolved=True))
    ke_.run()
    assert executions == []

    executions = []
    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name='name2', age=19))
    ke_.run()
    assert set(executions) == {18, 19}

    executions = []
    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name="name2", age=18))
    ke_.run()
    assert executions == []

    ke_ = Person_KE()
    ke_.reset()
    ke_.declare(Person(name="name1", age=18))
    ke_.declare(Person(name="name2", age=18))
    ke_.declare(ConflictResolver(resolved=True))
    ke_.run()
    assert executions == []


def test_declare_raises_typeerror_if_conditionalelement_found():
    from pyknow import KnowledgeEngine, L, W, P, Fact

    ke = KnowledgeEngine()

    with pytest.raises(TypeError):
        ke.declare(Fact(L(1)))

    with pytest.raises(TypeError):
        ke.declare(Fact(W()))

    with pytest.raises(TypeError):
        ke.declare(Fact(P(lambda _: True)))

    with pytest.raises(TypeError):
        ke.declare(Fact(~L(1)))

    with pytest.raises(TypeError):
        ke.declare(Fact(L(1) | L(2)))

    with pytest.raises(TypeError):
        ke.declare(Fact(L(1) & L(2)))
