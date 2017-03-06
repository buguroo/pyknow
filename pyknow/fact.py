"""

Definitions of clips' ``Pattern Conditional Element``.

See :ref:conditional_elements

"""
# pylint: disable=invalid-name, unnecessary-lambda
# pylint: disable=no-self-use

from collections import namedtuple
from attrdict import AttrDict


FactType = namedtuple("FactType", "value")


class T(FactType):
    """
    Test (``T`` FactType).

    Evaluates against a callable.

    That is:

    T(lambda x: "foo") == L("foo")
    T(lambda x: x.startswith("asdf") == L("asdffoo")
    """
    pass


class V(FactType):
    """
    Captured values ``FactType``
    Grabs a context to be evaluated later
    """
    pass


class W(FactType):
    """
    Wildcard ``FactType``

    If its value is True, returns True whenever the key is
    found in the other fact.

    If value is False, returns false whenever the key is found
    in the other fact.
    """

    pass


class Fact(AttrDict):
    """
    Base Fact class
    """

    # pylint: disable=too-few-public-methods

    def __hash__(self):
        return hash(tuple(set(self.items())))


class InitialFact(Fact):
    """
    InitialFact
    """

    # pylint: disable=too-few-public-methods
    pass
