import pytest

@pytest.mark.wip
def test_rule_exists():
    try:
        from pyknow import rule
    except ImportError:
        assert False
    else:
        assert True

@pytest.mark.wip
def test_rule_Rule_exists():
    from pyknow import rule
    assert hasattr(rule, 'Rule')

@pytest.mark.wip
def test_rule_Rule_is_class():
    from pyknow import rule
    assert isinstance(rule.Rule, type)

@pytest.mark.wip
def test_Rule_needs___eval__():
    from pyknow.rule import Rule

    with pytest.raises(TypeError):
        Rule()

@pytest.mark.wip
def test_Rule_subclass_with___eval__():
    from pyknow.rule import Rule

    class MyRuleWithEval(Rule):
        def __eval__(self):
            pass

    assert MyRuleWithEval()

@pytest.mark.wip
def test_Rule_is_decorator(DRule):
    @DRule()
    def my_rule():
        pass

    assert my_rule()

@pytest.mark.wip
def test_Rule_decorated_returns_tuple(DRule):
    @DRule()
    def my_rule():
        pass

    res = my_rule()

    assert isinstance(res, tuple)

@pytest.mark.wip
def test_Rule_decorated_returns_function_in_second_position(DRule):
    @DRule()
    def my_rule():
        pass

    _, second = my_rule()

    assert callable(second)

@pytest.mark.wip
def test_Rule_decorated_returns_bool_in_first_position(DRule):
    @DRule()
    def my_rule():
        pass

    first, _ = my_rule()

    assert isinstance(first, bool)

@pytest.mark.wip
def test_Rule_decorator_pass_arguments(DRule):
    @DRule()
    def my_rule(*args, **kwargs):
        return (args, kwargs)

    facts=None
    args = (1, 2, 3)
    kwargs = {'A': 'a', 'B': 'b', 'C': 'c'}

    res = my_rule(facts, *args, **kwargs)
    _, fn = res

    assert (args, kwargs) == fn()

@pytest.mark.wip
def test_rule_FactState():
    from pyknow import rule 

    assert hasattr(rule, 'FactState')

@pytest.mark.wip
def test_rule_FactState_is_enum():
    from pyknow.rule import FactState
    from enum import Enum

    assert issubclass(FactState, Enum)

@pytest.mark.wip
def test_rule_FactState_has_states():
    from pyknow.rule import FactState

    assert hasattr(FactState, 'DEFINED')
    assert hasattr(FactState, 'NOT_DEFINED')

@pytest.mark.wip
def test_Rule__check_for_state_DEFINED_True(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'something': None})
    assert match is True

@pytest.mark.wip
def test_Rule__check_for_state_DEFINED_False(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'notsomething': None})
    assert match is False

@pytest.mark.wip
def test_Rule__check_for_state_NOT_DEFINED_True(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.NOT_DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'something': None})
    assert match is False

@pytest.mark.wip
def test_Rule__check_for_state_NOT_DEFINED_False(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.NOT_DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'notsomething': None})
    assert match is True

@pytest.mark.wip
def test_Rule__check_with_callable_True(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=lambda x: x is True)
    def my_rule():
        pass

    match, _ = my_rule({'something': True})
    assert match is True

@pytest.mark.wip
def test_Rule__check_with_callable_False(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=lambda x: x is True)
    def my_rule():
        pass

    match, _ = my_rule({'something': False})
    assert match is False 

@pytest.mark.wip
def test_Rule__check_with_callable_UNDEFINED(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=lambda x: x is True)
    def my_rule():
        pass

    match, _ = my_rule({'this_is_not_something': False})
    assert match is False 

@pytest.mark.wip
def test_Rule__check_with_value(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something='myvalue')
    def my_rule():
        pass

    match, _ = my_rule({'something': 'myvalue'})
    assert match is True

@pytest.mark.wip
def test_Rule__check_with_value_but_OTHER(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something='myvalue')
    def my_rule():
        pass

    match, _ = my_rule({'this_is_not_something': 'myvalue'})
    assert match is False
