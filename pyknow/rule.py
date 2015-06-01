from functools import wraps, partial
from enum import Enum
from abc import ABCMeta, abstractmethod


class FactState(Enum):
    DEFINED = 'DEFINED'
    NOT_DEFINED = 'NOT_DEFINED'


class Rule(metaclass=ABCMeta):
    def __init__(self, *args, **patterns):
        self.args = args
        self.patterns = patterns
        
    @abstractmethod
    def __eval__(self, facts=None):
        pass

    def __call__(self, fn_or_facts=None):
        if callable(fn_or_facts):
            fn = fn_or_facts
            @wraps(fn)
            def wrapper(facts=None, *args, **kwargs):
                p = partial(fn, *args, **kwargs)
                return (self.__eval__(facts), p)
            return wrapper
        else:
            facts = fn_or_facts
            return (self.__eval__(facts), None)

    def _check_pattern(self, name, facts):
        _cmp = self.patterns[name]
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

    def _check_args(self, facts):
        return (a(facts) for a in self.args)
