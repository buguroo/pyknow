from enum import Enum

import pytest


def test_token_is_namedtuple():
    from pyknow.matchers.rete.token import Token

    assert issubclass(Token, tuple)
    assert 'tag' in Token._fields
    assert 'data' in Token._fields
    assert 'context' in Token._fields


def test_token_tagtype():
    from pyknow.matchers.rete.token import Token

    assert issubclass(Token.TagType, Enum)
    assert hasattr(Token.TagType, 'VALID')
    assert hasattr(Token.TagType, 'INVALID')


def test_token_initialization_types():
    """
    Token.tag must be a Tag
    Token.data can be:
        - A Fact
        - An interable of Facts

    """
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    with pytest.raises(TypeError):
        Token(None, Fact())

    with pytest.raises(TypeError):
        Token(Token.TagType.VALID, None)

    with pytest.raises(TypeError):
        Token(Token.TagType.VALID, [Fact(), None])

    with pytest.raises(TypeError):
        Token(Token.TagType.VALID, [Fact()], [])

    # THIS MUST NOT RAISE
    Token(Token.TagType.VALID, Fact(), {})
    Token(Token.TagType.VALID, [Fact(), Fact()], {})


def test_token_initialization_conversions():
    """
    Token.data is modified in this way:
        - If is a Fact: Converted to a Set containing this Fact.
        - An interable of Facts: Converter to a set of Facts.

    """
    from pyknow.matchers.rete.token import Token
    from pyknow.fact import Fact

    t1 = Token(Token.TagType.VALID, Fact())
    assert t1.data == {Fact()}

    t2 = Token(Token.TagType.VALID, [Fact(a=1), Fact(b=2)])
    assert t2.data == {Fact(a=1), Fact(b=2)}


def test_token_shortcut_valid():
    from pyknow.matchers.rete.token import Token

    assert Token.valid([]) == Token(Token.TagType.VALID, [])


def test_token_shortcut_invalid():
    from pyknow.matchers.rete.token import Token

    assert Token.invalid([]) == Token(Token.TagType.INVALID, [])


def test_token_copy_mutable():
    from pyknow.matchers.rete.token import Token

    a = Token.valid([])
    b = a.copy()

    assert a == b and a is not b
    assert a.data == b.data and a.data is not b.data
    assert a.context == b.context and a.context is not b.context
