"""
Factlist related tests
"""
# pylint: disable=invalid-name
import pytest


def test_factlist_is_ordereddict():
    """ Fact list on FactList object is an OrderedDict """

    from pyknow.factlist import FactList
    from collections import OrderedDict
    assert issubclass(FactList, OrderedDict)


def test_factlist_facts_idx_starts_zero():
    """ Factlist idx starts at zero """

    from pyknow.factlist import FactList
    assert getattr(FactList(), "last_index") == 0


def test_factlist_declare_raises_valueError():
    """ declare raises valueerror if not ``Fact`` object providen """

    from pyknow.factlist import FactList
    import pytest

    with pytest.raises(ValueError):
        FactList().declare("Foo")


def test_factlist_declare():
    """ Test declare method adds to factlist and updates index """
    from pyknow.factlist import FactList
    from pyknow import Fact
    flist = FactList()
    assert getattr(flist, "last_index") == 0
    assert not flist
    flist.declare(Fact())
    assert getattr(flist, "last_index") == 1
    assert isinstance(flist[0], Fact)


def test_factlist_retract():
    """ Test retract method """

    from pyknow.factlist import FactList
    from pyknow import Fact
    flist = FactList()
    assert getattr(flist, "last_index") == 0
    assert not flist
    flist.declare(Fact())
    assert getattr(flist, "last_index") == 1
    assert isinstance(flist[0], Fact)
    assert flist.retract(0) == 0
    assert not flist


def test_factlist_changes():
    """ Test factlist changes """

    from pyknow.factlist import FactList
    from pyknow import Fact

    flist = FactList()

    f0 = flist.declare(Fact(a=1))
    assert flist.changes[0] == [f0]

    f1 = flist.declare(Fact(b=1))
    assert flist.changes[0] == [f1]

    flist.retract(f1)
    assert flist.changes[1] == [f1]


def test_factlist_raises_valueerror_on_invalid_fact():
    from pyknow.factlist import FactList
    from pyknow import Fact, Field

    class MockFact(Fact):
        must_be_string = Field(str, mandatory=True)

    flist = FactList()
    f0 = MockFact(must_be_string=0)

    with pytest.raises(ValueError):
        flist.declare(f0)
