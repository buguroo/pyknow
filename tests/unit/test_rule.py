""" Rule object tests """


import pytest

# pylint: disable=missing-docstring, invalid-name


def test_Rule_can_decorate_function():
    from pyknow import Rule

    called = False

    @Rule()
    def myfunction():
        nonlocal called
        called = True

    myfunction()

    assert called


def test_Rule_can_decorate_function_with_one_parameter():
    from pyknow import Rule

    called = False

    @Rule()
    def myfunction(x):
        nonlocal called
        called = True
        assert x is True

    myfunction(True)
    assert called


def test_Rule_can_decorate_function_with_multiple_positional_args():
    from pyknow import Rule

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
    from pyknow import Rule

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
    from pyknow import Rule
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
    from pyknow import Rule

    with pytest.raises(AttributeError):
        Rule()()


def test_Rule_decorated_function_is_instance_of_Rule():
    from pyknow import Rule

    @Rule()
    def myfunction():
        pass

    assert isinstance(myfunction, Rule)


def test_Rule_decorator_store_salience():
    from pyknow import Rule

    @Rule(salience=10)
    def myfunction():
        pass

    assert myfunction.salience == 10


@pytest.mark.wip
def test_rule_is_iterable():
    from pyknow import Rule
    from pyknow import Fact

    rule_ = Rule(Fact(a=1), Fact(a=2))
    assert next(rule_) == Fact(a=1)
    assert next(rule_) == Fact(a=2)
