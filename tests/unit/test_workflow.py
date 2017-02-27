from hypothesis import given
from hypothesis import strategies as st
import pytest

# pylint: disable=missing-docstring, invalid-name


@given(to_declare_random=st.lists(st.integers()))
def test_rules_are_executed_once(to_declare_random):
    from random import shuffle
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L

    executions = []

    class Test(KnowledgeEngine):
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

    to_declare = list(set(to_declare_random + [1, 2, 3]))
    shuffle(to_declare)
    print(to_declare)

    for i in to_declare:
        ke.deffacts(Fact(something=L(i)))

    ke.reset()
    ke.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1


def test_default_is_and():
    """
        Test that AND is the default operator
    """
    from collections import defaultdict
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L

    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(something=L(1)),
              Fact(something=L(2)))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(something=L(3)))
        def rule2(self):
            """ Second rule, only something=3 """
            nonlocal executions
            executions.append('rule2')

    ke_ = Test()

    to_declare = []

    for i in range(1, 10):
        to_declare.append(L(i))

    to_declare = dict(enumerate(to_declare))

    for k, n in to_declare.items():
        ke_.deffacts(Fact(something=n))

    ke_.reset()
    results = defaultdict(list)
    for activation in ke_.agenda.activations:
        results[''.join([str(to_declare[a - 1].resolve())
                         for a in activation.facts])].append(1)

    assert dict(results) == {'3': [1], '12': [1]}
    assert len(ke_.agenda.activations) == 2
    ke_.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1


def test_or_notmatching_operator():
    """
        Test OR operator
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, OR
    from pyknow.fact import Fact, L

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(OR(Fact(something=L(1)),
              Fact(something=L(2))))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            pass

    static = ((1, 3), (1, 3, 5))
    for test in static:
        ke_ = Test()
        ke_.reset()
        for val in test:
            ke_.deffacts(Fact(none=L(val)))
        ke_.reset()
        assert len(ke_.agenda.activations) == 0

    ke_.run()


def test_or_operator():
    """
    Test OR operator
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, OR
    from pyknow.fact import Fact, L

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(OR(Fact(something=L(1)),
              Fact(something=L(2))))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            pass

    ke_ = Test()
    ke_.deffacts(Fact(something=L(1)))
    ke_.reset()
    assert len(ke_.agenda.activations) == 1

    ke_ = Test()
    ke_.deffacts(Fact(something=L(2)))
    ke_.reset()
    assert len(ke_.agenda.activations) == 1

    ke_ = Test()
    ke_.deffacts(Fact(something=L(3)))
    ke_.reset()
    assert len(ke_.agenda.activations) == 0


def test_ke_inheritance():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L
    from pyknow.engine import KnowledgeEngine

    executed = False

    class Person(Fact):
        pass

    class Base(KnowledgeEngine):
        @Rule(Person(name=L('pepe')))
        def is_pepe(self):
            self.declare(Person(drinks=L("coffee")))

    class Test(Base):
        @Rule(Person(drinks=L("coffee")))
        def drinks_coffee(self):
            nonlocal executed
            executed = True

    ke_ = Test()
    ke_.deffacts(Person(name=L('pepe')))
    ke_.reset()
    ke_.run()

    assert executed


def test_nested_declarations():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executed = False

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=L("David")))
        def david(self):
            self.declare(Person(name=L("Pepe")))

        @Rule(Person(name=L("Pepe")))
        def pepe(self):
            nonlocal executed
            executed = True

    ke_ = Person_KE()
    ke_.deffacts(Person(name=L("David")))
    ke_.reset()
    ke_.run()
    assert executed


def test_matching_different_number_of_arguments():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executed = False

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=L("David")))
        def david(self):
            self.declare(Person(name=L("Pepe"), apellido=L("stuff")))

        @Rule(Person(name=L("Pepe")))
        def pepe(self):
            nonlocal executed
            executed = True

    ke_ = Person_KE()
    ke_.deffacts(Person(name=L("David")))
    ke_.reset()
    ke_.run()
    assert executed


def test_matching_captured_different_facts_AND():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L, V, C
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=C("name")), Person(surname=V('name')))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.deffacts(Person(surname=L('surname'), name=L("NotAName")))
    ke_.deffacts(Person(name=L('name'), surname=L("NotAName")))
    ke_.reset()
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


        (defrule test_clips
           (person (name ?thename))
           (person (surname ?thename))
           =>
           (printout t "Found"))

        (deffacts thenames
            (person (name NotAName) (surname NotAName))
            (person (name name) (surname NotAName))
        )

        (reset)
        (run)

    Result:

        FIRE    1 test_clips: f-1,f-2
        FIRE    2 test_clips: f-1,f-1

    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L, V, C
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=C("name"), surname=V('name')))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.deffacts(Person(name=L('NotAName'), surname=L("NotAName")))
    ke_.deffacts(Person(name=L('name'), surname=L("NotAName")))
    ke_.reset()
    ke_.run()
    assert executions == ["NotAName", "NotAName"]


def test_matching_captured_different_facts_NOT_positive():
    """
    Declaring a NOT() using C/V should be a factlist-wide
    comparision.

    Positive test (returning activation because there were
    NO matches (the NOT is therefore executed).
    """
    from pyknow.rule import Rule, NOT
    from pyknow.fact import Fact, L, V, C
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=C("name")),
              NOT(Person(surname=V('name'))))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.deffacts(Person(name=L('name'), surname=L("NotAName")))
    ke_.reset()
    ke_.run()
    assert executions == ["name"]


def test_matching_captured_different_facts_NOT_negative():
    """
    Declaring a NOT() using C/V should be a factlist-wide
    comparision.

    Negative test (returning no activation because there were
    matches (the NOT is therefore not executed).
    """
    from pyknow.rule import Rule, NOT
    from pyknow.fact import Fact, L, V, C
    from pyknow.engine import KnowledgeEngine

    class Person(Fact):
        pass

    executions = []

    class Person_KE(KnowledgeEngine):
        @Rule(Person(name=C("name")),
              NOT(Person(surname=V('name'))))
        def same_name(self, name):
            nonlocal executions
            executions.append(name)

    ke_ = Person_KE()
    ke_.deffacts(Person(name=L('name'), surname=L("NotAName")))
    ke_.deffacts(Person(name=L('name'), surname=L("name")))
    ke_.reset()
    ke_.run()
    assert executions == []
