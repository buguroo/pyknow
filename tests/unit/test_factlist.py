"""
Factlist related tests
"""
# pylint: disable=invalid-name


def test_factlist_has_facts():
    """ Factlist object has a fact list """
    from pyknow.factlist import FactList
    assert hasattr(FactList(), "facts")


def test_factlist_facts_are_ordereddict():
    """ Fact list on FactList object is an OrderedDict """

    from pyknow.factlist import FactList
    from collections import OrderedDict
    assert isinstance(getattr(FactList(), "facts"), OrderedDict)


def test_factlist_facts_idx_starts_zero():
    """ Factlist idx starts at zero """

    from pyknow.factlist import FactList
    assert getattr(FactList(), "_fidx") == 0


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
    assert getattr(flist, "_fidx") == 0
    assert not flist.facts
    flist.declare(Fact())
    assert getattr(flist, "_fidx") == 1
    assert isinstance(flist.facts[0], Fact)


def test_factlist_retract():
    """ Test retract method """

    from pyknow.factlist import FactList
    from pyknow import Fact
    flist = FactList()
    assert getattr(flist, "_fidx") == 0
    assert not flist.facts
    flist.declare(Fact())
    assert getattr(flist, "_fidx") == 1
    assert isinstance(flist.facts[0], Fact)
    assert flist.retract(0) == 0
    assert not flist.facts


def test_factlist_retract_matching():
    """ Test retract_matching method """

    from pyknow.factlist import FactList
    from pyknow import Fact
    flist = FactList()
    assert getattr(flist, "_fidx") == 0
    assert not flist.facts
    flist.declare(Fact())
    assert getattr(flist, "_fidx") == 1
    assert isinstance(flist.facts[0], Fact)
    assert flist.retract_matching(Fact()) == [0]
    assert not flist.facts


def test_factlist_changes():
    """ Test factlist changes """

    from pyknow.factlist import FactList
    from pyknow import Fact
    flist = FactList()

    flist.declare(Fact(a=1))
    assert flist.changes[0] == {Fact(a=1)}

    flist.declare(Fact(b=1))
    assert flist.changes[0] == {Fact(b=1)}

    flist.retract_matching(Fact(b=1))
    assert flist.changes[1] == {Fact(b=1)}
