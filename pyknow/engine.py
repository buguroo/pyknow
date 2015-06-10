from pyknow.factlist import FactList


class KnowledgeEngine:

    def __init__(self):
        self._facts = FactList()

    def declare(self, *facts):
        for fact in facts:
            idx = self._facts.declare(fact)
        return idx

    def retract(self, idx):
        self._facts.retract(idx)
