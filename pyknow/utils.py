from functools import singledispatch, reduce
import collections.abc

from frozendict import frozendict

from .fieldconstraint import P
from .conditionalelement import ConditionalElement


@singledispatch
def freeze(obj):
    if isinstance(obj, collections.abc.Hashable):
        return obj
    else:
        raise TypeError(
            ("type(%r) => %s is not hashable, "
             "see `pyknow.utils.freeze` docs to register your "
             "own freeze method") % (obj, type(obj)))


@freeze.register(collections.abc.MutableMapping)
def freeze_mapping(obj):
    return frozendict((k, freeze(v)) for k, v in obj.items())


@freeze.register(collections.abc.MutableSequence)
def freeze_list(obj):
    return tuple(freeze(v) for v in obj)


@freeze.register(collections.abc.MutableSet)
def freeze_set(obj):
    return frozenset(freeze(v) for v in obj)


def anyof(*what):
    return P(lambda y: y in what)


"""
N = {}
F = defaultdict(W)
for k, v in N.items():
    if is_nested(k):
        base = getbase(k)
        F[base] &= flattern(k , v)

"""


def get_base(s):
    return s.split("__")[0]


def is_nested(s):
    return "__" in s.strip('_')


def flattern(key, fn):
    base, *path = key.split("__")
    if not isinstance(fn, ConditionalElement):
        _fn = (lambda x: x == fn)
    else:
        _fn = fn

    def _extract_and_apply(current):
        for p in path:
            if p.isnumeric():
                p = int(p)
            try:
                current = current[p]
            except (KeyError, IndexError, TypeError):
                return False
        return _fn(current)

    return P(_extract_and_apply)
