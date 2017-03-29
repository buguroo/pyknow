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
    from pyknow.activation import Activation

    assert Activation(None, []) == Activation(None, [])
    assert (None, []) != Activation(None, [])


def test_activation_in_set():
    from pyknow.activation import Activation

    assert Activation(None, []) in {Activation(None, [])}
