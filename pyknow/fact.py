"""
Definitions of clips' ``Pattern Conditional Element``.

See :ref:conditional_elements

"""
from collections import OrderedDict
from functools import lru_cache
from itertools import chain
import operator as op

from pyknow.rule import PatternConditionalElement, LiteralPCE
from pyknow.rule import AND, OR, NOT, ComposableCE, Bindable


class Fact(ComposableCE, Bindable, dict):
    """
    Base Fact class

    """
    def __init__(self, *args, **kwargs):
        self.update(dict(chain(enumerate(args), kwargs.items())))

    def update(self, mapping):
        for k, v in mapping.items():
            self[k] = v

    @staticmethod
    def arg_to_ce(arg):
        if not isinstance(arg, PatternConditionalElement):
            return LiteralPCE(arg)
        else:
            return arg

    def __setitem__(self, key, value):
        return super().__setitem__(key, self.arg_to_ce(value))

    def copy(self):
        args = [v for k, v in self.items() if isinstance(k, int)]
        kwargs = {k: v for k, v in self.items() if not isinstance(k, int)}
        return self.__class__(*args, **kwargs)

    @property
    def id(self):
        return self.get('id', None)

    @id.setter
    def id(self, value):
        super().__setitem__('id', LiteralPCE(value))

    @classmethod
    def from_iter(cls, pairs):
        obj = cls()
        obj.update(dict(pairs))
        return obj

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                (repr(v) if isinstance(k, int) else "{}={!r}".format(k, v)
                 for k, v in self.items())))

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(frozenset(self.items()))
            return self._hash

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and super().__eq__(other))


class InitialFact(Fact):
    """
    InitialFact
    """

    # pylint: disable=too-few-public-methods
    pass
