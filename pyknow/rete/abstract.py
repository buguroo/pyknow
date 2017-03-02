import abc


class AbstractNode(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def children(self):
        """List of the edges leaving the node."""
        pass
