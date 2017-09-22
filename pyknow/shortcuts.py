from .conditionalelement import TEST
from .fieldconstraint import W


class _MATCH:
    """
    Helps replacing this:
    "something" << W()

    With this:
    MATCH.something
    """
    def __getattr__(self, name):
        return (name << W())


MATCH = _MATCH()
