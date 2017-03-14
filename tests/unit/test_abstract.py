import pytest


@pytest.mark.wip
def test_matcher_exists():
    try:
        from pyknow.abstract import Matcher
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_matcher_interface():
    from pyknow.abstract import Matcher

    assert Matcher.__abstractmethods__ == {'changes'}
