import pytest
from hypothesis import given
from hypothesis import strategies as st

from conftest import random_kwargs


def test_fact_exists():
    try:
        from pyknow import fact
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_fact_Fact_exists():
    from pyknow import fact

    assert hasattr(fact, 'Fact')


def test_Fact_is_class():
    from pyknow.fact import Fact

    assert isinstance(Fact, type)


def test_Fact_store_literal_value():
    from pyknow.fact import Fact, L

    value = {'a': L(1), 'b': L(2)}

    f = Fact(**value)

    assert f.value == value


def test_Fact_store_literal_valueset():
    from pyknow.fact import Fact, L

    value = {'a': L(1), 'b': L(2)}

    f = Fact(**value)

    assert set(value.items()) == f.valueset


def test_Fact_store_literal_keyset():
    from pyknow.fact import Fact, L

    value = {'a': L(1), 'b': L(2)}

    f = Fact(**value)

    assert set(value.keys()) == f.keyset


@given(kwargs=random_kwargs)
def test_Fact_equality_literal(kwargs):
    from pyknow.fact import Fact, L
    kwargs = {a: L(b) for a, b in kwargs.items()}

    f0 = Fact(**kwargs)
    f1 = Fact(**kwargs)

    assert f0 == f1


def test_facts_cant_accept_not_FactType():
    from pyknow.fact import Fact
    with pytest.raises(TypeError):
        Fact(a="foo")
    with pytest.raises(TypeError):
        Fact(a=False)
    with pytest.raises(TypeError):
        Fact(a=1)


def test_facts_accept_FactType_L():
    """
        This test is actually redundant...
        As soon as I add new types I'll rewrite these
    """
    from pyknow.fact import Fact, L
    assert Fact(a=L('foo'))
