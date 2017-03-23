"""
Tests regarding activation object.
"""


def test_activation_has_facts():
    """ Check if activation has facts property """
    from pyknow.activation import Activation
    from pyknow import Rule
    assert hasattr(Activation(rule=Rule(), facts=[]), 'facts')


def test_activation_facts_only_iterable():
    """ Check if activation facts are required to be a tuple """
    from pyknow.activation import Activation
    from pyknow import Rule
    import pytest

    # SHOULD NOT RAISE
    Activation(rule=Rule(), facts=tuple())
    Activation(rule=Rule(), facts=list())
    Activation(rule=Rule(), facts=dict())

    with pytest.raises(TypeError):
        Activation(rule=Rule(), facts=None)


def test_activation_eq():
    """ Check if we can compare two activations """
    from pyknow.activation import Activation
    from pyknow import Rule
    from pyknow.factlist import FactList
    from pyknow import Fact

    fl = FactList()
    f1 = Fact(1)
    fl.declare(f1)
    f2 = Fact(2)
    fl.declare(f2)
    f3 = Fact(3)
    fl.declare(f3)
    f4 = Fact(4)
    fl.declare(f4)

    rule = Rule()

    act1 = Activation(rule=rule, facts=(f1, f2, f3, f3))
    act2 = Activation(rule=rule, facts=(f1, f2, f3, f4))
    act3 = Activation(rule=rule, facts=(f1, f2, f3, f3))

    assert act1 != act2
    assert act1 == act3
