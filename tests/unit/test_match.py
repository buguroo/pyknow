"""
Test match module
"""

import pytest


def test_capturations_add():
    """ Test __add__ method of capturations """
    from pyknow.match import Capturation, Context
    cap1 = Capturation({"1": Context({"1": "foo"}),
                        "2": Context({"1": "bar"})})
    cap2 = Capturation({"1": Context({"2": "foo"}),
                        "3": Context({"1": "foo"})})
    result = cap1 + cap2
    assert result == Capturation({"1": Context({"1": "foo", "2": "foo"}),
                                  "2": Context({"1": "bar"}),
                                  "3": Context({"1": "foo"})})


def test_context_add():
    """ Test __add__ method of context """
    from pyknow.match import Context
    context1 = Context({"foo": 1})
    context2 = Context({"bar": 1})
    context3 = Context({"foo": 1, "bar": 1})
    result = context1 + context2
    assert context3 == result


def test_context_add_setitem():
    """ Check that context are not overwritten """
    from pyknow.match import Context
    context = Context()
    context["foo"] = "bar"
    context["foo"] = "bar"
    with pytest.raises(ValueError):
        context["foo"] = "baz"
