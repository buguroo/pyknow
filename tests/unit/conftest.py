from string import ascii_letters
import os

from hypothesis import strategies as st
import pytest


random_types = st.one_of(st.integers(),
                         st.booleans(),
                         st.floats(),
                         st.complex_numbers(),
                         st.tuples(st.text()),
                         st.lists(st.text()),
                         st.sets(st.text()),
                         st.text(),
                         st.dictionaries(keys=st.text(), values=st.text()))


random_kwargs = st.dictionaries(keys=st.text(alphabet=ascii_letters,
                                             min_size=1),
                                values=st.text())


@pytest.fixture
def TestNode():
    class _TestNode:
        """
        This is a test node only for testing.

        Adds any token passed to the activation function to `self.added`.

        """
        def __init__(self):
            self.added = []
            self.children = []

        def activate(self, token):
            self.added.append(token)
    return _TestNode
