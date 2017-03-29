from collections import deque


class Agenda:
    """

    Collection of activations that handles its execution state.

    .. note::
       Extracted from clips documentation: ``The agenda is a collection
       of activations which are those rules which match pattern entities``

    """
    def __init__(self):
        self.activations = deque()

    def __repr__(self):  # pragma: no cover
        return "\n".join(
            "{idx}: {rule} {facts}".format(idx=idx,
                                           rule=act.rule.__name__,
                                           facts=act.facts)
            for idx, act in enumerate(self.activations))

    def get_next(self):
        """Returns the next activation, removes it from activations list."""

        try:
            return self.activations.popleft()
        except IndexError:
            return None
