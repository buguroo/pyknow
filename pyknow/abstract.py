import abc

from pyknow.watchers import AGENDA_WATCHER


class Matcher(metaclass=abc.ABCMeta):
    def __init__(self, engine):
        self.engine = engine

    @abc.abstractmethod
    def changes(adding=None, deleting=None):
        """
        Main interface with the matcher.

        Called by the knowledge engine when changes are made in the
        working memory and return a set of activations.

        """
        pass


class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
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
