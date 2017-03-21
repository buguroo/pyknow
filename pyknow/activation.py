"""
Activations represent rules that matches against a specific factlist.

"""
from pyknow.rule import Rule


class Activation:
    """
    Activation object
    """
    def __init__(self, rule, facts, context=None):
        if not isinstance(rule, Rule):
            raise TypeError("Rule must be a Rule object")

        if not isinstance(facts, tuple):
            raise TypeError("Facts must be tuple")

        self.rule = rule
        self.facts = facts
        if context is None:
            self.context = dict()
        else:
            self.context = context

    def __repr__(self):
        return "Activation(rule={}, facts={}, context={})".format(
            self.rule, self.facts, self.context)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.rule == other.rule \
            and self.facts == other.facts \
            and self.context == other.context

    def __hash__(self):
        return hash((self.rule,
                     frozenset(self.facts),
                     frozenset(self.context.items())))
