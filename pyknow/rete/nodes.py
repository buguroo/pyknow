from collections import namedtuple
from collections.abc import Callable, Mapping
from contextlib import suppress

from .abstract import AbstractNode, OneInputNode, TwoInputNode
from .token import Token
from pyknow.rule import Rule
from pyknow.activation import Activation

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
                for key, value in match.items():
                    if token.context.get(key, value) != value:
                        return False
                token.context.update(match)
            for child in self.children:
                child.callback(token)


class OrdinaryMatchNode(AnyChild, HaveMatcher, TwoInputNode):
    def __init__(self, *args, **kwargs):
        self.left_memory = list()
        self.right_memory = list()
        super().__init__(*args, **kwargs)

    def _activation(self, token, branch_memory, matching_memory):
        if token.is_valid():
            branch_memory.append(token.to_info())
        else:
            with suppress(ValueError):
                branch_memory.remove(token.to_info())

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
            self.memory.append(token.to_info())
        else:
            with suppress(ValueError):
                self.memory.remove(token.to_info())

    def get_activations(self):
        return [Activation(self.rule,
                           tuple(info.data),
                           dict(info.context))
                for info in self.memory]


class NotNode(AnyChild, HaveMatcher, TwoInputNode):
    def __init__(self, *args, **kwargs):
        self.left_memory = dict()
        self.right_memory = list()

        super().__init__(*args, **kwargs)

    def _activate_left(self, token):
        count = 0
        for right_data, right_context in self.right_memory:
            if self.matcher(token.context, right_context):
                count += 1
        if token.is_valid():
            self.left_memory[token.to_info()] = count
        if count == 0:
            for child in self.children:
                child.callback(token)

    def _activate_right(self, token):
        if token.is_valid():
            self.right_memory.append(token.to_info())
            inc = 1
        else:
            inc = -1

        for left in self.left_memory:
            if self.matcher(left.context, token.context):
                self.left_memory[left] += inc
                newcount = self.left_memory[left]
                if (newcount == 0 and inc == -1) or \
                        (newcount == 1 and inc == 1):
                    if inc == -1:
                        newtoken = left.to_valid_token()
                    else:
                        newtoken = left.to_invalid_token()
                    for child in self.children:
                        child.callback(newtoken)
