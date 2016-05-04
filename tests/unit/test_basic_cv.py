"""
    Basic tests for captured values
"""


def test_capture_to_valueset():
    """
        Test that captured values are added to capvalueset
    """
    from pyknow.fact import Fact, C
    fact = Fact(name=C('name'), name2=C('name2'))
    fact in fact  # Trigger matching
    assert len(fact.capvalueset) == 2


def test_capture_to_extcontext():
    """
        Test that a captured value is added to context, wich can
        be externally added so we'll be able to have a general context
        for all the facts in a rule
    """
    from pyknow.fact import Fact, C, L, Context
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    fact = Fact(name=C('stuff'))
    fact.context = Context()
    rule = Rule(fact)

    fl_ = FactList()
    fl_.declare(Fact(name=L('foo')))
    rule.get_activations(fl_)
    assert fact.context['main'].captured == {'name': 'stuff'}


def test_factlist_shouldnot_inherit_context():
    """
        Factlist we're comparing against should not get context.
        Only rules' facts should
    """
    from pyknow.fact import Fact, C, L, Context
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    fact = Fact(name=C('stuff'))
    context = Context()
    fact.context = context
    rule = Rule(fact)

    fl_ = FactList()
    fl_.declare(Fact(name=L('foo')))

    for activation in rule.get_activations(fl_):
        for fact in activation.facts:
            assert fl_._facts[fact].context['main'] is not context


def test_rulefacts_inherit_context():
    """
        After getting activations, thus comparing against all valuesets
        we should get a context having the captured values
    """
    from pyknow.fact import Fact, C, L, Context
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    fact = Fact(name=C('stuff'))
    fact.context = Context()
    rule = Rule(fact)

    fl_ = FactList()
    fl_.declare(Fact(name=L('foo')))

    rule.get_activations(fl_)
    assert rule.conds()

    for fact in rule.conds():
        assert fact.context['main'].captured == {'name': 'stuff'}


def test_rule_inherit_context():
    """
        After getting activations, thus comparing against all valuesets
        we should get a context having the captured values
    """
    from pyknow.fact import Fact, C, L, Context
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    fact = Fact(name=C('stuff'))
    rule = Rule(fact)
    rule.context = Context()

    fl_ = FactList()
    fl_.declare(Fact(name=L('foo')))

    rule.get_activations(fl_)
    assert rule.conds()

    for fact in rule.conds():
        assert fact.context['main'].captured == {'name': 'stuff'}


def test_rule_inherit_ke_context():
    """
        KnowledgeEngine has context and rules assigned to it inherit it
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
            executions.append('rule1')

        @Rule(Fact(name=V("name_p")))
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
            executions.append('rule1')

        @Rule(Fact(name=V("name_p")))
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

    print(ke_.context.captured)
