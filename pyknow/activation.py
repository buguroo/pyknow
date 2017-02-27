"""
Activations represent rules that matches against a specific factlist.

"""

# pylint: disable=too-few-public-methods


class Activation:
    """
    Activation object
    """
    def __init__(self, rule, facts):
        from pyknow.rule import Rule
        if rule:
            if not isinstance(rule, Rule):
                raise ValueError("Rule must be a Rule object")
        if not isinstance(facts, tuple):
            raise ValueError("Facts must be tuple")
        self.rule = rule
        self.facts = facts

    def __add__(self, other):
        facts = set(self.facts + other.facts)
        return Activation(rule=self.rule, facts=tuple(facts))

    def __repr__(self):
        return "Activation(rule={}, facts={})".format(self.rule, self.facts)

    def __eq__(self, other):
        return self.rule == other.rule and self.facts == other.facts

    def __hash__(self):
        return hash((self.rule, self.facts))
