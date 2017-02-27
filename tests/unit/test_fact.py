"""
Fact methods
"""

import pytest
from hypothesis import given
from conftest import random_kwargs
# pylint: disable=invalid-name


def test_Fact_store_literal_value_and_keyset():
    """
    Check that, upon setting a fact value,
    we set its keyset and value
    """
    from pyknow.fact import Fact, L
    value = {'a': L(1), 'b': L(2)}
    fact = Fact(**value)
    assert fact.value == value
    assert set(value.keys()) == fact.keyset


@pytest.mark.parametrize("facttype", ("L", "C"))
def test_facts_equals_all_facttypes(facttype):
    """
    Check that we can create facts with all facttypes and they're equal
    """
    import pyknow.fact
    fact1 = pyknow.fact.Fact(a=getattr(pyknow.fact, facttype)('foo'))
    fact2 = pyknow.fact.Fact(a=getattr(pyknow.fact, facttype)('foo'))
    assert fact1 == fact2
    with pytest.raises(ValueError):
        pyknow.fact.Fact(a="Foo")


@pytest.mark.parametrize("facttype", ("L", "C"))
def test_facts_matches_all_facttypes_not_context(facttype):
    """
    Check that we can create facts with all value facttypes and they match
    (those facttypes that use context are excluded)
    """
    import pyknow.fact
    fact1 = pyknow.fact.Fact(a=getattr(pyknow.fact, facttype)('foo'))
    fact2 = pyknow.fact.Fact(a=pyknow.fact.L('foo'))
    assert fact1.matches(fact2, {})


def test_facts_produce_activations_without_capturation():
    """
    A fact produces activations if no capturations are provided
    """
    from pyknow.fact import Fact, L
    from pyknow.factlist import FactList
    from pyknow.match import Capturation

    flist = FactList()
    flist.declare(Fact(a=L(1)))
    caps = list(Fact(a=L(1)).get_activations(flist, Capturation()))
    assert len(caps) == 1


def test_facts_produce_activations_that_are_Activations():
    """
    A fact produces activations that are Activation objects
    """
    from pyknow.fact import Fact, L
    from pyknow.factlist import FactList
    from pyknow.match import Capturation
    from pyknow.activation import Activation

    flist = FactList()
    flist.declare(Fact(a=L(1)))
    caps = list(Fact(a=L(1)).get_activations(flist, Capturation()))
    assert len(caps) == 1
    assert isinstance(caps[0], Activation)
    assert caps[0].facts == (0,)


@given(kwargs=random_kwargs)
def test_empty_fact_match_all(kwargs):
    """ Empty fact matches against all. InitialFact should be this case """
    from pyknow.fact import Fact, L
    fact = Fact(**{a: L(b) for a, b in kwargs.items()})
    assert Fact().matches(fact, {})


def test_different_fact_types_do_not_match():
    """ Different derived classes don't match """
    # pylint: disable= too-few-public-methods
    from pyknow.fact import Fact

    class FactType0(Fact):
        """ Fake facttype """
        pass

    class FactType1(Fact):
        """ Fake facttype 2 """
        pass

    assert not FactType0().matches(FactType1(), {})
    assert not FactType1().matches(FactType0(), {})
