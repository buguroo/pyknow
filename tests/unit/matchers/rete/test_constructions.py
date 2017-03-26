import pytest


def test_self_referencing_fact():
    from pyknow import KnowledgeEngine, Rule, Fact, W

    result = []

    class Test(KnowledgeEngine):
        @Rule(Fact(a=W('X'), b=W('X')))
        def rule1(self, X):
            nonlocal result
            result.append(X)

    ke = Test()

    ke.deffacts(Fact(a=1, b=1))
    ke.deffacts(Fact(a=2, b=3))
    ke.deffacts(Fact(a=3, b=2))

    ke.reset()
    ke.run()

    assert result == [1]


def test_self_referencing_fact_with_negation():
    from pyknow import KnowledgeEngine, Rule, Fact, W

    result = []

    class Test(KnowledgeEngine):
        @Rule(Fact(a=W('X'), b=~W('X')))
        def rule1(self, X):
            nonlocal result
            result.append(X)

    ke = Test()

    ke.deffacts(Fact(a=1, b=2))
    ke.deffacts(Fact(a=2, b=2))
    ke.deffacts(Fact(a=3, b=3))

    ke.reset()
    ke.run()

    assert result == [1]


def test_or_with_multiple_nots_get_multiple_activations():
    from pyknow import KnowledgeEngine, Rule, Fact


    executions = 0

    class Test(KnowledgeEngine):
        @Rule(~Fact(a=1) | ~Fact(a=2) | ~Fact(a=3))
        def test(self):
            nonlocal executions
            executions += 1

    t = Test()
    t.reset()
    t.run()

    assert executions == 3


def test_initial_not_vs_and_not():
    from pyknow import KnowledgeEngine, Rule, Fact

    executions = 0

    class Test(KnowledgeEngine):
        @Rule(Fact(a=1) & ~Fact(b=2))
        def test_fact_before_not(self):
            nonlocal executions
            executions +=1

    t = Test()
    f1 = Fact(a=1)
    t.deffacts(f1)
    t.reset()
    t.run()

    assert executions == 1

    t.retract(f1)
    t.declare(Fact(a=1))
    t.run()
    assert executions == 2

    executions = 0

    class Test(KnowledgeEngine):
        @Rule(~Fact(b=2) & Fact(a=1))
        def test_fact_after_not(self):
            nonlocal executions
            executions +=1

    t = Test()
    f1 = Fact(a=1)
    t.deffacts(f1)
    t.reset()
    t.run()

    assert executions == 1

    t.retract(f1)
    t.declare(Fact(a=1))
    t.run()
    assert executions == 2
