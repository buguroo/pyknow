from pyknow.factlist import FactList
from pyknow.agenda import Agenda
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
