from abc import ABCMeta, abstractmethod
from collections import deque
from collections import defaultdict
from itertools import chain

listdict = lambda:defaultdict(list)


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def update_agenda(self, agenda, acts):
        pass


class Depth(Strategy):
    def update_agenda(self, agenda, acts):
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
                neworder.append(a)

        agenda.activations = neworder
