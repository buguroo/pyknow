"""
    Knowledge Engine
    ----------------

    TODO: Document the knowledge engine and examples
"""
from inspect import getmembers

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact, Context
from pyknow.factlist import FactList
from pyknow.rule import Rule
from pyknow.strategies import Depth


class KnowledgeEngine:
    """
        Base knowledge engine.
    """

    __strategy__ = Depth

    def __init__(self):
        self.context = Context()
        self._fixed_facts = []
        self._facts = FactList()
        self.agenda = Agenda()
        self.strategy = self.__strategy__()

    def declare(self, *facts, persistent=False):
        """
            Declare a Fact in the KE.

            If persistent is specified, the facts will be there
            even after a reset() has been performed, as with
            clips' initialfacts

            .. note::

                This updates the agenda.

        """
        for fact in facts:
            if fact.is_matcher:
                raise TypeError("Cant use types T, C, V declaring a fact")
            idx = self._facts.declare(fact)
            self.strategy.update_agenda(self.agenda, self.get_activations())

        if persistent:
            self._fixed_facts.extend(facts)
        return idx

    def retract(self, idx):
        """
            Retracts a specific fact, using index

            .. note::

                This updates the agenda
        """
        self._facts.retract(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

    def retract_matching(self, fact):
        """
            Retracts a specific fact, comparing against another fact

            .. note::

                This updates the agenda
        """
        self._facts.retract_matching(fact)
        self.strategy.update_agenda(self.agenda, self.get_activations())

    def get_rules(self):
        """
            Gets all rules assigned to this KE.
        """
        def _rules():
            for name, obj in getmembers(self):
                if isinstance(obj, Rule):
                    obj.ke = self
                    yield obj
        return list(_rules())

    def get_activations(self):
        """
            Return a list of activations for every rule / fact.
        """
        def _activations():
            for rule in self.get_rules():
                rule.ke = self
                for act in rule.get_activations(self._facts):
                    yield act
        return list(_activations())

    def run(self, steps=None):
        """
            Execute agenda activations
        """
        while steps is None or steps > 0:
            activation = self.agenda.get_next()
            if activation is None:
                break
            else:
                if steps is not None:
                    steps -= 1
                activation.rule(self)

    def reload_initial_facts(self):
        """
            Loads InitialFact and all the persistent declared facts
        """
        self.declare(InitialFact())
        if self._fixed_facts:
            self.declare(*self._fixed_facts)

    def reset(self):
        """
            Perform a reset, resets the agenda and factlist
            If persistent facts have been added, they'll be
            repopulated after.
        """
        self.agenda = Agenda()
        self._facts = FactList()
        self.reload_initial_facts()
