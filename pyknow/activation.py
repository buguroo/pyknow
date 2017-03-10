"""
Activations represent rules that matches against a specific factlist.

"""

# pylint: disable=too-few-public-methods

from pyknow.match import Context


class Activation:
    """
    Activation object
    """
    def __init__(self, rule, facts, context=None):
        from pyknow.rule import Rule
        if rule:
            if not isinstance(rule, Rule):
                raise ValueError("Rule must be a Rule object")
        if not isinstance(facts, tuple):
            raise ValueError("Facts must be tuple")
        self.rule = rule
        self.facts = facts
        self.context = context

    def __add__(self, other):
        facts = set(self.facts + other.facts)
        contexts = (self.context, other.context)
        context = sum((a for a in contexts if a), Context())
        return Activation(rule=self.rule, facts=tuple(facts),
                          context=context)

    def __repr__(self):
        return "Activation(rule={}, facts={}, context={})".format(
            self.rule, self.facts, self.context)

    def __eq__(self, other):
        return self.rule == other.rule and self.facts == other.facts

    def __hash__(self):
        return hash(
            (hash(self.rule), self.facts,
             tuple(self.context.items() if self.context else tuple())))
