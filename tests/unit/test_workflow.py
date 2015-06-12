import pytest
from hypothesis import given
from hypothesis import strategies as st


@given(to_declare_random=st.lists(st.integers()))
def test_rules_are_executed_once(to_declare_random):
    from random import shuffle
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact

    executions = []

    class Test(KnowledgeEngine):
        @Rule(Fact(something=1),
              Fact(something=2))
        def rule1(self):
            nonlocal executions
            executions.append('rule1')

        @Rule(Fact(something=3))
        def rule2(self):
            nonlocal executions
            executions.append('rule2')
        
    ke = Test()
    ke.reset()

    to_declare = to_declare_random + [1, 2, 3]
    shuffle(to_declare)

    for i in to_declare:
        ke.declare(Fact(something=i))
    
    assert len(ke.agenda.activations) == 2
    ke.run()

    assert executions.count('rule1') == 1
    assert executions.count('rule2') == 1
