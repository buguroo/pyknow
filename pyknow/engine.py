from inspect import getmembers

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact
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
        self.strategy.update_agenda(self.agenda, self.get_activations())
        return idx

    def retract(self, idx):
        self._facts.retract(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

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

    def run(self, steps=None):
        while steps is None or steps > 0:
            activation = self.agenda.get_next()
            if activation is None:
                break
            else:
                if steps is not None:
                    steps -= 1
                activation.rule(self)

    def reset(self):
        self.agenda = Agenda()
        self._facts = FactList()
        self.declare(InitialFact())
