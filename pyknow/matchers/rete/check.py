from collections import namedtuple
from collections.abc import Mapping
import dis
import inspect

from pyknow.rule import PatternConditionalElement
from pyknow.rule import LiteralPCE, PredicatePCE, WildcardPCE
from pyknow.rule import ANDPCE, ORPCE, NOTPCE
from .abstract import Check
from pyknow.watchers import MATCH


class TypeCheck(Check, namedtuple('_TypeCheck', ['fact_type'])):

    _instances = dict()

    def __new__(cls, fact_type):
        if fact_type not in cls._instances:
            cls._instances[fact_type] = super().__new__(cls, fact_type)
        return cls._instances[fact_type]

    def __call__(self, fact):
        res = type(fact) == self.fact_type

        log = MATCH.info if res else MATCH.debug
        log("type(%s) == %s = %r",
            fact, self.fact_type.__name__, res)

        return res

    def __str__(self):
        return "type() == %s" % self.fact_type.__name__


class FactCapture(Check, namedtuple('_FactCapture', ['bind'])):

    _instances = dict()

    def __new__(cls, bind):
        if bind not in cls._instances:
            cls._instances[bind] = super().__new__(cls, bind)
        return cls._instances[bind]

    @property
    def __bind__(self):
        return self.bind

    def __call__(self, fact):
        MATCH.info("%r <= %s", self.__bind__, fact)
        return {self.__bind__: fact}

    def __str__(self):
        return "%s <= <Fact>" % (self.__bind__)


class FeatureCheck(Check,
                   namedtuple('_FeatureCheck',
                              ['what', 'how', 'check', 'expected'])):

    _instances = dict()

    def __new__(cls, what, how):
        if not isinstance(how, PatternConditionalElement):
            how = LiteralPCE(how)

        key_a = type(how)

        if key_a is LiteralPCE:
            key_b = (how.value, how.__bind__)
        elif key_a is PredicatePCE:
            key_b = (tuple(dis.get_instructions(how.match)), how.__bind__)
        elif key_a is WildcardPCE:
            key_b = how.__bind__
        elif key_a is NOTPCE:
            key_b = FeatureCheck(what, how[0])
        elif key_a in (ANDPCE, ORPCE):
            key_b = tuple([FeatureCheck(what, h) for h in how])
        else:
            raise TypeError("Unknown PCE type.")

        key = (what, key_a, key_b)

        if key not in cls._instances:
            if key_a is LiteralPCE:
                def equal_literal(actual, expected):
                    if expected.value == actual:
                        if expected.__bind__ is None:
                            return True
                        else:
                            return {expected.__bind__: actual}
                    else:
                        return False

                expected = how
                check = equal_literal
            elif key_a is PredicatePCE:
                def match_predicate(actual, expected):
                    if expected.match(actual):
                        if expected.__bind__ is None:
                            return True
                        else:
                            return {expected.__bind__: actual}
                    else:
                        return False

                expected = how
                check = match_predicate
            elif key_a is WildcardPCE:
                def wildcard_match(actual, expected):
                    if expected.__bind__ is None:
                        return True
                    else:
                        return {expected.__bind__: actual}

                expected = how
                check = wildcard_match
            elif key_a is NOTPCE:
                def not_equal(actual, expected):
                    subresult = expected(actual, is_fact=False)
                    if isinstance(subresult, Mapping):
                        newresult = {(False, k): v
                                     for k, v in subresult.items()}
                        return newresult
                    else:
                        return not subresult

                expected = key_b
                check = not_equal
            elif key_a is ANDPCE:
                def and_match(actual, expected):
                    value = dict()
                    for subcheck in expected:
                        subres = subcheck(actual, is_fact=False)
                        if subres is False:
                            break
                        elif subres is True:
                            pass
                        elif isinstance(subres, Mapping):
                            value.update(subres)
                        else:
                            raise TypeError('Bad check value.')
                    else:
                        if not value:
                            return True
                        else:
                            return value
                    return False

                expected = key_b
                check = and_match
            elif key_a is ORPCE:
                def or_match(actual, expected):
                    for subcheck in expected:
                        subres = subcheck(actual, is_fact=False)
                        if subres:
                            return subres
                    else:
                        return False

                expected = key_b
                check = or_match
            else:  # noqa
                pass

            cls._instances[key] = super(Check, cls).__new__(
                cls,
                what,
                how,
                check,
                expected)

        return cls._instances[key]

    def __call__(self, data, is_fact=True):
        if is_fact:
            try:
                record = data[self.what]
            except KeyError:
                return False
        else:
            record = data

        res = self.check(record, self.expected)

        log = MATCH.info if res else MATCH.debug
        log("what=%r, how=%r, fact=%s = %r", self.what, self.how, data, res)

        return res

    def __str__(self):
        return "%s (%s) %s" % (self.what, self.check.__name__, self.expected)


class SameContextCheck(Check):
    def __call__(self, l, r):
        for key, value in l.items():
            if key[0] is False:
                raise RuntimeError(
                    'Negated value "%s" present before capture.' % key[1])
            else:
                if key in r and value != r[key]:
                    return False
                if (False, key) in r and value == r[(False, key)]:
                    return False
        else:
            return True


class WhereCheck(Check, namedtuple('_WhereCheck', ['test'])):

    _instances = dict()

    def __new__(cls, test):
        if test not in cls._instances:
            obj = super().__new__(cls, test)
            obj.parameters = inspect.signature(test).parameters.keys()
            cls._instances[test] = obj

        return cls._instances[test]

    def __call__(self, context):
        parameters = {k: context[k] for k in self.parameters}
        res = self.test(**parameters)

        log = MATCH.info if res else MATCH.debug
        log("TEST %r(%r) == %r", self.test, parameters, res)

        return res
