from collections import namedtuple
from collections.abc import Mapping
from enum import Enum

from pyknow.fact import Fact


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

    @classmethod
    def valid(cls, data):
        return cls(cls.TagType.VALID, data)

    @classmethod
    def invalid(cls, data):
        return cls(cls.TagType.INVALID, data)

    def copy(self):
        return self.__class__(self.tag, self.data.copy(), self.context.copy())
