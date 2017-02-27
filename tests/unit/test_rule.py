""" Rule object tests """


import pytest
from conftest import random_types
from hypothesis import given

# pylint: disable=missing-docstring, invalid-name


def test_Rule_can_decorate_function():
    from pyknow.rule import Rule

    called = False

    @Rule()
    def myfunction():
        nonlocal called
        called = True

    myfunction()

    assert called


def test_Rule_can_decorate_function_with_one_parameter():
    from pyknow.rule import Rule

    called = False

    @Rule()
    def myfunction(x):
        nonlocal called
        called = True
        assert x is True

    myfunction(True)
    assert called


def test_Rule_can_decorate_function_with_multiple_positional_args():
    from pyknow.rule import Rule

    called = False

    @Rule()
    def myfunction(x, y, z):
        nonlocal called
        called = True
        assert x == 'x'
        assert y == 'y'
        assert z == 'z'

    myfunction('x', 'y', 'z')
    assert called


def test_Rule_can_decorate_function_with_mixed_args():
    from pyknow.rule import Rule

    called = False

    @Rule()
    def myfunction(x, y, z=None, a=None):
        nonlocal called
        called = True
        assert x == 'x'
        assert y == 'y'
        assert z is None
        assert a == 'a'

    myfunction('x', 'y', a='a')

    assert called


def test_Rule_decorated_function_raise_TypeError_on_bad_arguments():
    from pyknow.rule import Rule
    # pylint: disable=unused-argument, no-value-for-parameter

    called = False

    @Rule()
    def myfunction(x, y, z):
        nonlocal called
        called = True

    with pytest.raises(TypeError):
        myfunction(True, True)

    assert not called


def test_Rule_decorator_raise_AttributeError_if_called_without_function():
    from pyknow.rule import Rule

    with pytest.raises(AttributeError):
        Rule()()


def test_Rule_decorated_function_is_instance_of_Rule():
    from pyknow.rule import Rule

    @Rule()
    def myfunction():
        pass

    assert isinstance(myfunction, Rule)


def test_Rule_decorator_store_salience():
    from pyknow.rule import Rule

    @Rule(salience=10)
    def myfunction():
        pass

    assert myfunction.salience == 10


def test_Rule_get_activations_exists():
    from pyknow.rule import Rule

    assert hasattr(Rule, 'get_activations')


@given(data=random_types)
def test_Rule_get_activations_needs_factlist(data):
    from pyknow.rule import Rule

    r = Rule()

    with pytest.raises(ValueError):
        r.get_activations(data)


def test_Rule_empty_doesnt_match_empty_factlist():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList

    r = Rule()
    fl = FactList()

    assert tuple(r.get_activations(fl)) == tuple()


def test_Rule_empty_matches_with_initial_fact():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import InitialFact
    from pyknow.activation import Activation
    from pyknow.match import Capturation

    r = Rule()
    fl = FactList()
    fl.declare(InitialFact())
    assert Activation(None, (0,)) in list(r.get_activations(fl, Capturation()))


def test_Rule_with_empty_Fact_matches_all_Facts():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L
    from pyknow.activation import Activation

    r = Rule(Fact())
    fl = FactList()

    fl.declare(Fact(something=L(True)))
    fl.declare(Fact(something=L(False)))
    fl.declare(Fact(something=L(3)))

    activations = list(r.get_activations(fl))
    assert len(activations) == 3
    for i in range(3):
        assert Activation(None, (i, )) in activations


def test_Rule_multiple_criteria_generates_activation_with_matching_facts():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L

    r = Rule(Fact(a=L(1)), Fact(b=L(2)))
    fl = FactList()
    fl.declare(Fact(a=L(1)))
    fl.declare(Fact(b=L(2)))

    activations = list(r.get_activations(fl))
    assert len(activations) == 1
    assert {0, 1} == set(activations[0].facts)


def test_Rule_simple_testce():
    from pyknow.rule import Rule
    from pyknow.fact import Fact, T, L
    from pyknow.factlist import FactList

    r = Rule(Fact(a=T(lambda c, x: x.startswith('D'))))

    fl = FactList()
    fl.declare(Fact(a=L("David")))
    fl.declare(Fact(a=L("Penelope")))

    activations = list(r.get_activations(fl))

    assert len(activations) == 1

    assert {0} == set(activations[0].facts)
