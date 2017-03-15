import pytest


def test_featurecheck_exists():
    try:
        from pyknow.matchers.rete.check import FeatureCheck
    except ImportError as exc:
        assert False, exc


def test_featurecheck_accepts_PCE():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow.rule import PredicatePCE

    with pytest.raises(TypeError):
        FeatureCheck('somekey', lambda _: None)

    # MUST NOT RAISE
    FeatureCheck('somekey', PredicatePCE(lambda _: None))

def test_featurecheck_is_borg_basic_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L

    assert FeatureCheck('somekey', L(1)) is FeatureCheck('somekey', L(1))

    assert FeatureCheck('somekey', L(1)) is not FeatureCheck('somekey', L(2))


def test_featurecheck_is_borg_basic_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P

    assert FeatureCheck('somekey', P(lambda _: True)) \
        is FeatureCheck('somekey', P(lambda _: True))

    assert FeatureCheck('somekey', P(lambda _: True)) \
        is not FeatureCheck('otherkey', P(lambda _: True))

    assert FeatureCheck('somekey', P(lambda _: True)) \
        is not FeatureCheck('somekey', P(lambda _: False))


def test_featurecheck_is_borg_basic_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W

    assert FeatureCheck('somekey', W(bind_to='X')) \
        is FeatureCheck('somekey', W(bind_to='X'))

    assert FeatureCheck('somekey', W(bind_to='X')) \
        is not FeatureCheck('somekey', W(bind_to='Y'))


def test_featurecheck_is_borg_composed_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L

    assert FeatureCheck('somekey', L(1) & L(1)) is FeatureCheck('somekey', L(1) & L(1))
    assert FeatureCheck('somekey', L(1) | L(1)) is FeatureCheck('somekey', L(1) | L(1))
    assert FeatureCheck('somekey', ~L(1)) is FeatureCheck('somekey', ~L(1))


def test_featurecheck_is_borg_composed_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P

    assert FeatureCheck('somekey', P(lambda _: True) & P(lambda _: False)) \
        is FeatureCheck('somekey', P(lambda _: True) & P(lambda _: False))

    assert FeatureCheck('somekey', P(lambda _: True) | P(lambda _: False)) \
        is FeatureCheck('somekey', P(lambda _: True) | P(lambda _: False))

    assert FeatureCheck('somekey', ~P(lambda _: True)) \
        is FeatureCheck('somekey', ~P(lambda _: True))

    assert FeatureCheck('somekey', P(lambda _: True) & P(lambda _: False)) \
        is not FeatureCheck('somekey', P(lambda _: True) & P(lambda _: None))

    assert FeatureCheck('somekey', P(lambda _: True) | P(lambda _: False)) \
        is not FeatureCheck('somekey', P(lambda _: True) | P(lambda _: None))

    assert FeatureCheck('somekey', ~P(lambda _: True)) \
        is not FeatureCheck('somekey', ~P(lambda _: False))


def test_featurecheck_is_borg_composed_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W

    assert FeatureCheck('somekey', W(bind_to='X') & W()) \
        is FeatureCheck('somekey', W(bind_to='X') & W())

    assert FeatureCheck('somekey', W(bind_to='X') | W()) \
        is FeatureCheck('somekey', W(bind_to='X') | W())

    assert FeatureCheck('somekey', ~W(bind_to='X')) \
        is FeatureCheck('somekey', ~W(bind_to='X'))

    assert FeatureCheck('somekey', W(bind_to='X') & W()) \
        is not FeatureCheck('somekey', W(bind_to='Y') & W())

    assert FeatureCheck('somekey', W(bind_to='X') | W()) \
        is not FeatureCheck('somekey', W(bind_to='Y') | W())

    assert FeatureCheck('somekey', ~W(bind_to='X')) \
        is not FeatureCheck('somekey', ~W(bind_to='Y'))


def test_featurecheck_call_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, Fact

    assert not FeatureCheck(0, L('mydata'))(Fact())

    assert FeatureCheck(0, L('mydata'))(Fact('mydata'))
    assert not FeatureCheck(0, L('otherdata'))(Fact('mydata'))

    assert FeatureCheck('mykey', L('mydata'))(Fact(mykey='mydata'))
    assert not FeatureCheck('mykey', L('mydata'))(Fact(otherkey='mydata'))


def test_featurecheck_call_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W, Fact

    assert not FeatureCheck(0, W())(Fact())

    assert FeatureCheck(0, W())(Fact('something'))

    assert FeatureCheck('mykey', W())(Fact(mykey='something'))
    assert not FeatureCheck('mykey', W())(Fact(otherkey='something'))

    assert FeatureCheck(0, W(bind_to='X'))(Fact('something')) == {'X': 'something'}
    assert FeatureCheck(0, W(bind_to='X'))(Fact()) is False


def test_featurecheck_call_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P, Fact

    assert not FeatureCheck(0, P(lambda _: True))(Fact())
    assert FeatureCheck(0, P(lambda _: True))(Fact('something'))

    assert FeatureCheck(0, P(lambda val: val > 0))(Fact(1))
    assert not FeatureCheck(0, P(lambda val: val <= 0))(Fact(1))

    assert FeatureCheck(0, P(lambda val: {'K': val}))(Fact(1)) == {'K': 1}


def test_featurecheck_call_not_literal():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, Fact

    assert not FeatureCheck(0, ~L('somedata'))(Fact('somedata'))
    assert FeatureCheck(0, ~L('somedata'))(Fact('otherdata'))


def test_featurecheck_call_not_predicate():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import P, Fact

    assert not FeatureCheck(0, ~P(lambda _: True))(Fact('somedata'))
    assert FeatureCheck(0, ~P(lambda _: False))(Fact('somedata'))


def test_featurecheck_call_not_wildcard():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import W, Fact

    assert not FeatureCheck(0, ~W())(Fact('somedata'))
    assert not FeatureCheck(0, ~W(bind_to='X'))(Fact('somedata'))


def test_featurecheck_call_and():
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, P, W, Fact

    assert FeatureCheck(0, L('mydata') & P(lambda _: True) & W())(Fact('mydata'))
    assert FeatureCheck(0, L('mydata') \
                    & W(bind_to='X'))(Fact('mydata')) == {'X': 'mydata'}

    assert not FeatureCheck(0, L('mydata') & ~W(bind_to='X'))(Fact('mydata'))


def test_featurecheck_call_or():
    """
    Or is normally not checked with FeatureCheck because is normalized out during DNF.

    """
    from pyknow.matchers.rete.check import FeatureCheck
    from pyknow import L, P, W, Fact

    assert FeatureCheck(0, L('mydata') | P(lambda _: True) & W())(Fact('mydata'))
    assert FeatureCheck(0, L('mydata') | W(bind_to='X'))(Fact('mydata')) is True

    assert FeatureCheck(0, W(bind_to='X') \
                    | L('mydata'))(Fact('mydata')) == {'X': 'mydata'}

    assert FeatureCheck(0, L('mydata') | ~L('otherdata'))(Fact('mydata'))
    assert FeatureCheck(0, ~L('otherdata') | L('mydata'))(Fact('mydata'))

    assert not FeatureCheck(0, ~L('mydata') | L('otherdata'))(Fact('mydata'))
    assert not FeatureCheck(0, L('otherdata') | ~L('mydata'))(Fact('mydata'))
