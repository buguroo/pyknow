from collections import namedtuple
from collections.abc import Mapping
from enum import Enum

from pyknow.fact import Fact


class TokenInfo(namedtuple('_TokenInfo', ['data', 'context'])):
    def to_valid_token(self):
        return Token.valid(self.data, self.context)

    def to_invalid_token(self):
        return Token.invalid(self.data, self.context)


class Token(namedtuple('_Token', ['tag', 'data', 'context'])):
    class TagType(Enum):
        VALID = True
        INVALID = False

    def __new__(cls, tag, data, context=None):
        if context is None:
            context = {}

        try:
            assert isinstance(tag, cls.TagType), \
                "tag must be of `Token.TagType` type"
            assert (isinstance(data, Fact) or
                    all(isinstance(f, Fact) for f in data)), \
                "data must be either Fact or iterable of Facts"
            assert isinstance(context, Mapping)
        except AssertionError as exc:
            raise TypeError(exc) from exc

        data = {data} if isinstance(data, Fact) else set(data)
        self = super(Token, cls).__new__(cls, tag, data, context)
        return self

    def to_info(self):
        return TokenInfo(self.data, self.context)

    @classmethod
    def valid(cls, data, context=None):
        return cls(cls.TagType.VALID, data, context)

    @classmethod
    def invalid(cls, data, context=None):
        return cls(cls.TagType.INVALID, data, context)

    def is_valid(self):
        return self.tag == self.TagType.VALID

    def copy(self):
        return self.__class__(self.tag, self.data.copy(), self.context.copy())
