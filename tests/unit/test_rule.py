import pytest


def test_rule_exists():
    try:
        from pyknow import rule
    except ImportError:
        assert False
    else:
        assert True


def test_rule_Rule_exists():
    from pyknow import rule
    assert hasattr(rule, 'Rule')


def test_rule_Rule_is_class():
    from pyknow import rule
    assert isinstance(rule.Rule, type)


def test_Rule_needs___eval__():
    from pyknow.rule import Rule

    with pytest.raises(TypeError):
        Rule()


def test_Rule_subclass_with___eval__():
    from pyknow.rule import Rule

    class MyRuleWithEval(Rule):
        def __eval__(self):
            pass

    assert MyRuleWithEval()


def test_Rule_is_decorator(DRule):
    @DRule()
    def my_rule():
        pass

    assert my_rule()


def test_Rule_decorated_returns_tuple(DRule):
    @DRule()
    def my_rule():
        pass

    res = my_rule()

    assert isinstance(res, tuple)


def test_Rule_decorated_returns_function_in_second_position(DRule):
    @DRule()
    def my_rule():
        pass

    _, second = my_rule()

    assert callable(second)


def test_Rule_decorated_returns_bool_in_first_position(DRule):
    @DRule()
    def my_rule():
        pass

    first, _ = my_rule()

    assert isinstance(first, bool)


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


def test_rule_FactState():
    from pyknow import rule 

    assert hasattr(rule, 'FactState')


def test_rule_FactState_is_enum():
    from pyknow.rule import FactState
    from enum import Enum

    assert issubclass(FactState, Enum)


def test_rule_FactState_has_states():
    from pyknow.rule import FactState

    assert hasattr(FactState, 'DEFINED')
    assert hasattr(FactState, 'NOT_DEFINED')


def test_Rule__check_pattern_for_state_DEFINED_True(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'something': None})
    assert match is True


def test_Rule__check_pattern_for_state_DEFINED_False(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'notsomething': None})
    assert match is False


def test_Rule__check_pattern_for_state_NOT_DEFINED_True(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.NOT_DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'something': None})
    assert match is False


def test_Rule__check_pattern_for_state_NOT_DEFINED_False(SRule):
    from pyknow.rule import FactState as fs

    @SRule(something=fs.NOT_DEFINED)
    def my_rule():
        pass

    match, _ = my_rule({'notsomething': None})
    assert match is True


def test_Rule__check_pattern_with_callable_True(SRule):
    @SRule(something=lambda f: f['something'] is True)
    def my_rule():
        pass

    match, _ = my_rule({'something': True})
    assert match is True


def test_Rule__check_pattern_with_callable_False(SRule):
    @SRule(something=lambda f: f['something'] is True)
    def my_rule():
        pass

    match, _ = my_rule({'something': False})
    assert match is False 


def test_Rule__check_pattern_with_callable_UNDEFINED(SRule):
    @SRule(something=lambda x: x['something'] is True)
    def my_rule():
        pass

    match, _ = my_rule({'this_is_not_something': False})
    assert match is False 


def test_Rule__check_pattern_with_value(SRule):
    @SRule(something='myvalue')
    def my_rule():
        pass

    match, _ = my_rule({'something': 'myvalue'})
    assert match is True


def test_Rule__check_pattern_with_value_but_OTHER(SRule):
    @SRule(something='myvalue')
    def my_rule():
        pass

    match, _ = my_rule({'this_is_not_something': 'myvalue'})
    assert match is False


def test_Rule__check_args(RRule):
    @RRule((lambda f: 'a'),
           (lambda f: 'b'))
    def my_rule():
        pass

    match, _ = my_rule({})
    assert match == ['a', 'b']


def test_Rule__check_args_get_facts(RRule):
    FACTS = {'A': 'a'}

    @RRule(lambda f: f is FACTS)
    def my_rule():
        pass

    match, _ = my_rule(FACTS)
    assert match == [True]


def test_Rule_not_decorating(DRule):

    res = DRule(lambda x: True)
    match, _ = res()
    assert match is True


def test_Rule_not_decorating_pass_facts(DRule):

    FACTS = {'A': 'a'}

    res = DRule(lambda f: f is FACTS)
    match, _ = res(FACTS)
    assert match
