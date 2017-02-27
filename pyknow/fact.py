"""

Definitions of clips' ``Pattern Conditional Element``.

See :ref:conditional_elements

"""
# pylint: disable=no-member, too-few-public-methods
# pylint: disable=unused-import

from collections import OrderedDict
from itertools import product

from pyknow.activation import Activation
from pyknow.facttypes import FactType, L, V, N, C, T, W, FACT_TYPES  # NOQA
from pyknow.facttypes import ValueSet
from pyknow.match import Capturation, Context
from pyknow.watchers import FACT_WATCHER


class Fact:
    """
    Base Fact class
    """
    def __init__(self, **value):
        self.rule = False
        self.value = value
        self.keyset = set(value.keys())
        self.valuesets = OrderedDict()
        for value in value.values():
            if not isinstance(value, FactType):
                raise ValueError("Fact values must descend from FactType")
        for fact_type in FACT_TYPES:
            self.valuesets[fact_type] = ValueSet(self, fact_type)
        self.populated = False

    def get_activations(self, factlist, capturations):
        """
        Extract activations from a given fact.
        Will be aggregated later by a ``Rule``
        """
        FACT_WATCHER.debug("Getting activations")

        if not capturations:
            FACT_WATCHER.debug("No capturations found")
            for idx, fact in factlist.facts.items():
                if self.matches(fact, Context()):
                    act = Activation(rule=None, facts=(idx,))
                    FACT_WATCHER.debug("Yielding uncontexted act: %s", act)
                    yield act
        else:
            for (idx, fact), caps in product(factlist.facts.items(),
                                             capturations.items()):
                cap_facts, ctx = caps
                if self.matches(fact, ctx):
                    facts = tuple(set([int(a) for a in cap_facts] + [idx]))
                    act = Activation(rule=None, facts=facts, context=ctx)
                    FACT_WATCHER.debug("Yielding contexted act: %s", act)
                    yield act
        FACT_WATCHER.debug("Got all activations")

    def get_capturations(self, factlist):
        """
        Returns ``Capturation`` objects, relating facts with its matching
        context
        """

        FACT_WATCHER.debug("Getting capturations")

        capture_valueset = ValueSet(self, 'C')

        for key, value in self.value.items():
            if value.__class__.__name__ == "C":
                value.key = key
                capture_valueset.value.add((key, value))

        for idx, fact in factlist.facts.items():
            captured_context = capture_valueset.matches(fact)
            if captured_context:
                yield Capturation(**{str(idx): captured_context})

        FACT_WATCHER.debug("All capturations returned")

    def matches(self, other, context):
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
            # This is so empty Fact() conditions will match.
            return True

        # The first time we compare a fact, populate its valuesets.
        if not other.populated:
            for key, value in other.value.items():
                if value.__class__.__name__ == "C":
                    continue
                value.key = key
                value_ = (key, value)
                other.valuesets[value.__class__.__name__].value.add(value_)
            other.populated = True

        # and ours
        if not self.populated:
            for key, value in self.value.items():
                if value.__class__.__name__ == "C":
                    continue
                value.key = key
                self.valuesets[value.__class__.__name__].value.add(
                    (key, value))
            self.populated = True

        for valueset in self.valuesets.values():
            if not valueset.matches(other, context):
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
