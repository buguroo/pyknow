from abc import ABCMeta, abstractmethod
from collections import deque
from collections import defaultdict
from itertools import chain
from pyknow.watchers import AGENDA_WATCHER

listdict = lambda:defaultdict(list)


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def _update_agenda(self, agenda, acts):
        pass

    def update_agenda(self, agenda, acts):
        acts_set = set(acts)

        # Remove executed activations from the activation list
        nonexecuted = acts_set - agenda.executed

        # Resolve conflicts using the appropiate strategy.
        res = self._update_agenda(agenda, nonexecuted)

        # Update executed set removing activations not found in the
        # current set.
        agenda.executed = acts_set & agenda.executed

        AGENDA_WATCHER.debug("Agenda updated: %s", agenda)
        return res


class Depth(Strategy):
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
