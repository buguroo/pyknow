"""
    Basic tests for captured values
"""

import pytest
@pytest.mark.wip
def test_can_capture_values():
    """
        KnowledgeEngine has context
    """
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, Context, V, L
    from collections import defaultdict
    executions = []

    class Test(KnowledgeEngine):
        """ Test KE """
        @Rule(Fact(name=C("name_p")))
        def rule1(self):
            """ First rule, something=1 and something=2"""
            nonlocal executions
            print("1 - {}".format(id(self.context)))
            executions.append('rule1')

        @Rule(Fact(name=V("name_p")))
        def rule2(self):
            """ Second rule, only something=3 """
            nonlocal executions
            print("2 - {}".format(id(self.context)))
            executions.append('rule2')

    ke_ = Test()
    ke_.reset()

    to_declare = []

    to_declare.append(L(2))
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

    assert ke_.context == {"name": "name_p"}
