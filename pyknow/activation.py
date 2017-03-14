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
        self.context = context

    def __repr__(self):
        return "Activation(rule={}, facts={}, context={})".format(
            self.rule, self.facts, self.context)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.rule == other.rule and self.facts == other.facts
        else:
            return False

    def __hash__(self):
        return hash(
            (hash(self.rule), self.facts,
             tuple(self.context.items() if self.context else tuple())))
