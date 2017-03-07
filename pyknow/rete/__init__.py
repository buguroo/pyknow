"""
RETE algorithm implementation.

This is implemented as described by Charles L. Forgy in his original
Ph.D thesis paper_. With minor changes to allow CLIPS like matching and
a more pythonic approach.

.. _paper: http://reports-archive.adm.cs.cmu.edu/anon/scan/CMU-CS-79-forgy.pdf

"""
from pyknow.abstract import AbstractMatcher
from .nodes import BusNode


class ReteMatcher(AbstractMatcher):
    """RETE algorithm with `pyknow` matcher interface."""

    def __init__(self, *args, **kwargs):
        """Create the RETE network for `self.engine`."""
        super().__init__(*args, **kwargs)
        self.root_node = BusNode()

    def changes(adding=None, deleting=None):
        """Transform the given facts to tokens and activate the root node."""
        pass
