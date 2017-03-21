from collections import namedtuple
from collections.abc import Mapping
import dis

from pyknow.rule import PatternConditionalElement
from pyknow.rule import LiteralPCE, PredicatePCE, WildcardPCE
from pyknow.rule import ANDPCE, ORPCE, NOTPCE
from .abstract import Check


class TypeCheck(Check, namedtuple('_TypeCheck', ['fact_type'])):

    _instances = dict()

    def __new__(cls, fact_type):
        if fact_type not in cls._instances:
            cls._instances[fact_type] = super().__new__(cls, fact_type)
        return cls._instances[fact_type]

    def __call__(self, fact):
        return type(fact) == self.fact_type


class FeatureCheck(Check,
                   namedtuple('_FeatureCheck',
                              ['what', 'how', 'check', 'expected'])):

    _instances = dict()

    def __new__(cls, what, how):
        if not isinstance(how, PatternConditionalElement):
            raise TypeError(
                "Check object accepts PatternConditionalElements only.")
        else:
            key_a = type(how)
            if key_a is LiteralPCE:
                key_b = (how[0], how.id)
            elif key_a is PredicatePCE:
                key_b = (tuple(dis.get_instructions(how[0])), how.id)
            elif key_a is WildcardPCE:
                key_b = how.id
            elif key_a is NOTPCE:
                key_b = FeatureCheck(what, how[0])
            elif key_a in (ANDPCE, ORPCE):
                key_b = tuple([FeatureCheck(what, h) for h in how])
            else:
                raise TypeError("Unknown PCE type.")

            key = (what, key_a, key_b)

            if key not in cls._instances:
                if key_a is LiteralPCE:
                    expected = how

                    def check(actual, expected):
                        if expected.value == actual:
                            if expected.id is None:
                                return True
                            else:
                                return {expected.id: actual}
                        else:
                            return False

                elif key_a is PredicatePCE:
                    expected = how

                    def check(actual, expected):
                        if expected.match(actual):
                            if expected.id is None:
                                return True
                            else:
                                return {expected.id: actual}
                        else:
                            return False

                elif key_a is WildcardPCE:
                    expected = how

                    def check(actual, expected):
                        if expected.id is None:
                            return True
                        else:
                            return {expected.id: actual}

                elif key_a is NOTPCE:
                    expected = key_b

                    def check(actual, expected):
                        subresult = expected(actual, is_fact=False)
                        if isinstance(subresult, Mapping):
                            newresult = {(False, k): v
                                         for k, v in subresult.items()}
                            return newresult
                        else:
                            return not subresult

                elif key_a is ANDPCE:
                    expected = key_b

                    def check(actual, expected):
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

                elif key_a is ORPCE:
                    expected = key_b

                    def check(actual, expected):
                        for subcheck in expected:
                            subres = subcheck(actual, is_fact=False)
                            if subres:
                                return subres
                        else:
                            return False

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
                # Value is always inside a LiteralPCE
                record = data[self.what][0]
            except KeyError:
                return False
        else:
            record = data

        return self.check(record, self.expected)
