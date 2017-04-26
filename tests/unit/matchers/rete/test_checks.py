import pytest


def test_featurecheck_exists():
    try:
        from pyknow.matchers.rete.check import FeatureCheck
    except ImportError as exc:
        assert False, exc


def test_featurecheck_convert_nonPCE_to_PCE():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L

    def testfunc():
        pass

    fc = FeatureCheck('somekey', testfunc)

    assert fc.how == L(testfunc)


def test_featurecheck_is_borg_basic_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L

    assert FeatureCheck('somekey', L(1)) is FeatureCheck('somekey', L(1))

    assert FeatureCheck('somekey', L(1)) is not FeatureCheck('somekey', L(2))


def test_featurecheck_is_borg_basic_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P

    def mypredicate1(_):
        return True

    def mypredicate2(_):
        return False

    assert FeatureCheck('somekey', P(mypredicate1)) \
        is FeatureCheck('somekey', P(mypredicate1))

    assert FeatureCheck('somekey', P(mypredicate1)) \
        is not FeatureCheck('otherkey', P(mypredicate1))

    assert FeatureCheck('somekey', P(mypredicate1)) \
        is not FeatureCheck('somekey', P(mypredicate2))


def test_featurecheck_is_borg_basic_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W

    assert FeatureCheck('somekey', W('X')) \
        is FeatureCheck('somekey', W('X'))

    assert FeatureCheck('somekey', W('X')) \
        is not FeatureCheck('somekey', W('Y'))


def test_featurecheck_is_borg_composed_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L

    assert FeatureCheck('somekey', L(1) & L(1)) is FeatureCheck('somekey', L(1) & L(1))
    assert FeatureCheck('somekey', L(1) | L(1)) is FeatureCheck('somekey', L(1) | L(1))
    assert FeatureCheck('somekey', ~L(1)) is FeatureCheck('somekey', ~L(1))


def test_featurecheck_is_borg_composed_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P

    def mypredicate1(_):
        return True

    def mypredicate2(_):
        return False

    def mypredicate3(_):
        return None

    assert FeatureCheck('somekey', P(mypredicate1) & P(mypredicate2)) \
        is FeatureCheck('somekey', P(mypredicate1) & P(mypredicate2))

    assert FeatureCheck('somekey', P(mypredicate1) | P(mypredicate2)) \
        is FeatureCheck('somekey', P(mypredicate1) | P(mypredicate2))

    assert FeatureCheck('somekey', ~P(mypredicate1)) \
        is FeatureCheck('somekey', ~P(mypredicate1))

    assert FeatureCheck('somekey', P(mypredicate1) & P(mypredicate2)) \
        is not FeatureCheck('somekey', P(mypredicate1) & P(mypredicate3))

    assert FeatureCheck('somekey', P(mypredicate1) | P(mypredicate2)) \
        is not FeatureCheck('somekey', P(mypredicate1) | P(mypredicate3))

    assert FeatureCheck('somekey', ~P(mypredicate1)) \
        is not FeatureCheck('somekey', ~P(mypredicate2))


def test_featurecheck_is_borg_composed_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W

    assert FeatureCheck('somekey', W('X') & W()) \
        is FeatureCheck('somekey', W('X') & W())

    assert FeatureCheck('somekey', W('X') | W()) \
        is FeatureCheck('somekey', W('X') | W())

    assert FeatureCheck('somekey', ~W('X')) \
        is FeatureCheck('somekey', ~W('X'))

    assert FeatureCheck('somekey', W('X') & W()) \
        is not FeatureCheck('somekey', W('Y') & W())

    assert FeatureCheck('somekey', W('X') | W()) \
        is not FeatureCheck('somekey', W('Y') | W())

    assert FeatureCheck('somekey', ~W('X')) \
        is not FeatureCheck('somekey', ~W('Y'))


def test_featurecheck_call_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, Fact

    # Positional field not present
    check = FeatureCheck(0, L('mydata'))
    assert not check(Fact())

    # Positional field present, matching and not matching
    check = FeatureCheck(0, L('mydata'))
    assert check(Fact('mydata'))
    check = FeatureCheck(0, L('otherdata'))
    assert not check(Fact('mydata'))

    # Named field present, matching and not matching
    check = FeatureCheck('mykey', L('mydata'))
    assert check(Fact(mykey='mydata'))

    check = FeatureCheck('mykey', L('mydata'))
    assert not check(Fact(mykey='myotherdata'))

    # Named field not present
    check = FeatureCheck('mykey', L('mydata'))
    assert not check(Fact(otherkey='mydata'))

    # Literal with binding, matching and not matching
    check = FeatureCheck('mykey', L('mydata', __bind__='D'))
    assert check(Fact(mykey='mydata')) == {'D': 'mydata'}
    check = FeatureCheck('mykey', L('mydata', __bind__='D'))
    assert check(Fact(mykey='otherdata')) is False


