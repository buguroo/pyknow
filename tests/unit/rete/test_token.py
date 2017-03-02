from enum import Enum

import pytest


@pytest.mark.wip
def test_token_is_namedtuple():
    from pyknow.rete.token import Token

    assert issubclass(Token, tuple)
    assert 'tag' in Token._fields
    assert 'data' in Token._fields


@pytest.mark.wip
def test_token_tagtype():
    from pyknow.rete.token import Token

    assert issubclass(Token.TagType, Enum)
    assert hasattr(Token.TagType, 'VALID')
    assert hasattr(Token.TagType, 'INVALID')


@pytest.mark.wip
def test_token_initialization_types():
    """
    Token.tag must be a Tag
    Token.data can be:
        - A Fact
        - An interable of Facts

    """
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    with pytest.raises(TypeError):
        Token(None, Fact())

    with pytest.raises(TypeError):
        Token(Token.TagType.VALID, None)

    with pytest.raises(TypeError):
        Token(Token.TagType.VALID, [Fact(), None])

    # THIS MUST NOT RAISE
    Token(Token.TagType.VALID, Fact())
    Token(Token.TagType.VALID, [Fact(), Fact()])


@pytest.mark.wip
def test_token_initialization_conversions():
    """
    Token.data is modified in this way:
        - If is a Fact: Converted to a Set containing this Fact.
        - An interable of Facts: Converter to a set of Facts.

    """
    from pyknow.rete.token import Token
    from pyknow.fact import Fact

    t1 = Token(Token.TagType.VALID, Fact())
    assert t1.data == {Fact()}

    t2 = Token(Token.TagType.VALID, [Fact(a=1), Fact(b=2)])
    assert t2.data == {Fact(a=1), Fact(b=2)}
