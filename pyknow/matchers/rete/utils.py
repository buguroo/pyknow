from functools import singledispatch
from .dnf import dnf
from .check import FeatureCheck, TypeCheck, FactCapture
from .nodes import ConflictSetNode, NotNode, OrdinaryMatchNode
from pyknow import Rule, InitialFact, NOT, OR, Fact, AND
from pyknow.rule import ConditionalElement


@singledispatch
def prepare_rule(exp):
    """
    Given a rule, build a new one suitable for RETE network generation.

    Meaning:

        #. Rule is in disjuntive normal form (DNF).

        #. If the `rule` is empty is filled with an `InitialFact`.

        #. If the `rule` starts with a `NOT`, an `InitialFact` is prepended.

        #. If any AND starts with a `NOT`, an `InitialFact` is prepended.

        #. If the `rule` is an OR condition, each NOT inside will be
        converted to AND(InitialFact(), NOT(...))

    """
    return exp


@prepare_rule.register(Rule)
def _(exp):
    dnf_rule = dnf(exp)
    prep_rule = Rule(*[prepare_rule(e) for e in dnf_rule])(dnf_rule._wrapped)
    if not prep_rule:
        return Rule(InitialFact())(prep_rule._wrapped)
    elif isinstance(prep_rule[0], NOT):
        return Rule(InitialFact(), *prep_rule)(prep_rule._wrapped)
    else:
        return dnf(prep_rule)


@prepare_rule.register(OR)
def _(exp):
    or_exp = []
    for e in exp:
        if isinstance(e, NOT):
            or_exp.append(AND(InitialFact(), e))
        elif isinstance(e, AND):
            or_exp.append(prepare_rule(e))
        else:
            or_exp.append(e)
    return OR(*or_exp)


@prepare_rule.register(AND)
def _(exp):
    if isinstance(exp[0], NOT):
        return AND(InitialFact(), *exp)
    else:
        return exp


def extract_facts(rule):
    """Given a rule, return a set containing all rule LHS facts."""
    def _extract_facts(ce):
        if isinstance(ce, Fact):
            yield ce
        else:
            for e in ce:
                yield from _extract_facts(e)

    return set(_extract_facts(rule))


def generate_checks(fact):
    """Given a fact, generate a list of Check objects for checking it."""

    yield TypeCheck(type(fact))

    for key, value in fact.items():
        if key == 'id':
            yield FactCapture(value[0])
        else:
            yield FeatureCheck(key, value)


def wire_rule(rule, alpha_terminals, lhs=None):
    if lhs is None:
        lhs = rule

    @singledispatch
    def _wire_rule(elem):
        raise TypeError("Unknown type %s" % type(elem))

    @_wire_rule.register(Rule)
    @_wire_rule.register(AND)
    def _(elem):

        def same_context(l, r):
            for key, value in l.items():
                if isinstance(key, tuple):
                    raise RuntimeError(
                        'Negated value "%s" present before capture.' % key[1])
                else:
                    if key in r and value != r[key]:
                        return False
                    if (False, key) in r and value == r[(False, key)]:
                        return False
            return True

        if len(elem) == 1 and isinstance(elem[0], Fact):
            return alpha_terminals[elem[0]]
        elif len(elem) > 1:
            current_node = None
            for f, s in zip(elem, elem[1:]):
                if isinstance(s, NOT):
                    node_cls = NotNode
                else:
                    node_cls = OrdinaryMatchNode

                if current_node is None:
                    current_node = node_cls(same_context)
                    left_branch = _wire_rule(f)
                    right_branch = _wire_rule(s)
                else:
                    left_branch = current_node
                    right_branch = _wire_rule(s)
                    current_node = node_cls(same_context)

                left_branch.add_child(current_node,
                                      current_node.activate_left)
                right_branch.add_child(current_node,
                                       current_node.activate_right)
            return current_node
        else:
            raise RuntimeError("Invalid rule! %r" % elem)

    @_wire_rule.register(Fact)
    def _(elem):
        return alpha_terminals[elem]

    @_wire_rule.register(NOT)
    def _(elem):
        return alpha_terminals[elem[0]]

    # Add a new child to the last node to trigger the rule
    conflict_set_node = ConflictSetNode(rule)
    last_node = _wire_rule(lhs)
    last_node.add_child(conflict_set_node, conflict_set_node.activate)
