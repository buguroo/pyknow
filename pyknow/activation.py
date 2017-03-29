"""
Activations represent rules that matches against a specific factlist.

"""
from functools import lru_cache
from collections.abc import Iterable

from pyknow.rule import Rule
from pyknow.fact import Fact


class Activation:
    """
    Activation object
    """
    def __init__(self, rule, facts, context=None):
        self.rule = rule
        self.facts = set(facts)
        if context is None:
            self.context = dict()
        else:
            self.context = context

    def __repr__(self):  # pragma: no cover
        return "Activation(rule={}, facts={}, context={})".format(
            self.rule, self.facts, self.context)

    def __eq__(self, other):
        try:
            return (self.context == other.context
                    and self.facts == other.facts
                    and self.rule == other.rule)
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.rule,
                     frozenset(self.facts),
                     frozenset(self.context.items())))