def test_featurecheck_call_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W, Fact

    # Positional field not present
    check = FeatureCheck(0, W())
    assert not check(Fact())

    # Positional field present
    check = FeatureCheck(0, W())
    assert check(Fact('something'))

    # Named field not present
    check = FeatureCheck('mykey', W())
    assert not check(Fact(otherkey='something'))

    # Named field present
    check = FeatureCheck('mykey', W())
    assert check(Fact(mykey='something'))

    # Binding present
    check = FeatureCheck(0, W('X'))
    assert check(Fact('something')) == {'X': 'something'}

    # Binding not present
    check = FeatureCheck(0, W('X'))
    assert check(Fact()) is False


def test_featurecheck_call_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P, Fact


    # Positional field not present
    check = FeatureCheck(0, P(lambda _: True))
    assert not check(Fact())

    # Positional field matching
    check = FeatureCheck(0, P(lambda _: True))
    assert check(Fact('something'))
    check = FeatureCheck(0, P(lambda val: val > 0))
    assert check(Fact(1))

    # Positional field not matching
    check = FeatureCheck(0, P(lambda val: val <= 0))
    assert not check(Fact(1))

    # Positional field matching with binding
    check = FeatureCheck(0, P(lambda val: True, __bind__='K'))
    assert check(Fact(1)) == {'K': 1}


def test_featurecheck_call_not_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, Fact

    # Positional matching (negated)
    check = FeatureCheck(0, ~L('somedata'))
    assert not check(Fact('somedata'))

    # Positional not matching (negated)
    check = FeatureCheck(0, ~L('somedata'))
    assert check(Fact('otherdata'))


def test_featurecheck_call_not_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P, Fact

    # Positional matching (negated)
    check = FeatureCheck(0, ~P(lambda _: True))
    assert not check(Fact('somedata'))

    # Positional not matching (negated)
    check = FeatureCheck(0, ~P(lambda _: False))
    assert check(Fact('somedata'))


def test_featurecheck_call_not_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W, Fact

    # Positional match (negated)
    check = FeatureCheck(0, ~W())
    assert not check(Fact('somedata'))

    # Positional match (negated) with binding
    check = FeatureCheck(0, ~W('X'))
    assert check(Fact('somedata')) == {(False, 'X'): 'somedata'}


def test_featurecheck_call_and():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, P, W, Fact

    # Positional, composed and matching 
    check = FeatureCheck(0, L('mydata') & P(lambda _: True) & W())
    assert check(Fact('mydata'))


    # Positional, composed and matching (with binding)
    check = FeatureCheck(0, L('mydata') & W('X'))
    assert check(Fact('mydata')) == {'X': 'mydata'}

    # Positional, composed and matching (with binding negated)
    check = FeatureCheck(0, L('mydata') & ~W('X'))
    assert check(Fact('mydata')) == {(False, 'X'): 'mydata'}


def test_featurecheck_call_or():
    """
    Or is normally not checked with FeatureCheck because is normalized
    out during DNF.

    """
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, P, W, Fact

    check = FeatureCheck(0, L('mydata') | P(lambda _: True) & W())
    assert check(Fact('mydata'))
    check = FeatureCheck(0, L('mydata') | W('X'))
    assert check(Fact('mydata')) is True

    check = FeatureCheck(0, W('X') | L('mydata'))
    assert check(Fact('mydata')) == {'X': 'mydata'}

    check = FeatureCheck(0, L('mydata') | ~L('otherdata'))
    assert check(Fact('mydata'))
    check = FeatureCheck(0, ~L('otherdata') | L('mydata'))
    assert check(Fact('mydata'))

    check = FeatureCheck(0, ~L('mydata') | L('otherdata'))
    assert not check(Fact('mydata'))
    check = FeatureCheck(0, L('otherdata') | ~L('mydata'))
    assert not check(Fact('mydata'))
