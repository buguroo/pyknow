from collections import defaultdict, deque
from itertools import chain
import operator as op

from pyknow.abstract import Strategy


def listdict():
    """ Defaultdict of a list """
    return defaultdict(deque)


class DepthStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_agenda(self, agenda, added, removed):
        activations = list(agenda.activations)
        activations.extend(added)

        for act in removed:
            try:
                activations.remove(act)
            except ValueError:
                # Already executed rule.
                pass

        sorted_activations = sorted(
            enumerate(activations),
            key=lambda x: (x[1].rule.salience,
                           sorted((f['__factid__'] for f in x[1].facts),
                                  reverse=True)),
            reverse=True)

        return (act for _, act in sorted_activations)
