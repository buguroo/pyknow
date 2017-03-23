"""Abstract base classes for the RETE implementation."""
import abc


class Node(metaclass=abc.ABCMeta):
    """Node interface."""

    def __init__(self):
        """Initialize `self.children` and reset the node own memory."""
        self.children = list()
        self._reset()  # Reset it's OWN memory.

    @abc.abstractmethod
    def add_child(self, child, callback):
        """Add a child to `self.children` if necessary."""
        pass

    def reset(self):
        """Reset itself and recursively all its children."""
        self._reset()
        for child in self.children:
            child.reset()

    @abc.abstractmethod
    def _reset(self):
        """Reset this node's memory."""
        pass

    def __repr__(self):
        return ""


class OneInputNode(Node):
    """Nodes which only have one input port."""

    def activate(self, token):
        """Make a copy of the received token and call `self._activate`."""
        return self._activate(token.copy())

    @abc.abstractproperty
    def _activate(self, token):
        """Node activation routine."""
        pass


class TwoInputNode(Node):
    """Nodes which have two input ports: left and right."""

    def activate_left(self, token):
        """Make a copy of the received token and call `_activate_left`."""
        return self._activate_left(token.copy())

    @abc.abstractproperty
    def _activate_left(self, token):
        """Node left activation routine."""
        pass

    def activate_right(self, token):
        """Make a copy of the received token and call `_activate_right`."""
        return self._activate_right(token.copy())

    @abc.abstractproperty
    def _activate_right(self, token):
        """Node right activation routine."""
        pass


class Check(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, fact):
        """
        Given a `Fact` or a subclass of `Fact`, return:

            * `True` if the check matched.
            * `False` if the check didn't match.
            * A non empty `Mapping` meaning the check matched and yield
              some context.

        """
        pass
