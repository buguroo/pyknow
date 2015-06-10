import pytest
from hypothesis import strategies as st

random_types = st.one_of(st.integers(),
                         st.booleans(),
                         st.floats(),
                         st.complex_numbers(),
                         st.tuples(st.text()),
                         st.lists(st.text()),
                         st.sets(st.text()),
                         st.text(),
                         st.dictionaries(keys=st.text(), values=st.text()))
