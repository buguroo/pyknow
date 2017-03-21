from collections import defaultdict
from collections import deque
from itertools import chain

from pyknow.abstract import Strategy


def listdict():
    """ Defaultdict of a list """
    return defaultdict(list)


class DepthStrategy(Strategy):
    def _update_agenda(self, agenda, acts):
        old = listdict()
        for a in agenda.activations:
            old[a.rule.salience].append(a)

        new = listdict()
        for a in acts:
            new[a.rule.salience].append(a)

        neworder = deque()
        for salience in sorted(set(new.keys()) | set(old.keys()),
                               reverse=True):
            for a in chain(new[salience], old[salience]):
                if a not in neworder:
                    neworder.append(a)

        agenda.activations = neworder
