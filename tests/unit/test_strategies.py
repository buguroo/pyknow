import pytest


def test_strategies_exists():
    try:
        from pyknow import strategies
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_Strategy_exists():
    from pyknow import strategies

    assert hasattr(strategies, 'Strategy')


def test_Strategy_is_class():
    from pyknow.abstract import Strategy

    assert isinstance(Strategy, type)


def test_Strategy_is_abstract():
    from pyknow.abstract import Strategy

    with pytest.raises(TypeError):
        Strategy()


def test_DepthStrategy_exists():
    from pyknow import strategies

    assert hasattr(strategies, 'DepthStrategy')


def test_DepthStrategy_is_Strategy():
    from pyknow.strategies import DepthStrategy, Strategy

    assert issubclass(DepthStrategy, Strategy)


def test_DepthStrategy_has_update_agenda():
    from pyknow.strategies import DepthStrategy
    assert hasattr(DepthStrategy(), 'update_agenda')


def test_DepthStrategy_update_agenda_no_facts_returns_empty_agenda():
    from pyknow.strategies import DepthStrategy
    from pyknow.agenda import Agenda

    st = DepthStrategy()
    a = Agenda()

    st.update_agenda(a, [], [])

    assert not a.activations


def test_DepthStrategy_update_agenda_activations_to_agenda():
    from pyknow.strategies import DepthStrategy
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow.agenda import Agenda
    from pyknow import Fact
    from pyknow.factlist import FactList

    fl = FactList()
    f1 = Fact(1)
    fl.declare(f1)
    f2 = Fact(2)
    fl.declare(f2)

    act1 = Activation(rule=Rule(), facts=(f1, ))
    act2 = Activation(rule=Rule(), facts=(f2, ))

    a = Agenda()

    st = DepthStrategy()
    st.update_agenda(a, [act1, act2], [])

    assert act1 in a.activations
    assert act2 in a.activations


def test_DepthStrategy_update_agenda_assertion_order_affects_agenda_order_1():
    from pyknow.strategies import DepthStrategy
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow.agenda import Agenda
    from pyknow import Fact
    from pyknow.factlist import FactList

    fl = FactList()

    f1 = Fact(1)
    fl.declare(f1)

    f2 = Fact(2)
    fl.declare(f2)

    f3 = Fact(3)
    fl.declare(f3)

    f4 = Fact(4)
    fl.declare(f4)

    act1 = Activation(rule=Rule(), facts=(f1, ))
    act2 = Activation(rule=Rule(), facts=(f2, ))
    first = [act1, act2]

    act3 = Activation(rule=Rule(), facts=(f3, ))
    act4 = Activation(rule=Rule(), facts=(f4, ))
    second = [act3, act4]

    a = Agenda()

    st = DepthStrategy()

    st.update_agenda(a, first, [])
    assert a.activations == first

    st.update_agenda(a, second, first)
    assert a.activations == second


def test_DepthStrategy_update_agenda_asertion_order_affects_agenda_order_2():
    from pyknow.strategies import DepthStrategy
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow.agenda import Agenda
    from pyknow import Fact
    from pyknow.factlist import FactList

    fl = FactList()

    f1 = Fact(1)
    fl.declare(f1)

    f2 = Fact(2)
    fl.declare(f2)

    f3 = Fact(3)
    fl.declare(f3)

    f4 = Fact(4)
    fl.declare(f4)

    act1 = Activation(rule=Rule(), facts=(f1, ))
    act2 = Activation(rule=Rule(), facts=(f2, ))
    first = [act1, act2]

    act3 = Activation(rule=Rule(), facts=(f3, ))
    act4 = Activation(rule=Rule(), facts=(f4, ))
    second = [act3, act4]

    a = Agenda()

    st = DepthStrategy()

    st.update_agenda(a, second, [])
    assert a.activations == second

    st.update_agenda(a, first, second)
    assert a.activations == first


def test_DepthStrategy_update_agenda_asertion_order_affects_agenda_order_3():
    """

    From Clips docs on Depth Strategy::

      Newly activated rules are placed above all rules of the same salience.
      For example, given that facta activates rule1 and rule2 and factb
      activates rule3 and rule4, then if facta is asserted before factb, rule3
      and rule4 will be above rule1 and rule2 on the agenda. However, the
      position of rule1 relative to rule2 and rule3 relative to rule4 will be
      arbitrary.

    """
    from pyknow.strategies import DepthStrategy
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow.agenda import Agenda
    from pyknow import Fact
    from pyknow.factlist import FactList

    fl = FactList()

    f1 = Fact(1)
    fl.declare(f1)

    f2 = Fact(2)
    fl.declare(f2)

    act1 = Activation(rule=Rule(), facts=(f1, ))
    act2 = Activation(rule=Rule(), facts=(f1, ))
    act3 = Activation(rule=Rule(), facts=(f2, ))
    act4 = Activation(rule=Rule(), facts=(f2, ))

    a = Agenda()

    st = DepthStrategy()

    st.update_agenda(a, [act1, act2, act3, act4], [])
    order = list(a.activations)

    assert (order.index(act4) > order.index(act1)
            and order.index(act4) > order.index(act2))
    assert (order.index(act3) > order.index(act1)
            and order.index(act3) > order.index(act2))


def test_DepthStrategy_update_agenda_different_salience():
    from random import shuffle

    from pyknow.strategies import DepthStrategy
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow import Fact
    from pyknow.agenda import Agenda
    from pyknow.factlist import FactList

    flist = FactList()

    f1 = Fact(1)
    flist.declare(f1)

    f2 = Fact(2)
    flist.declare(f2)

    f3 = Fact(3)
    flist.declare(f3)

    f4 = Fact(4)
    flist.declare(f4)

    act1 = Activation(rule=Rule(salience=1), facts=(f1, ))
    act2 = Activation(rule=Rule(salience=2), facts=(f2, ))
    act3 = Activation(rule=Rule(salience=3), facts=(f3, ))
    act4 = Activation(rule=Rule(salience=4), facts=(f4, ))

    acts = [act1, act2, act3, act4]
    shuffle(acts)

    st = DepthStrategy()
    a = Agenda()

    for act in acts:
        st.update_agenda(a, acts, [])

    order = list(a.activations)
    assert (order.index(act4)
            > order.index(act3)
            > order.index(act2)
            > order.index(act1))
