import pytest


def test_activation_exists():
    try:
        from pyknow import activation
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_Activation_exists():
    from pyknow import activation

    assert hasattr(activation, 'Activation')


def test_Activation_is_class():
    from pyknow.activation import Activation

    assert isinstance(Activation, type)


def test_Activation_store_rule_and_facts():
    from pyknow.activation import Activation

    class S:
        pass

    a = Activation(rule=S, facts=[S, S])

    assert a.rule is S
    assert a.facts == [S, S]
