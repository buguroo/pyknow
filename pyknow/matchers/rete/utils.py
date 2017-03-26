from functools import singledispatch, lru_cache
import warnings

from .dnf import dnf
from .check import FeatureCheck, TypeCheck, FactCapture, SameContextCheck, WhereCheck
from .nodes import ConflictSetNode, NotNode, OrdinaryMatchNode
from .nodes import FeatureTesterNode, WhereNode
from pyknow import Rule, InitialFact, NOT, OR, Fact, AND
from pyknow.rule import ConditionalElement
from pyknow.watchers import MATCH


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
    prep_rule = dnf_rule.new_conditions(
        *[prepare_rule(e) for e in dnf_rule])
    if not prep_rule:
        return prep_rule.new_conditions(InitialFact())
    elif isinstance(prep_rule[0], NOT):
        return prep_rule.new_conditions(InitialFact(), *prep_rule)
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
        if (isinstance(key, str)
                and key.startswith('__')
                and key.endswith('__')):
            # Special fact feature
            if key == '__bind__':
                yield FactCapture(value)
            else:
                warnings.warn(
                    "Unknown special symbol '%s' inside pattern" % key)
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
                    current_node = node_cls(SameContextCheck())
                    left_branch = _wire_rule(f)
                    right_branch = _wire_rule(s)
                else:
                    left_branch = current_node
                    right_branch = _wire_rule(s)
                    current_node = node_cls(SameContextCheck())

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

    # Build beta network
    last_node = _wire_rule(lhs)

    # Add all (where) tests to the end of the beta network, before the CSN
    for test in rule.where:
        test_node = WhereNode(WhereCheck(test))
        last_node.add_child(test_node, test_node.activate)
        last_node = test_node

    # Add a new child to the last node to trigger the rule
    conflict_set_node = ConflictSetNode(rule)
    last_node.add_child(conflict_set_node, conflict_set_node.activate)
