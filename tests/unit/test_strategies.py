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
    from pyknow.strategies import Strategy

    assert isinstance(Strategy, type)


def test_Strategy_is_abstract():
    from pyknow.strategies import Strategy

    with pytest.raises(TypeError):
        Strategy()


def test_Depth_exists():
    from pyknow import strategies

    assert hasattr(strategies, 'Depth')


def test_Depth_is_Strategy():
    from pyknow.strategies import Depth, Strategy

    assert issubclass(Depth, Strategy)


def test_Depth_has_update_agenda():
    from pyknow.strategies import Depth
    assert hasattr(Depth(), 'update_agenda')


def test_Depth_update_agenda_no_facts_returns_empty_agenda():
    from pyknow.strategies import Depth
    from pyknow.agenda import Agenda

    st = Depth()
    a = Agenda()

    st.update_agenda(a, set())

    assert not a.activations


def test_Depth_update_agenda_activations_to_agenda():
    from pyknow.strategies import Depth
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(rule=Rule(), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(rule=Rule(), facts=(2, ), contexts=(2, tuple()))

    a = Agenda()

    st = Depth()
    st.update_agenda(a, {act1, act2})

    assert act1 in a.activations
    assert act2 in a.activations


def test_Depth_update_agenda_asertion_order_affects_agenda_order_1():
    from pyknow.strategies import Depth
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(rule=Rule(), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(rule=Rule(), facts=(2, ), contexts=(1, tuple()))
    first = {act1, act2}

    act3 = Activation(rule=Rule(), facts=(3, ), contexts=(1, tuple()))
    act4 = Activation(rule=Rule(), facts=(4, ), contexts=(1, tuple()))
    second = {act3, act4}

    a = Agenda()

    st = Depth()

    st.update_agenda(a, first)
    st.update_agenda(a, second)

    left, right = set(list(a.activations)[:2]), set(list(a.activations)[2:])

    assert left == second
    assert right == first


def test_Depth_update_agenda_asertion_order_affects_agenda_order_2():
    from pyknow.strategies import Depth
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(rule=Rule(), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(rule=Rule(), facts=(2, ), contexts=(1, tuple()))
    first = {act1, act2}

    act3 = Activation(rule=Rule(), facts=(3, ), contexts=(1, tuple()))
    act4 = Activation(rule=Rule(), facts=(4, ), contexts=(1, tuple()))
    second = {act3, act4}

    a = Agenda()

    st = Depth()

    st.update_agenda(a, second)
    st.update_agenda(a, first)

    left, right = set(list(a.activations)[:2]), set(list(a.activations)[2:])

    assert left == first
    assert right == second


def test_Depth_update_agenda_different_salience():
    from random import shuffle

    from pyknow.strategies import Depth
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(
        rule=Rule(salience=1), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(
        rule=Rule(salience=2), facts=(2, ), contexts=(1, tuple()))
    act3 = Activation(
        rule=Rule(salience=3), facts=(3, ), contexts=(1, tuple()))
    act4 = Activation(
        rule=Rule(salience=4), facts=(4, ), contexts=(1, tuple()))

    acts = [act1, act2, act3, act4]
    shuffle(acts)

    st = Depth()
    a = Agenda()

    for act in acts:
        st.update_agenda(a, [act])

    order = list(a.activations)
    assert (order.index(act4) < order.index(act3) <
            order.index(act2) < order.index(act1))


@pytest.mark.parametrize("strategy", ['Depth'])
def test_Strategy_update_agenda_doesnt_add_executed_activations(strategy):
    from pyknow import strategies
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(rule=Rule(), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(rule=Rule(), facts=(2, ), contexts=(1, tuple()))

    acts = [act1, act2]

    st = getattr(strategies, strategy)()
    a = Agenda()
    a.executed.add(act1)

    st.update_agenda(a, acts)

    assert act1 not in a.activations
    assert act2 in a.activations


@pytest.mark.parametrize("strategy", ['Depth'])
def test_Strategy_update_agenda_update_executed(strategy):
    from pyknow import strategies
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    from pyknow.agenda import Agenda

    act1 = Activation(rule=Rule(), facts=(1, ), contexts=(1, tuple()))
    act2 = Activation(rule=Rule(), facts=(2, ), contexts=(1, tuple()))

    st = getattr(strategies, strategy)()
    a = Agenda()
    a.executed.add(act1)

    st.update_agenda(a, [act2])

    assert act1 not in a.executed
