from functools import wraps, partial, reduce
from enum import Enum
from abc import ABCMeta, abstractmethod
import operator


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
        def _get_value(a):
            if isinstance(a, Rule):
                return a(facts)[0]
            else:
                return a(facts)
        return (_get_value(a) for a in self.args)


class AND(Rule):
    def __eval__(self, facts=None):
        return (all(self._check_args(facts)) and
                all(self._check_pattern(name, facts)
                    for name in self.patterns))


class OR(Rule):
    def __eval__(self, facts=None):
        return (any(self._check_args(facts)) or
                any(self._check_pattern(name, facts)
                    for name in self.patterns))


class XOR(Rule):
    def __eval__(self, facts=None):
        def _xor(items):
            return reduce(operator.xor, items, False)

        return (_xor(self._check_args(facts)) ^ 
                _xor(self._check_pattern(name, facts)
                     for name in self.patterns))


class NOT(Rule):
    def __eval__(self, facts=None):
        if len(self.args) + len(self.patterns) > 1:
            raise ValueError("Can't use multiple values with unary operator.")

        if self.args:
            return not list(self._check_args(facts))[0]
        elif self.patterns:
            return not [self._check_pattern(name, facts)
                        for name in self.patterns][0]
        else:
            return True
