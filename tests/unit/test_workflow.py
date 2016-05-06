import pytest
from hypothesis import given
from hypothesis import strategies as st


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
    ke.reset()

    to_declare = list(set(to_declare_random + [1, 2, 3]))
    shuffle(to_declare)
    print(to_declare)

    for i in to_declare:
        ke.declare(Fact(something=L(i)))

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
    ke_.reset()

    to_declare = []

    for i in range(1, 10):
        to_declare.append(L(i))

    to_declare = dict(enumerate(to_declare))

    for k, n in to_declare.items():
        ke_.declare(Fact(something=n))

    results = defaultdict(list)
    for activation in ke_.agenda.activations:
        results[''.join([str(to_declare[a - 1].resolve())
                         for a in activation.facts])].append(1)

    assert dict(results) == {'3': [1], '12': [1]}
    assert len(ke_.agenda.activations) == 2
    ke_.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1


def test_or_operator():
    """
        Test OR operator
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, OR
    from pyknow.fact import Fact, L
    import itertools

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(OR(Fact(something=L(1)),
              Fact(something=L(2))))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            pass

        @Rule(Fact(something=L(3)))
        def rule2(self):
            """ Second rule, only something=3 """
            pass

    static = ((1, 3), (1, 2), (1, 1, 2), (1, 3, 5))
    for test in static:
        ke_ = Test()
        ke_.reset()
        for val in test:
            ke_.declare(Fact(something=L(val)))
        assert len(ke_.agenda.activations) == 2

    ke_ = Test()
    ke_.reset()
    ke_.declare(Fact(something=L(1)))
    assert len(ke_.agenda.activations) == 1

    ke_ = Test()
    ke_.reset()
    ke_.declare(Fact(something=L(2)))
    assert len(ke_.agenda.activations) == 1

    dinamic = (1, 2, 3)
    for comb_len in range(1, 3):
        for combination in itertools.combinations(dinamic, comb_len):
            ke_ = Test()
            ke_.reset()
            for val in combination:
                ke_.declare(Fact(something=L(val)))
            assert len(ke_.agenda.activations) == comb_len


def test_ke_inheritance():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, L
    from pyknow.engine import KnowledgeEngine


    executed = False


    class Person(Fact):
        pass


    class Base(KnowledgeEngine):
        @Rule(Person(name='pepe'))
        def is_pepe(self):
            self.declare(Person(drinks="coffee"))


    class Test(Base):
        @Rule(Person(drinks="coffee"))
        def drinks_coffee(self):
            nonlocal executed
            executed = True


    ke_ = Test()
    ke_.declare(Person(name='pepe'))
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
        @Rule(Person(name="David"))
        def david(self):
            self.declare(Person(name="Pepe"))

        @Rule(Person(name="Pepe"))
        def pepe(self):
            nonlocal executed
            executed=True

    ke_ = Person_KE()
    ke_.declare(Person(name="David"))
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
        @Rule(Person(name="David"))
        def david(self):
            self.declare(Person(name="Pepe", apellido="stuff"))

        @Rule(Person(name="Pepe"))
        def pepe(self):
            nonlocal executed
            executed=True

    ke_ = Person_KE()
    ke_.declare(Person(name="David"))
    ke_.run()
    assert executed
