from collections import namedtuple
from collections.abc import Callable, Mapping
from contextlib import suppress

from .abstract import AbstractNode, OneInputNode, TwoInputNode
from .token import Token

ChildNode = namedtuple('ChildNode', ['node', 'callback'])


class AnyChild:
    def add_child(self, node, callback):
        self.children.add(ChildNode(node, callback))


class HaveMatcher:
    def __init__(self, matcher):
        try:
            assert isinstance(matcher, Callable)
        except AssertionError as exc:
            raise TypeError(exc) from exc
        else:
            self.matcher = matcher

        super().__init__()


class BusNode(AnyChild, AbstractNode):
    def add(self, fact):
        token = Token.valid(fact)
        for child in self.children:
            child.callback(token)

    def remove(self, fact):
        token = Token.invalid(fact)
        for child in self.children:
            child.callback(token)


class FeatureTesterNode(AnyChild, HaveMatcher, OneInputNode):
    def _activate(self, token):
        match = self.matcher(token)
        if match:
            if isinstance(match, Mapping):
                token.context.update(match)
            for child in self.children:
                child.callback(token)


class OrdinaryMatchNode(AnyChild, HaveMatcher, TwoInputNode):
    def __init__(self, *args, **kwargs):
        self.left_memory = []
        self.right_memory = []
        super().__init__(*args, **kwargs)

    def _activate_left(self, token):
        if token.is_valid():
            self.left_memory.append((token.data, token.context))
        else:
            with suppress(ValueError):
                self.left_memory.remove((token.data, token.context))

        for right_data, right_context in self.right_memory:
            match = self.matcher(token.context, right_context)
            if match:
                if not isinstance(match, Mapping):
                    match = {}

                match.update(token.context)
                match.update(right_context)
                newtoken = Token(token.tag,
                                 token.data | right_data,
                                 match)
                for child in self.children:
                    child.callback(newtoken)

    def _activate_right(self, token):
        if token.is_valid():
            self.right_memory.append((token.data, token.context))
        else:
            with suppress(ValueError):
                self.right_memory.remove((token.data, token.context))

        for left_data, left_context in self.left_memory:
            match = self.matcher(left_context, token.context)
            if match:
                if not isinstance(match, Mapping):
                    match = {}

                match.update(token.context)
                match.update(left_context)
                newtoken = Token(token.tag,
                                 left_data | token.data,
                                 match)
                for child in self.children:
                    child.callback(newtoken)
