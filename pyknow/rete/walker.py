
"""
Engine walker
-------------

Given a ``pyknow.engine.Engine`` object and a RETE
root node, fill the RETE network starting on the root node.

"""
from contextlib import suppress
from operator import itemgetter

from pyknow.fact import W, Fact
from pyknow.rete.nodes import FeatureTesterNode, OrdinaryMatchNode
from pyknow.rete.nodes import ConflictSetNode, NotNode
from pyknow.rule import Rule, NOT, AND
from pyknow.rete.dnf_rule import dnf

PRIORITIES = [1000, 100, 10]
FIRST, SECOND, THIRD = PRIORITIES


class EngineWalker:
    """
    Walks trough an engine producing an alpha network.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, engine, root_node):
        self.engine = engine
        self.root_node = root_node
        self.input_nodes = []

    @staticmethod
    def normalize_tree(conds, prev_class):
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
                              EngineWalker.normalize_tree(conds, prev_class))

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
        beta_node = cls(Callables.and_match)
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
        # pylint: disable=protected-access

        for rule in self.engine.get_rules():
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
                # pylint: disable=too-many-function-args
                # pylint fails to interpret the inheritance there...
                last_node = OrdinaryMatchNode(Callables.and_match)
                exit_nodes[0].add_child(last_node, last_node._activate_left)
                exit_nodes[1].add_child(last_node, last_node._activate_right)
            else:
                last_node = exit_nodes[0]

            last_node.add_child(conflict_set, conflict_set._activate)

        for node in self.input_nodes:
            self.root_node.add_child(node, node._activate)


class Callables:
    """
    Alpha nodes callables
    """

    @staticmethod
    def and_match(left, right):
        """
        Returns true if all the items in the left dictionary are
        contained in the right dictionary and all the common values
        are the same.
        """
        return not set(left) - set(right)

    @staticmethod
    def match_W(key, value):
        """ Returns alpha for a given key/value pair for type W """
        # pylint: disable=invalid-name
        def _has_key(fact):
            if not value:
                return fact.get(key, None) is None
            else:
                return fact.get(key, None) is not None
        return _has_key

    @staticmethod
    def match_V(key, value):
        """ Returns alpha for a given key/value pair for type V """
        # pylint: disable=invalid-name
        def _get_context(fact):
            if fact.get(key, None) is not None:
                return {value: fact.get(key)}
            return {}

        return _get_context

    @staticmethod
    def match_T(key, value):
        """ Returns alpha for a given key/value pair for type T """
        # pylint: disable=invalid-name
        return lambda fact: value(fact.get(key))

    @staticmethod
    def match_L(key, value):
        """ Returns alpha for a given key/value pair for type L """
        # pylint: disable=invalid-name
        return lambda fact: fact.get(key, None) == value

    @staticmethod
    def has_key(key):
        """
        Return base alpha element for this fact type
        By default we check that we've got the remote key.
        You must preferibly override ``get_alpha``
        if you require that condition to not be met.

        This checks that we've got the key in the checked fact
        """
        return lambda fact: hasattr(fact, key)

    @staticmethod
    def same_class(parent_class):
        """
        Compare fact classes
        """
        # pylint: disable=unidiomatic-typecheck
        # We need to check against the specific class, not any children.
        return lambda fact: type(fact) is parent_class.__class__

    @staticmethod
    def compatible_facts(fact):
        """
        Check if fact keys is a subset of the other fact keys
        """
        return lambda other: set(fact.keys()).issubset(other.keys())

    @staticmethod
    def get_callable(key, value):
        """
        Return compare method for specific class, defaults to literal
        comparision
        """
        name = value.__class__.__name__
        getter = getattr(Callables, "match_{}".format(name), Callables.match_L)
        return getter(key, value)
