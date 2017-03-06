from collections import namedtuple
from collections.abc import Callable, Mapping
from contextlib import suppress

from .abstract import AbstractNode, OneInputNode, TwoInputNode
from .token import Token
from pyknow.rule import Rule

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

    def _activation(self, token, branch_memory, matching_memory):
        if token.is_valid():
            branch_memory.append((token.data, token.context))
        else:
            with suppress(ValueError):
                branch_memory.remove((token.data, token.context))

        for other_data, other_context in matching_memory:
            match = self.matcher(token.context, other_context)

            if match:
                if not isinstance(match, Mapping):
                    match = {}

                match.update(token.context)
                match.update(other_context)
                newtoken = Token(token.tag,
                                 token.data | other_data,
                                 match)
                for child in self.children:
                    child.callback(newtoken)

    def _activate_left(self, token):
        self._activation(token, self.left_memory, self.right_memory)

    def _activate_right(self, token):
        self._activation(token, self.right_memory, self.left_memory)


class ConflictSetNode(AnyChild, OneInputNode):
    def __init__(self, rule):
        try:
            assert isinstance(rule, Rule)
        except AssertionError as exc:
            raise TypeError(exc) from exc
        else:
            self.rule = rule

        self.memory = []

        super().__init__()

    def _activate(self, token):
        if token.is_valid():
            self.memory.append((token.data, token.context))
        else:
            with suppress(ValueError):
                self.memory.remove((token.data, token.context))
