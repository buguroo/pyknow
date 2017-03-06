import abc


class AbstractNode(metaclass=abc.ABCMeta):
    def __init__(self):
        self.children = set()

    @abc.abstractproperty
    def add_child(self, child, callback):
        """Add a child to `self.children` if necessary."""
        pass


class OneInputNode(AbstractNode):
    def activate(self, token):
        return self._activate(token.copy())

    @abc.abstractproperty
    def _activate(self, token):
        pass


class TwoInputNode(AbstractNode):
    def activate_left(self, token):
        return self._activate_left(token.copy())

    @abc.abstractproperty
    def _activate_left(self, token):
        pass

    def activate_right(self, token):
        return self._activate_right(token.copy())

    @abc.abstractproperty
    def _activate_right(self, token):
        pass
