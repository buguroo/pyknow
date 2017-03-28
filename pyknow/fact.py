from itertools import chain

from pyknow.pattern import Bindable
from pyknow.conditionalelement import OperableCE
from pyknow.conditionalelement import ConditionalElement


class Fact(OperableCE, Bindable, dict):
    """Base Fact class"""

    def __init__(self, *args, **kwargs):
        self.update(dict(chain(enumerate(args), kwargs.items())))

    def update(self, mapping):
        for k, v in mapping.items():
            self[k] = v

    def copy(self):
        args = [v for k, v in self.items() if isinstance(k, int)]
        kwargs = {k: v for k, v in self.items() if not isinstance(k, int)}
        return self.__class__(*args, **kwargs)

    def has_field_constraints(self):
        return any(isinstance(v, ConditionalElement) for v in self.values())

    @staticmethod
    def is_special(key):
        return (isinstance(key, str)
                and key.startswith('__')
                and key.endswith('__'))

    @property
    def __bind__(self):
        return self.get('__bind__', None)

    @__bind__.setter
    def __bind__(self, value):
        super().__setitem__('__bind__', value)

    @property
    def __factid__(self):
        return self.get('__factid__', None)

    @__factid__.setter
    def __factid__(self, value):
        super().__setitem__('__factid__', value)

    @classmethod
    def from_iter(cls, pairs):
        obj = cls()
        obj.update(dict(pairs))
        return obj

    def __str__(self):
        if self.__factid__ is None:
            return "<Undeclared Fact> %r" % self
        else:
            return "<f-%d>" % self.__factid__

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                (repr(v) if isinstance(k, int) else "{}={!r}".format(k, v)
                 for k, v in self.items()
                 if not self.is_special(k))))

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
    pass
