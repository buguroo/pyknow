import pytest
from hypothesis import given
from hypothesis import strategies as st

@pytest.mark.wip
def test_fact_exists():
    try:
        from pyknow import fact
    except ImportError as exc:
        assert False, exc
    else:
        assert True

@pytest.mark.wip
def test_fact_Fact_exists():
    from pyknow import fact

    assert hasattr(fact, 'Fact')

@pytest.mark.wip
def test_Fact_is_class():
    from pyknow.fact import Fact

    assert isinstance(Fact, type)

@pytest.mark.wip
def test_Fact_store_value():
    from pyknow.fact import Fact

    value = {'a': 1, 'b': 2}

    f = Fact(**value)

    assert f.value == value

@pytest.mark.wip
def test_Fact_store_valueset():
    from pyknow.fact import Fact

    value = {'a': 1, 'b': 2}

    f = Fact(**value)

    assert set(value.items()) == f.valueset

@pytest.mark.wip
def test_Fact_store_keyset():
    from pyknow.fact import Fact

    value = {'a': 1, 'b': 2}

    f = Fact(**value)

    assert set(value.keys()) == f.keyset
