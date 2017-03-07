"""
RETE algorithm implementation.

This is implemented as described by Charles L. Forgy in his original
Ph.D thesis paper_. With minor changes to allow CLIPS like matching and
a more pythonic approach.

.. _paper: http://reports-archive.adm.cs.cmu.edu/anon/scan/CMU-CS-79-forgy.pdf

"""
from functools import lru_cache

from pyknow.abstract import AbstractMatcher
from .nodes import BusNode, ConflictSetNode
from .token import Token

PRIORITIES = [1000, 100, 10]


class ReteMatcher(AbstractMatcher):
    """RETE algorithm with `pyknow` matcher interface."""

    def __init__(self, *args, **kwargs):
        """Create the RETE network for `self.engine`."""
        super().__init__(*args, **kwargs)
        self.root_node = BusNode()

    @lru_cache(maxsize=1)
    def _get_conflict_set_nodes(self):
        def _get_csn(node):
            if isinstance(node, ConflictSetNode):
                yield node
            for child in node.children:
                yield from _get_csn(child.node)

        return list(_get_csn(self.root_node))

    def changes(self, adding=None, deleting=None):
        """Pass the given changes to the root_node."""
        if adding is not None:
            for added in adding:
                self.root_node.add(added)
        if deleting is not None:
            for deleted in deleting:
                self.root_node.remove(deleted)

        activations = []
        for csn in self._get_conflict_set_nodes():
            activations += csn.get_activations()
        return activations
