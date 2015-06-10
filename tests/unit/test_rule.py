import pytest


def test_rule_exists():
    try:
        from pyknow import rule
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_Rule_exists():
    from pyknow import rule

    assert hasattr(rule, 'Rule')


def test_Rule_is_class():
    from pyknow.rule import Rule

    assert isinstance(Rule, type)
