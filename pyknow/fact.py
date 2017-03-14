"""
Definitions of clips' ``Pattern Conditional Element``.

See :ref:conditional_elements

"""
from collections import OrderedDict
import operator as op

from pyknow.rule import PatternConditionalElement, LiteralPCE


class Fact(OrderedDict):
    """
    Base Fact class

    """
    @staticmethod
    def arg_to_ce(arg):
        if not isinstance(arg, PatternConditionalElement):
            return LiteralPCE(arg)
        else:
            return arg

    def __init__(self, *args, **kwargs):
        super(Fact, self).__init__()

        for idx, arg in enumerate(args):
            self[idx] = self.arg_to_ce(arg)

        for key, value in sorted(kwargs.items(), key=op.itemgetter(0)):
            if key.isidentifier():
                self[key] = self.arg_to_ce(value)
            else:
                raise ValueError("{!r} is not a valid identifier.".format(key))

    @classmethod
    def from_iter(cls, pairs):
        obj = cls()

        for k, v in pairs:
            obj[k] = v

        return obj

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                (repr(v) if isinstance(k, int) else "{}={!r}".format(k, v)
                 for k, v in self.items())))

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __eq__(self, other):
        if type(self) == type(other):
            return hash(self) == hash(other)
        else:
            return False


class InitialFact(Fact):
    """
    InitialFact
    """

    # pylint: disable=too-few-public-methods
    pass
