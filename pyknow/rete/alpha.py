"""
Alpha nodes
"""
from contextlib import suppress
from operator import itemgetter

from pyknow.engine import KnowledgeEngine
from pyknow.fact import W, Fact
from pyknow.rete import PRIORITIES
from pyknow.rete.callables import Callables
from pyknow.rete.nodes import FeatureTesterNode, OrdinaryMatchNode
from pyknow.rete.nodes import ConflictSetNode
from pyknow.rule import Rule, OR, NOT

FIRST, SECOND, THIRD = PRIORITIES


class EngineWalker:
    """
    EngineWalker.

    Walks trough an engine producing an alpha network.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, engine):
        assert isinstance(engine, KnowledgeEngine)
        self.engine = engine
        self.nodes = []
        self.input_nodes = []

    @staticmethod
    def normalize_branch(conds, prev_class):
        r"""
        Given a branch, ensure that it always has two-elements.
        If needed, anidate its children in its own class, as in:

        Tree
          \-> Branch1
               \-> Element1
               \-> Element2
               \-> Element3

        Tree
          \-> Branch1
               \-> Element1
                \-> Branch1.2
                     \-> Element2
                     \-> Element3
        """
        conds = list(conds)
        first_cond = conds.pop()
        if not conds:
            # We finished processing the network.
            # This should only happen when we have something like:
            # AND(AND(Fact=1))
            return prev_class(first_cond)
        elif len(conds) == 1:
            # We finished processing the tree
            return prev_class(first_cond, conds.pop())
        elif len(conds) > 1:
            # We still need to resolve part of the tree
            return prev_class(first_cond,
                              EngineWalker.normalize_branch(conds, prev_class))

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
        yield Callables.same_class(fact), FIRST

        if not any(isinstance(v.__class__, W) for v in fact.values()):
            yield Callables.compatible_facts(fact), SECOND

        for key, value in fact.items():
            if not isinstance(value.__class__, W):
                yield Callables.has_key(key), SECOND  # NOQA
            yield Callables.get_callable(key, value), THIRD

    def get_alpha_branch(self, alpha_cls, fact):
        """
        Generate an alpha branch, that is:
        - Get the necesary callables to resolve a fact
        - Chain them sorted by priority order
        - Append the nodes to be able to reset() later
        - Append the input node to the list of input nodes

        """
        clbs = sorted(EngineWalker.get_callables(fact),
                      key=itemgetter(1), reverse=True)
        nodes = [alpha_cls(a[0]) for a in clbs]
        self.nodes += nodes
        self.input_nodes.append(nodes[0])
        for num, alpha_node in enumerate(nodes):
            with suppress(IndexError):
                # pylint: disable=protected-access
                alpha_node.add_child(nodes[num+1], nodes[num+1]._activate)
        # Latest node in the list has no children, we return it
        # so its children will be the next node (a beta node)
        return nodes[-1]

    def get_beta_node(self, left, right):
        """
        Given a two-node condition, return a beta node for it.
        If needed, resolve its children.
        """
        # pylint: disable=protected-access
        left_node = self.get_node(left)
        right_node = self.get_node(right)
        beta_node = OrdinaryMatchNode(Callables.and_match)
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
            return self.get_beta_node(cond[0], cond[1])
        elif isinstance(cond, NOT):
            # yield NotNode(network(cond, cls))
            raise NotImplementedError()
        elif isinstance(cond, OR):
            raise NotImplementedError()
        elif isinstance(cond, Fact):
            return self.get_alpha_branch(FeatureTesterNode, cond)
        else:
            raise Exception()

    def get_network(self):
        """ Generate alpha network """
        # pylint: disable=protected-access

        for rule in self.engine.get_rules():
            beta_node = OrdinaryMatchNode(Callables.and_match)

            conds = EngineWalker.normalize_branch(rule, rule.__class__)
            last_nodes = [self.get_node(cond) for cond in conds]
            left_node = last_nodes.pop()

            if last_nodes:
                right_node = last_nodes.pop()
            else:
                right_node = FeatureTesterNode(lambda x: True)

            left_node.add_child(beta_node, beta_node._activate_left)
            right_node.add_child(beta_node, beta_node._activate_right)

            conflict_set = ConflictSetNode(rule)
            beta_node.add_child(conflict_set, conflict_set._activate)
            yield conflict_set
