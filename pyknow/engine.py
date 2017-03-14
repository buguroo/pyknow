"""
``pyknow engine`` represents ``CLIPS modules``

"""

from inspect import getmembers
import logging

from pyknow import abstract

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact
from pyknow.factlist import FactList
from pyknow.rule import Rule

from pyknow.strategies import DepthStrategy
from pyknow.rete import ReteMatcher

logging.basicConfig()


class KnowledgeEngine:
    """
    This represents a clips' ``module``, wich is an ``inference engine``
    holding a set of ``rules`` (as :obj:`pyknow.rule.Rule` objects),
    an ``agenda`` (as :obj:`pyknow.agenda.Agenda` object)
    and a ``fact-list`` (as :obj:`pyknow.factlist.FactList` objects)

    This could be considered, when inherited from, as the
    ``knowlege-base``.
    """
    from pyknow.matchers import ReteMatcher as __matcher__
    from pyknow.strategies import DepthStrategy as __strategy__

    def __init__(self):
        self._fixed_facts = []
        self.running = False
        self.facts = FactList()
        self.agenda = Agenda()

        if not isinstance(self.__matcher__, abstract.Matcher):
            raise TypeError("__matcher__ must be a subclass of Matcher")
        else:
            self.matcher = self.__matcher__(self)

        if not isinstance(self.__strategy__, abstract.Strategy):
            raise TypeError("__strategy__ must be a subclass of Strategy")
        else:
            self.strategy = self.__strategy__()

    def deffacts(self, *facts):
        """
        Declare a Fact from OUTSIDE the engine.
        Equivalent to clips' deffacts.
        """

        if self.running:
            logging.warning("Declaring fixed facts while run()")

        self._fixed_facts.extend(facts)

    def load_initial_facts(self):
        """
        Declares all fixed_facts
        """

        if self._fixed_facts:
            self.__declare(*self._fixed_facts)

    def modify(self, fact, result_fact):
        """
        Modifies a fact.
        Facts are inmutable in Clips, thus, as documented in clips reference
        manual, this retracts a fact and then re-declares it
        """

        self.retract_matching(fact)
        self.declare(result_fact)

    def get_rules(self):
        """
        When instanced as a knowledge-base, this will return
        each of the rules that are assigned to it (the rule-base).
        """

        def _rules():
            for _, obj in getmembers(self):
                if isinstance(obj, Rule):
                    obj.ke = self
                    yield obj
        return list(_rules())

    def get_activations(self):
        """
        Return activations
        """
        return self.matcher.changes(*self.facts.changes)

    def retract(self, idx):
        """
        Retracts a specific fact, using its index

        .. note::
            This updates the agenda
        """

        idx = self.facts.retract(idx)
        self.agenda.remove_from_fact(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

    def retract_matching(self, fact):
        """
        Retracts a specific fact, comparing against another fact

        .. note::
            This updates the agenda
        """

        for idx in self.facts.retract_matching(fact):
            self.agenda.remove_from_fact(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

    def run(self, steps=None):
        """
        Execute agenda activations
        """

        self.running = True
        while steps is None or steps > 0:
            activation = self.agenda.get_next()
            if activation is None:
                break
            else:
                if steps is not None:
                    steps -= 1
                activation.rule(self, activation=activation)
        self.running = False

    def reset(self):
        """
        Performs a reset as per CLIPS behaviour (resets the
        agenda and factlist and declares InitialFact())

        .. note:: If persistent facts have been added, they'll be
                  re-declared.
        """

        self.agenda = Agenda()
        self.facts = FactList()
        self.__declare(InitialFact())
        self.load_initial_facts()
        activations = self.get_activations()
        self.strategy.update_agenda(self.agenda, activations)

    def __declare(self, *facts):
        """
        Internal declaration method. Used for ``declare`` and ``deffacts``
        """

        return [self.facts.declare(fact) for fact in facts]

    def declare(self, *facts):
        """
        Declare from inside a fact, equivalent to ``assert`` in clips.

        .. note::

            This updates the agenda.
        """

        if not self.running:
            logging.warning("Declaring fact while not run()")
        self.__declare(*facts)
        activations = self.get_activations()
        self.strategy.update_agenda(self.agenda, activations)
