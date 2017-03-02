from collections import namedtuple
from enum import Enum

from pyknow.fact import Fact


class Token(namedtuple('_Token', ['tag', 'data'])):
    class TagType(Enum):
        VALID = True
        INVALID = False

    def __new__(cls, tag, data):
        try:
            assert isinstance(tag, cls.TagType), \
                "tag must be of `Token.TagType` type"
            assert (isinstance(data, Fact) or
                    all(isinstance(f, Fact) for f in data)), \
                "data must be either Fact or iterable of Facts"
        except AssertionError as exc:
            raise TypeError(exc) from exc

        data = {data} if isinstance(data, Fact) else set(data)
        self = super(Token, cls).__new__(cls, tag, data)
        return self
