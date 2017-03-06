from collections import namedtuple
from collections.abc import Callable, Mapping

from .abstract import AbstractNode, OneInputNode
from .token import Token

ChildNode = namedtuple('ChildNode', ['node', 'callback'])


class AnyChild:
    def add_child(self, node, callback):
        self.children.add(ChildNode(node, callback))


class BusNode(AnyChild, AbstractNode):
    def add(self, fact):
        token = Token.valid(fact)
        for child in self.children:
            child.callback(token)

    def remove(self, fact):
        token = Token.invalid(fact)
        for child in self.children:
            child.callback(token)


class FeatureTesterNode(AnyChild, OneInputNode):
    def __init__(self, matcher):
        try:
            assert isinstance(matcher, Callable)
        except AssertionError as exc:
            raise TypeError(exc) from exc
        else:
            self.matcher = matcher

        super().__init__()

    def _activate(self, token):
        match = self.matcher(token)
        if match:
            if isinstance(match, Mapping):
                token.context.update(match)
            for child in self.children:
                child.callback(token)
