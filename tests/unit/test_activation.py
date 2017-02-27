"""
Tests regarding activation object.
"""


def test_activation_has_facts():
    """ Check if activation has facts property """
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    assert hasattr(Activation(rule=Rule(), facts=tuple()), 'facts')


def test_activation_facts_only_tuple():
    """ Check if activation facts are required to be a tuple """
    from pyknow.activation import Activation
    from pyknow.rule import Rule
    import pytest
    with pytest.raises(ValueError):
        Activation(rule=Rule(), facts=list())


def test_activation_has_not_rule():
    """ Check if we can create an activation without rule """

    from pyknow.activation import Activation
    assert Activation(rule=None, facts=tuple())


def test_activation_sum():
    """ Check if we can sum two activations and the result is correct """

    from pyknow.activation import Activation
    act1 = Activation(rule=None, facts=(1, 2, 3, 3))
    act2 = Activation(rule=None, facts=(1, 2, 3, 4))
    act3 = act1 + act2
    assert act3.facts == (1, 2, 3, 4)


def test_activation_eq():
    """ Check if we can compare two activations """
    from pyknow.activation import Activation
    act1 = Activation(rule=None, facts=(1, 2, 3, 3))
    act2 = Activation(rule=None, facts=(1, 2, 3, 4))
    act3 = Activation(rule=None, facts=(1, 2, 3, 3))
    assert act1 != act2
    assert act1 == act3
