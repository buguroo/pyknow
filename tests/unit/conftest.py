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
    """
    Simple Rule subclass to test Rule._check_pattern method functionality.

    """
    from pyknow.rule import Rule
    class SRule(Rule):
        def __eval__(self, facts=None):
            for k in self.patterns:
                return self._check_pattern(k, facts)
    return SRule

@pytest.fixture
def RRule():
    """Simple Rule subclass to test Rule *args."""
    from pyknow.rule import Rule
    class RRule(Rule):
        def __eval__(self, facts=None):
            return list(self._check_args(facts))

    return RRule

@pytest.fixture
def LRule():
    """Simple Rule subclass to operator nesting."""
    from pyknow.rule import Rule
    class LRule(Rule):
        def __eval__(self, facts=None):
            return self.args[0]

    return LRule
