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


def test_TEST_1():
    from collections import Counter
    from pyknow import KnowledgeEngine, Rule, Fact, TEST, W

    executed = Counter()

    class Test(KnowledgeEngine):
        @Rule(Fact("a" << W()),
              Fact("b" << W()),
              TEST(lambda a, b: a > b))
        def is_greater(self, a, b):
            nonlocal executed
            executed[(a, b)] += 1

    t = Test()
    f1 = Fact(1)
    f2 = Fact(2)
    f3 = Fact(3)
    t.deffacts(f1, f2, f3)
    t.reset()
    t.run()

    assert len(executed) == 3
    assert (3, 2) in executed and executed[(3, 2)] == 1
    assert (3, 1) in executed and executed[(3, 1)] == 1
    assert (2, 1) in executed and executed[(2, 1)] == 1


def test_TEST_2():
    from collections import Counter
    from pyknow import KnowledgeEngine, Rule, Fact, TEST, W

    executed = Counter()

    class Test(KnowledgeEngine):
        @Rule(Fact("a" << W()),
              Fact("b" << W()),
              TEST(lambda a, b: a > b),
              Fact("c" << W()),
              TEST(lambda b, c: b > c))
        def is_greater(self, a, b, c):
            nonlocal executed
            executed[(a, b, c)] += 1

    t = Test()
    f1 = Fact(1)
    f2 = Fact(2)
    f3 = Fact(3)
    f4 = Fact(4)
    t.deffacts(f1, f2, f3, f4)
    t.reset()
    t.run()

    assert len(executed) == 4
    assert (4, 3, 2) in executed and executed[(4, 3, 2)] == 1
    assert (4, 3, 1) in executed and executed[(4, 3, 1)] == 1
    assert (4, 2, 1) in executed and executed[(4, 2, 1)] == 1
    assert (3, 2, 1) in executed and executed[(3, 2, 1)] == 1


def test_TEST_3():
    from collections import Counter
    from pyknow import KnowledgeEngine, Rule, Fact, TEST, W

    executed = 0

    class Test(KnowledgeEngine):
        @Rule(Fact("a" << W()),
              TEST(lambda a: isinstance(a, int)))
        def is_number(self, a):
            nonlocal executed
            executed += 1

    t = Test()
    f1 = Fact(1)
    f2 = Fact(2)
    f3 = Fact('a')
    t.deffacts(f1, f2, f3)
    t.reset()
    t.run()

    assert executed == 2


def test_TEST_4():
    from collections import Counter
    from pyknow import KnowledgeEngine, Rule, Fact, TEST, W

    executed = 0

    class Test(KnowledgeEngine):
        @Rule(TEST(lambda: True))
        def is_greater(self):
            nonlocal executed
            executed += 1

    t = Test()
    f1 = Fact(1)
    f2 = Fact(2)
    f3 = Fact(3)
    t.deffacts(f1, f2, f3)
    t.reset()
    t.run()

    assert executed == 1


def test_EXISTS_1():
    from pyknow import KnowledgeEngine, Rule, Fact, EXISTS

    executed = 0

    class Test(KnowledgeEngine):
        @Rule(EXISTS(Fact()))
        def any_fact_once(self):
            nonlocal executed
            executed += 1

    t = Test()
    f1 = Fact(1)
    f2 = Fact(2)
    f3 = Fact(3)
    t.deffacts(f1, f2, f3)
    t.reset()
    t.run()

    assert executed == 1


def test_FORALL_1():
    from pyknow import KnowledgeEngine, Rule, Fact, FORALL, W

    executed = 0

    class Test(KnowledgeEngine):
        @Rule(FORALL(Fact(key_a="k" << W()),
                     Fact(key_b="k" << W()),
                     Fact(key_c="k" << W())))
        def any_fact_once(self):
            nonlocal executed
            executed += 1

    t = Test()
    t.reset()
    t.run()

    t.declare(Fact(key_a=1))
    t.run()
    assert executed == 1
    t.declare(Fact(key_b=1))
    t.run()
    assert executed == 1
    t.declare(Fact(key_c=1))
    t.run()
    assert executed == 2

    t.declare(Fact(key_a=2))
    t.run()
    assert executed == 2
    t.declare(Fact(key_b=2))
    t.run()
    assert executed == 2
    t.declare(Fact(key_c=2))
    t.run()
    assert executed == 3
