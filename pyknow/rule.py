from functools import wraps, partial
from enum import Enum
from abc import ABCMeta, abstractmethod


class FactState(Enum):
    DEFINED = 'DEFINED'
    NOT_DEFINED = 'NOT_DEFINED'


class Rule(metaclass=ABCMeta):
    def __init__(self, **conds):
        self.conds = conds
        
    @abstractmethod
    def __eval__(self, facts=None):
        pass

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(facts=None, *args, **kwargs):
            p = partial(fn, *args, **kwargs)
            return (self.__eval__(facts), p)
        return wrapper

    def _check(self, name, facts):
        _cmp = self.conds[name]
        if _cmp is FactState.DEFINED:
            return name in facts
        elif _cmp is FactState.NOT_DEFINED:
            return name not in facts
        else:
            if not name in facts:
                return False
            elif callable(_cmp):
                return _cmp(facts[name])
            else:
                return facts[name] == _cmp
