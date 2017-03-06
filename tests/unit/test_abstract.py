import pytest


@pytest.mark.wip
def test_matcher_exists():
    try:
        from pyknow.abstract import AbstractMatcher
    except ImportError as exc:
        assert False, exc


@pytest.mark.wip
def test_matcher_interface():
    from pyknow.abstract import AbstractMatcher

    assert AbstractMatcher.__abstractmethods__ == {'changes'}
