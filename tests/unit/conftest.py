from string import ascii_letters
from hypothesis import strategies as st
from pyknow.watchers import watch
import os

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

if os.getenv("TEST_WATCHERS"):
    watch()
