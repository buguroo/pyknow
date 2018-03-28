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

    ke.reset()
    ke.declare(Fact(a=1, b=1))
    ke.declare(Fact(a=2, b=3))
    ke.declare(Fact(a=3, b=2))

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

    ke.reset()
    ke.declare(Fact(a=1, b=2))
    ke.declare(Fact(a=2, b=2))
    ke.declare(Fact(a=3, b=3))

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
    from pyknow import KnowledgeEngine, Rule, Fact, DefFacts

    executions = 0

    class Test(KnowledgeEngine):
        @DefFacts()
        def test_deffacts(self):
            yield Fact(a=1)

        @Rule(Fact(a=1) & ~Fact(b=2))
        def test_fact_before_not(self):
            nonlocal executions
            executions +=1

    t = Test()
    t.reset()
    t.run()

    assert executions == 1

    t.retract(1)
    t.declare(Fact(a=1))
    t.run()
    assert executions == 2

    executions = 0

    class Test(KnowledgeEngine):
        @DefFacts()
        def test_deffacts(self):
            yield Fact(a=1)

        @Rule(~Fact(b=2) & Fact(a=1))
        def test_fact_after_not(self):
            nonlocal executions
            executions +=1

    t = Test()
    t.reset()
    t.run()

    assert executions == 1

    t.retract(1)
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
    t.reset()
    t.declare(f1, f2, f3)
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
    t.reset()
    t.declare(f1, f2, f3, f4)
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
    t.reset()
    t.declare(f1, f2, f3)
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
    t.reset()
    t.declare(f1, f2, f3)
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
    t.reset()
    t.declare(f1, f2, f3)
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


def test_fact_capture():
    from pyknow import KnowledgeEngine, Rule, Fact

    executed = None

    class KE(KnowledgeEngine):
        @Rule('myfact' << Fact())
        def r1(self, myfact):
            nonlocal executed
            executed = myfact

    ke = KE()
    ke.reset()
    f1 = ke.declare(Fact('data'))
    ke.run()
    assert executed is f1


def test_OR_not_allow_inside_FORALL_nor_EXISTS():
    from pyknow import KnowledgeEngine, Fact, Rule, FORALL, EXISTS, OR

    class KE(KnowledgeEngine):
        @Rule(EXISTS(OR(Fact(), Fact())))
        def r1(self):
            pass

    with pytest.raises(SyntaxError):
        KE()

    class KE(KnowledgeEngine):
        @Rule(EXISTS(OR(Fact(), Fact())))
        def r1(self):
            pass

    with pytest.raises(SyntaxError):
        KE()


def test_ANDNOT_reactivation():
    from pyknow import KnowledgeEngine, Fact, Rule, NOT, W

    class KE(KnowledgeEngine):
        @Rule(Fact(x='x' << W()),
              NOT(Fact(y='x' << W())))
        def r1(self):
            pass

    ke = KE()
    ke.reset()
    assert not ke.agenda.activations

    f1 = ke.declare(Fact(x=1))
    assert ke.agenda.activations

    ke.retract(f1)
    assert not ke.agenda.activations

    f2 = ke.declare(Fact(y=1))
    assert not ke.agenda.activations

    f3 = ke.declare(Fact(x=1))
    assert not ke.agenda.activations

    f4 = ke.declare(Fact(x=2))
    assert ke.agenda.activations

    ke.retract(f4)
    assert not ke.agenda.activations


def test_OR_inside_Rule():
    from pyknow import KnowledgeEngine, OR, Fact, Rule

    class KE(KnowledgeEngine):
        @Rule(Fact(1),
              OR(Fact('a'),
                 Fact('b')),
              OR(Fact('x'),
                 Fact('y')))
        def r1(self):
            pass

    ke = KE()
    ke.reset()
    assert len(ke.agenda.activations) == 0

    p0 = ke.declare(Fact(1))
    assert len(ke.agenda.activations) == 0

    p1 = ke.declare(Fact('a'))
    assert len(ke.agenda.activations) == 0

    p2 = ke.declare(Fact('x'))
    assert len(ke.agenda.activations) == 1

    ke.retract(p2)
    assert len(ke.agenda.activations) == 0

    p2 = ke.declare(Fact('y'))
    assert len(ke.agenda.activations) == 1

    ke.retract(p1)
    assert len(ke.agenda.activations) == 0

    p1 = ke.declare(Fact('b'))
    assert len(ke.agenda.activations) == 1

    ke.retract(p2)
    assert len(ke.agenda.activations) == 0

    p2 = ke.declare(Fact('x'))
    assert len(ke.agenda.activations) == 1

    ke.retract(p0)
    assert len(ke.agenda.activations) == 0


def test_nested_values_dict():
    from pyknow import KnowledgeEngine, Fact, Rule

    class KE(KnowledgeEngine):
        @Rule(Fact(key__with__nested__dicts=1))
        def r1(self):
            pass

    ke = KE()
    ke.reset()
    assert len(ke.agenda.activations) == 0

    p0 = ke.declare(Fact(key={"with": {"dicts": 1}}))
    assert len(ke.agenda.activations) == 0

    p1 = ke.declare(Fact(key={"with": {"nested": {"dicts": 1}}}))
    assert len(ke.agenda.activations) == 1


def test_nested_values_dict_and_lists():
    from pyknow import KnowledgeEngine, Fact, Rule

    class KE(KnowledgeEngine):
        @Rule(Fact(key__0__with__nested__1__dicts=1))
        def r1(self):
            pass

    ke = KE()
    ke.reset()
    assert len(ke.agenda.activations) == 0

    p0 = ke.declare(Fact(key={"with": {"nested": [{"other": 1}, {"dicts": 1}]}}))
    assert len(ke.agenda.activations) == 0

    p1 = ke.declare(Fact(key=[{"with": {"nested": [{"other": 1}, {"dicts": 1}]}}]))
    assert len(ke.agenda.activations) == 1
