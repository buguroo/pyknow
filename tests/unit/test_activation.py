"""
Tests regarding activation object.
"""


def test_activation_has_facts():
    """ Check if activation has facts property """
    from pyknow.activation import Activation
    from pyknow import Rule
    assert hasattr(Activation(rule=Rule(), facts=tuple()), 'facts')


def test_activation_facts_only_tuple():
    """ Check if activation facts are required to be a tuple """
    from pyknow.activation import Activation
    from pyknow import Rule
    import pytest
    with pytest.raises(TypeError):
        Activation(rule=Rule(), facts=list())


def test_activation_eq():
    """ Check if we can compare two activations """
    from pyknow.activation import Activation
    from pyknow import Rule

    rule = Rule()

    act1 = Activation(rule=rule, facts=(1, 2, 3, 3))
    act2 = Activation(rule=rule, facts=(1, 2, 3, 4))
    act3 = Activation(rule=rule, facts=(1, 2, 3, 3))

    assert act1 != act2
    assert act1 == act3
