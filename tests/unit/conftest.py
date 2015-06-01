import pytest

@pytest.fixture
def DRule():
    """Dummy Rule subclass to test Rule class functionality."""
    from pyknow.rule import Rule
    class DRule(Rule):
        def __eval__(self, facts=None):
            return True
    return DRule

@pytest.fixture
def SRule():
    """Simple Rule subclass to test Rule class functionality."""
    from pyknow.rule import Rule
    class SRule(Rule):
        def __eval__(self, facts=None):
            for k in self.conds:
                return self._check(k, facts)
    return SRule
