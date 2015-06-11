from inspect import getmembers

from pyknow.agenda import Agenda
from pyknow.factlist import FactList
from pyknow.rule import Rule
from pyknow.strategies import Depth


class KnowledgeEngine:

    __strategy__ = Depth

    def __init__(self):
        self._facts = FactList()
        self.agenda = Agenda()
        self.strategy = self.__strategy__()

    def declare(self, *facts):
        for fact in facts:
            idx = self._facts.declare(fact)
        return idx

    def retract(self, idx):
        self._facts.retract(idx)

    def get_rules(self):
        def _rules():
            for name, obj in getmembers(self):
                if isinstance(obj, Rule):
                    yield obj
        return list(_rules())

    def get_activations(self):
        def _activations():
            for rule in self.get_rules():
                for act in rule.get_activations(self._facts):
                    yield act
        return list(_activations())
