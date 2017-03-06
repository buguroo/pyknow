import abc


class AbstractMatcher(metaclass=abc.ABCMeta):
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
