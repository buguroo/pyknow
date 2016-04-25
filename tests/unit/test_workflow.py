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
