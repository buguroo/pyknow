"""

Definitions of clips' ``Pattern Conditional Element``.

See :ref:conditional_elements

"""
# pylint: disable=no-member, too-few-public-methods
# pylint: disable=unused-import
from collections import OrderedDict
from pyknow.facttypes import ValueSet
from pyknow.facttypes import L, V, N, C, T, W, FACT_TYPES  # NOQA


class Context(dict):
    """
    Context is a just dictionary for now
    """
    def __hash__(self):
        return hash(tuple(self.items()))


class Fact:
    """
    Base Fact class
    """
    def __init__(self, **value):
        self.rule = False
        self.value = value
        self.keyset = set(value.keys())
        self.valuesets = OrderedDict()
        for fact_type in FACT_TYPES:
            self.valuesets[fact_type] = ValueSet(self, fact_type)
        self.populated = False

    @property
    def context(self):
        """ Rule context """
        if self.rule:
            return self.rule.context
        else:
            return {}

    def __contains__(self, other):
        """
        Does this Fact contain ``other``?.

        To check it, we group its values by its FactType
        (populating with them ValueSet objects), and check
        if none of them declare a negative condition.

        ValueSet objects are to be tested using .matches method,
        wich will be a different implementation for each kind of
        facttype, as there will be a different ValueSet subclass
        for each facttype.

        .. warning:: This is a match-by-default method.
        """

        if self.__class__ != other.__class__:
            return False
        elif not self.value:
            # TODO: Check if this is because of the initialfact.
            # TODO: Maybe this is the reason I don't quite get the NOT.
            return True

        # The first time we compare a fact, populate its valuesets.
        if not other.populated:
            for key, value in other.value.items():
                value.key = key
                value_ = (key, value)
                other.valuesets[value.__class__.__name__].value.add(value_)
            other.populated = True

        # and ours
        if not self.populated:
            for key, value in self.value.items():
                value.key = key
                self.valuesets[value.__class__.__name__].value.add(
                    (key, value))
            self.populated = True

        for valueset in self.valuesets.values():
            if not valueset.matches(other):
                return False
        return True

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(tuple(self.value.items()))

    def __repr__(self):
        value = ', '.join("{}={}".format(a, b) for a, b in self.value.items())
        return "Fact({})".format(value)


class InitialFact(Fact):
    """
        InitialFact
    """
    pass
