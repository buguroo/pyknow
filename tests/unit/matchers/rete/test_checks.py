import pytest


def test_check_exists():
    try:
        from pyknow.matchers.rete.checks import Check
    except ImportError as exc:
        assert False, exc


def test_check_accepts_PCE():
    from pyknow.matchers.rete.checks import Check
    from pyknow.rule import PredicatePCE

    with pytest.raises(TypeError):
        Check('somekey', lambda _: None)

    # MUST NOT RAISE
    Check('somekey', PredicatePCE(lambda _: None))

def test_check_is_borg_basic_literal():
    from pyknow.matchers.rete.checks import Check
    from pyknow import L

    assert Check('somekey', L(1)) is Check('somekey', L(1))

    assert Check('somekey', L(1)) is not Check('somekey', L(2))


def test_check_is_borg_basic_predicate():
    from pyknow.matchers.rete.checks import Check
    from pyknow import P

    assert Check('somekey', P(lambda _: True)) \
        is Check('somekey', P(lambda _: True))

    assert Check('somekey', P(lambda _: True)) \
        is not Check('otherkey', P(lambda _: True))

    assert Check('somekey', P(lambda _: True)) \
        is not Check('somekey', P(lambda _: False))


def test_check_is_borg_basic_wildcard():
    from pyknow.matchers.rete.checks import Check
    from pyknow import W

    assert Check('somekey', W(bind_to='X')) \
        is Check('somekey', W(bind_to='X'))

    assert Check('somekey', W(bind_to='X')) \
        is not Check('somekey', W(bind_to='Y'))


def test_check_is_borg_composed_literal():
    from pyknow.matchers.rete.checks import Check
    from pyknow import L

    assert Check('somekey', L(1) & L(1)) is Check('somekey', L(1) & L(1))
    assert Check('somekey', L(1) | L(1)) is Check('somekey', L(1) | L(1))
    assert Check('somekey', ~L(1)) is Check('somekey', ~L(1))


def test_check_is_borg_composed_predicate():
    from pyknow.matchers.rete.checks import Check
    from pyknow import P

    assert Check('somekey', P(lambda _: True) & P(lambda _: False)) \
        is Check('somekey', P(lambda _: True) & P(lambda _: False))

    assert Check('somekey', P(lambda _: True) | P(lambda _: False)) \
        is Check('somekey', P(lambda _: True) | P(lambda _: False))

    assert Check('somekey', ~P(lambda _: True)) \
        is Check('somekey', ~P(lambda _: True))

    assert Check('somekey', P(lambda _: True) & P(lambda _: False)) \
        is not Check('somekey', P(lambda _: True) & P(lambda _: None))

    assert Check('somekey', P(lambda _: True) | P(lambda _: False)) \
        is not Check('somekey', P(lambda _: True) | P(lambda _: None))

    assert Check('somekey', ~P(lambda _: True)) \
        is not Check('somekey', ~P(lambda _: False))


def test_check_is_borg_composed_wildcard():
    from pyknow.matchers.rete.checks import Check
    from pyknow import W

    assert Check('somekey', W(bind_to='X') & W()) \
        is Check('somekey', W(bind_to='X') & W())

    assert Check('somekey', W(bind_to='X') | W()) \
        is Check('somekey', W(bind_to='X') | W())

    assert Check('somekey', ~W(bind_to='X')) \
        is Check('somekey', ~W(bind_to='X'))

    assert Check('somekey', W(bind_to='X') & W()) \
        is not Check('somekey', W(bind_to='Y') & W())

    assert Check('somekey', W(bind_to='X') | W()) \
        is not Check('somekey', W(bind_to='Y') | W())

    assert Check('somekey', ~W(bind_to='X')) \
        is not Check('somekey', ~W(bind_to='Y'))


def test_check_call_literal():
    from pyknow.matchers.rete.checks import Check
    from pyknow import L, Fact

    assert not Check(0, L('mydata'))(Fact())

    assert Check(0, L('mydata'))(Fact('mydata'))
    assert not Check(0, L('otherdata'))(Fact('mydata'))

    assert Check('mykey', L('mydata'))(Fact(mykey='mydata'))
    assert not Check('mykey', L('mydata'))(Fact(otherkey='mydata'))


def test_check_call_wildcard():
    from pyknow.matchers.rete.checks import Check
    from pyknow import W, Fact

    assert not Check(0, W())(Fact())

    assert Check(0, W())(Fact('something'))

    assert Check('mykey', W())(Fact(mykey='something'))
    assert not Check('mykey', W())(Fact(otherkey='something'))

    assert Check(0, W(bind_to='X'))(Fact('something')) == {'X': 'something'}
    assert Check(0, W(bind_to='X'))(Fact()) is False


def test_check_call_predicate():
    from pyknow.matchers.rete.checks import Check
    from pyknow import P, Fact

    assert not Check(0, P(lambda _: True))(Fact())
    assert Check(0, P(lambda _: True))(Fact('something'))

    assert Check(0, P(lambda val: val > 0))(Fact(1))
    assert not Check(0, P(lambda val: val <= 0))(Fact(1))

    assert Check(0, P(lambda val: {'K': val}))(Fact(1)) == {'K': 1}


def test_check_call_not_literal():
    from pyknow.matchers.rete.checks import Check
    from pyknow import L, Fact

    assert not Check(0, ~L('somedata'))(Fact('somedata'))
    assert Check(0, ~L('somedata'))(Fact('otherdata'))


def test_check_call_not_predicate():
    from pyknow.matchers.rete.checks import Check
    from pyknow import P, Fact

    assert not Check(0, ~P(lambda _: True))(Fact('somedata'))
    assert Check(0, ~P(lambda _: False))(Fact('somedata'))


def test_check_call_not_wildcard():
    from pyknow.matchers.rete.checks import Check
    from pyknow import W, Fact

    assert not Check(0, ~W())(Fact('somedata'))
    assert not Check(0, ~W(bind_to='X'))(Fact('somedata'))


def test_check_call_and():
    from pyknow.matchers.rete.checks import Check
    from pyknow import L, P, W, Fact

    assert Check(0, L('mydata') & P(lambda _: True) & W())(Fact('mydata'))
    assert Check(0, L('mydata') \
                    & W(bind_to='X'))(Fact('mydata')) == {'X': 'mydata'}

    assert not Check(0, L('mydata') & ~W(bind_to='X'))(Fact('mydata'))


def test_check_call_or():
    """
    Or is normally not checked with Check because is normalized out during DNF.

    """
    from pyknow.matchers.rete.checks import Check
    from pyknow import L, P, W, Fact

    assert Check(0, L('mydata') | P(lambda _: True) & W())(Fact('mydata'))
    assert Check(0, L('mydata') | W(bind_to='X'))(Fact('mydata')) is True

    assert Check(0, W(bind_to='X') \
                    | L('mydata'))(Fact('mydata')) == {'X': 'mydata'}

    assert Check(0, L('mydata') | ~L('otherdata'))(Fact('mydata'))
    assert Check(0, ~L('otherdata') | L('mydata'))(Fact('mydata'))

    assert not Check(0, ~L('mydata') | L('otherdata'))(Fact('mydata'))
    assert not Check(0, L('otherdata') | ~L('mydata'))(Fact('mydata'))
