import pytest


def test_conditionalelement_exists():
    try:
        from pyknow import conditionalelement
    except ImportError as exc:
        assert False, exc


@pytest.mark.parametrize('name', ['AND',
                                  'OR',
                                  'NOT',
                                  'TEST',
                                  'EXISTS',
                                  'FORALL'])
def test_existence_of_conditional_elements(name):
    from pyknow import conditionalelement

    assert hasattr(conditionalelement, name)
