import pytest


def test_fact_decorator_exists():
    import pyknow
    assert hasattr(pyknow, 'fact')


def test_fact_decorator_returns_tuple():
    import pyknow

    @pyknow.fact
    def my_fact():
        pass

    res = my_fact()

    assert isinstance(res, tuple)


def test_fact_decorator_returns_function_wrapping_decorated_function():
    import pyknow

    was_called = False

    def my_fact():
        nonlocal was_called
        was_called = True

    _, fn = pyknow.fact(my_fact)()

    fn()

    assert was_called


def test_fact_decorator_accepts_kwargs():
    import pyknow

    @pyknow.fact(something='value')
    def my_fact():
        pass

    res = my_fact()
    _, fn = res
    assert callable(fn)


def test_fact_decorated_function_accepts_facter_like_object():
    import pyknow

    my_facter = {}

    @pyknow.fact()
    def my_fact(something):
        return something

    res = my_fact(my_facter)
    _, fn = res

    assert fn() is my_facter


def test_fact_tuple_first_member_is_bool__nocall():
    import pyknow

    @pyknow.fact
    def my_fact():
        pass

    res = my_fact()
    is_asserted, _ = res

    assert isinstance(is_asserted, bool)


def test_fact_tuple_first_member_is_bool__call_withoutparams():
    import pyknow

    @pyknow.fact()
    def my_fact():
        pass

    res = my_fact()
    is_asserted, _ = res

    assert isinstance(is_asserted, bool)


def test_fact_tuple_first_member_is_bool__call_withparams():
    import pyknow

    @pyknow.fact(param1='value')
    def my_fact():
        pass

    res = my_fact()
    is_asserted, _ = res

    assert isinstance(is_asserted, bool)


def test_fact_if_defined__returns_True():
    import pyknow

    @pyknow.fact(if_defined='otherfact')
    def my_fact():
        pass

    res = my_fact({'otherfact': 'value'})
    is_asserted, _ = res

    assert is_asserted


def test_fact_if_defined__returns_False():
    import pyknow

    @pyknow.fact(if_defined='otherfact')
    def my_fact():
        pass

    res = my_fact({'nothing': 'value'})
    is_asserted, _ = res

    assert not is_asserted


def test_fact_if_defined__without_facts_returns_False():
    import pyknow

    @pyknow.fact(if_defined='otherfact')
    def my_fact():
        pass

    res = my_fact()
    is_asserted, _ = res

    assert not is_asserted
