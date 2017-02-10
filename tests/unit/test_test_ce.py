def test_basic_ce():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L, T

    r = Rule(Fact(name=T(lambda c, x: x.startswith('D'))))
    fl = FactList()

    fl.declare(Fact(name=L("David")))
    fl.declare(Fact(name=L("Penelope")))
    fl.declare(Fact(name=L("Daniel")))

    activations = r.get_activations(fl)
    assert len(activations) == 2


def test_V_with_context():
    """
    Basic test V operator
    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, V
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
    engine.declare(Fact(name="David", surname="Francos"))
    engine.declare(Fact(name="Rodriguez", surname="Rodriguez"))
    engine.run()
    assert executions == ["Rodriguez"]


def test_N_with_context():
    """
    Basic test N operator
    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, N
    from pyknow.engine import KnowledgeEngine

    executions = []

    class PeopleEngine(KnowledgeEngine):
        @Rule(Fact(name=C('name_t'), surname=N('name_t')))
        def name_is_NOT_same_as_surname(self, name_t):
            nonlocal executions
            executions.append(name_t)
            print("Name {} has not the same surname".format(name_t))

    engine = PeopleEngine()
    engine.reset()
    engine.declare(Fact(name="David", surname="Rodriguez"))
    engine.declare(Fact(name="Pedro", surname="Pedro"))
    engine.declare(Fact(name="David", surname="Pedro"))
    engine.run()
    assert executions == ["David"]

def test_C_with_context_alone():
    """
    Basic test C operator alone
    """
    from pyknow.rule import Rule
    from pyknow.fact import Fact, C, V
    from pyknow.engine import KnowledgeEngine

    executions = []

    class PeopleEngine(KnowledgeEngine):
        @Rule(Fact(name=C('name_t')))
        def name_is_same_as_surname(self, name_t):
            nonlocal executions
            executions.append(name_t)

    engine = PeopleEngine()
    engine.reset()
    engine.declare(Fact(name="David", surname="Francos"))
    engine.declare(Fact(name="Rodriguez", surname="Rodriguez"))
    engine.run()
    assert len(executions) == 2


