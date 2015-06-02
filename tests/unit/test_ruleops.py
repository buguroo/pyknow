from hypothesis import given
from hypothesis import strategies as st
import pytest

#
# AND
#
def test_AND_exists():
    from pyknow import rule
    assert hasattr(rule, 'AND')


def test_AND_is_Rule_subclass():
    from pyknow.rule import Rule, AND
    assert issubclass(AND, Rule)


@given(args=st.lists(st.booleans()))
def test_AND_logic_args(args):
    from pyknow.rule import AND

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]

    assert AND(*_args)({}) == (bool(all(args)), None)


@given(patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_AND_logic_patterns(patterns):
    from pyknow.rule import AND

    def ret(elem):
        def check(_):
            return elem
        return check
        
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert AND(**kwargs)(patterns) == (bool(all(patterns.values())), None)


@given(args=st.lists(st.booleans()),
       patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_AND_logic_args_and_patterns(args, patterns):
    from pyknow.rule import AND

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert AND(*_args, **kwargs)(patterns) == (bool((all(args) and
                                                     all(patterns.values()))),
                                               None)


@given(args=st.lists(st.booleans()))
def test_AND_nesting(LRule, args):
    from pyknow.rule import AND
    _args = [LRule(x) for x in args]

    assert AND(*_args)({}) == (all(args), None)

#
# OR
#
def test_OR_exists():
    from pyknow import rule
    assert hasattr(rule, 'OR')


def test_OR_is_Rule_subclass():
    from pyknow.rule import Rule, OR
    assert issubclass(OR, Rule)


@given(args=st.lists(st.booleans()))
def test_OR_logic_args(args):
    from pyknow.rule import OR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]

    assert OR(*_args)({}) == (bool(any(args)), None)


@given(patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_OR_logic_patterns(patterns):
    from pyknow.rule import OR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert OR(**kwargs)(patterns) == (bool(any(patterns.values())), None)


@given(args=st.lists(st.booleans()),
       patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_OR_logic_args_and_patterns(args, patterns):
    from pyknow.rule import OR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert OR(*_args, **kwargs)(patterns) == (bool((any(args) or
                                                    any(patterns.values()))),
                                               None)


@given(args=st.lists(st.booleans()))
def test_OR_nesting(LRule, args):
    from pyknow.rule import OR
    _args = [LRule(x) for x in args]

    assert OR(*_args)({}) == (any(args), None)


#
# XOR
#
def test_XOR_exists():
    from pyknow import rule
    assert hasattr(rule, 'XOR')


def test_XOR_is_Rule_subclass():
    from pyknow.rule import Rule, XOR
    assert issubclass(XOR, Rule)


@given(args=st.lists(st.booleans()))
def test_XOR_logic_args(args):
    from operator import xor
    from functools import reduce
    from pyknow.rule import XOR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]

    assert XOR(*_args)({}) == (bool(reduce(xor, args, False)), None)


@given(patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_XOR_logic_patterns(patterns):
    from operator import xor
    from functools import reduce
    from pyknow.rule import XOR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert XOR(**kwargs)(patterns) == (bool(reduce(xor,
                                                   patterns.values(),
                                                   False)),
                                       None)


@given(args=st.lists(st.booleans()),
       patterns=st.dictionaries(keys=st.text(), values=st.booleans()))
def test_XOR_logic_args_and_patterns(args, patterns):
    from operator import xor
    from functools import reduce
    from pyknow.rule import XOR

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(x) for x in args]
    kwargs = {k: ret(x) for k, x in patterns.items()}

    assert XOR(*_args, **kwargs)(patterns) == (bool(reduce(xor, args, False) ^
                                                    reduce(xor,
                                                           patterns.values(),
                                                           False)),
                                               None)


@given(args=st.lists(st.booleans()))
def test_XOR_nesting(LRule, args):
    from operator import xor
    from functools import reduce
    from pyknow.rule import XOR
    _args = [LRule(x) for x in args]

    assert XOR(*_args)({}) == (reduce(xor, args, False), None)


#
# NOT
#
def test_NOT_exists():
    from pyknow import rule
    assert hasattr(rule, 'NOT')


def test_NOT_is_Rule_subclass():
    from pyknow.rule import Rule, NOT
    assert issubclass(NOT, Rule)


def test_NOT_multiple_args():
    from pyknow.rule import NOT

    with pytest.raises(ValueError):
        NOT((lambda f: True),
            (lambda f: True))({})


def test_NOT_multiple_kwargs():
    from pyknow.rule import NOT

    with pytest.raises(ValueError):
        NOT(something=True,
            other=True)({})


def test_NOT_more_than_one_args_and_or_kwargs():
    from pyknow.rule import NOT

    with pytest.raises(ValueError):
        NOT((lambda f: True),
            other=True)({})


@given(value=st.booleans())
def test_NOT_logic_args(value):
    from operator import xor
    from functools import reduce
    from pyknow.rule import NOT

    def ret(elem):
        def check(_):
            return elem
        return check
        
    _args = [ret(value)]

    assert NOT(*_args)({}) == (not value, None)


@given(value=st.booleans())
def test_NOT_logic_args(value):
    from operator import xor
    from functools import reduce
    from pyknow.rule import NOT

    def ret(elem):
        def check(_):
            return elem
        return check
        
    kwargs = {'something': ret(value)}

    assert NOT(**kwargs)(kwargs) == (not value, None)


def test_NOT_logic_None():
    from pyknow.rule import NOT
        
    assert NOT()() == (not None, None)


@given(value=st.booleans())
def test_NOT_nesting(LRule, value):
    from pyknow.rule import NOT
    _args = [LRule(value)]

    assert NOT(*_args)({}) == (not value, None)
