from functools import singledispatch
import collections.abc

from frozendict import frozendict


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
