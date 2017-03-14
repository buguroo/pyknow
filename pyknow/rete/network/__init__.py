
"""
Engine walker
-------------

Given a ``pyknow.engine.Engine`` object and a RETE
root node, fill the RETE network starting on the root node.

"""
from contextlib import suppress
from operator import itemgetter

from pyknow.fact import Fact
from pyknow.rete.nodes import FeatureTesterNode, OrdinaryMatchNode
from pyknow.rete.nodes import ConflictSetNode, NotNode
from pyknow.rule import Rule, NOT, AND
from pyknow.rete.network.dnf import dnf
from pyknow.rete.network import callables

PRIORITIES = [1000, 100, 10]
FIRST, SECOND, THIRD = PRIORITIES


def get_callable(key, value):
    """
    Return compare method for specific class, defaults to literal
    comparision
    """
    name = value.__class__.__name__
    getter = getattr(callables, "match_{}".format(name), callables.match_L)
    return getter(key, value)


class EngineWalker:
    """
    Walks trough an engine producing an alpha network.
    """

    def __init__(self, engine, root_node):
        self.engine = engine
        self.root_node = root_node
        self.input_nodes = []

    @staticmethod
    def get_callables(fact):
        """
        Construct the base alpha callables, that check if:

        - Same fact class
        - Its keys are a subset of the other fact's keys
          Only if it does not contain any wildcard.
        - Has its key (if not W mode)
        - Specific condition depending on the fact content.
          - T -> Calls a given callable
          - None (Default) -> Direct value comparision
          - W -> W(True), the key should be in the fact,
                 W(False) the key should not be in the fact.
          - C -> Context comparision
        """

        yield callables.same_class(fact), FIRST

        if not any(isinstance(v.__class__, W) for v in fact.values()):
            yield callables.compatible_facts(fact), SECOND

        for key, value in fact.items():
            if not isinstance(value.__class__, W):
                yield callables.has_key(key), SECOND  # NOQA
            yield get_callable(key, value), THIRD

    def get_alpha_branch(self, alpha_cls, fact):
        """
        Generate an alpha branch, that is:
        - Get the necesary callables to resolve a fact
        - Chain them sorted by priority order
        - Append the input node to the list of input nodes
        """

        # Walk trough nodes by reverse order
        clbs = sorted(EngineWalker.get_callables(fact),
                      key=itemgetter(1), reverse=True)
        nodes = [alpha_cls(a[0]) for a in clbs]
        # self.nodes += nodes
        self.input_nodes.append(nodes[0])
        for num, alpha_node in enumerate(nodes):
            with suppress(IndexError):
                # pylint: disable=protected-access
                alpha_node.add_child(nodes[num+1], nodes[num+1]._activate)
        # Latest node in the list has no children, we return it
        # so its children will be the next node (a beta node)
        return nodes[-1]

    def get_beta_node(self, left, right, cls=OrdinaryMatchNode):
        """
        Given a two-node condition, return a beta node for it.
        If needed, resolve its children.
        """

        # pylint: disable=protected-access
        left_node = self.get_node(left)
        right_node = self.get_node(right)
        beta_node = cls(callables.and_match)
        left_node.add_child(beta_node, beta_node._activate_left)
        right_node.add_child(beta_node, beta_node._activate_right)
        return beta_node

    def get_node(self, cond):
        """
        Return a node for a specific condition
        """

        if isinstance(cond, Rule) and not isinstance(cond, NOT):
            # Return a match node with the two elements on the network
            # This relies on the fact that the network is normalized
            # as 2-element tuples and that a rule is iterable.
            left = next(cond)
            right = next(cond)
            return self.get_beta_node(left, right)
        elif isinstance(cond, NOT):
            # pylint: disable=too-many-function-args
            # pylint fails to interpret the inheritance there...
            return NotNode(next(cond))
        elif isinstance(cond, Fact):
            return self.get_alpha_branch(FeatureTesterNode, cond)
        else:
            raise Exception()

    def build_network(self):
        """
        Generate alpha network and add it to the node tree started at
        ``root_node``
        """

        for rule in self.engine.get_rules():
            # pylint: disable=unidiomatic-typecheck
            if type(rule) is Rule:
                # Rule behaviour defaults to AND, replace it.
                rule_ = AND(*[a for a in rule])
            conds = dnf(rule_)
            if isinstance(conds, Fact):
                conds = [conds]

            # As this has been previously normalized, only two
            # exit nodes can exist at most.
            exit_nodes = [self.get_node(cond) for cond in conds]

            # Add the conflict_set as a children of the Rule's beta node.
            # This is the end of the tree
            conflict_set = ConflictSetNode(rule)

            if len(exit_nodes) == 2:
                # pylint: disable=too-many-function-args, protected-access
                # pylint fails to interpret the inheritance there...
                last_node = OrdinaryMatchNode(callables.and_match)
                exit_nodes[0].add_child(last_node, last_node._activate_left)
                exit_nodes[1].add_child(last_node, last_node._activate_right)
            else:
                last_node = exit_nodes[0]

            # pylint: disable=protected-access
            last_node.add_child(conflict_set, conflict_set._activate)

        for node in self.input_nodes:
            # pylint: disable=protected-access
            self.root_node.add_child(node, node._activate)
