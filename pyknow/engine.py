"""
``pyknow engine`` represents ``CLIPS modules``

"""

from inspect import getmembers
import logging
import warnings

from pyknow import abstract

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact
from pyknow.factlist import FactList
from pyknow.rule import Rule, ConditionalElement
from pyknow import watchers

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

        if not issubclass(self.__matcher__, abstract.Matcher):
            raise TypeError("__matcher__ must be a subclass of Matcher")
        else:
            self.matcher = self.__matcher__(self)

        if not issubclass(self.__strategy__, abstract.Strategy):
            raise TypeError("__strategy__ must be a subclass of Strategy")
        else:
            self.strategy = self.__strategy__()

    def deffacts(self, *facts):
        """
        Declare a Fact from OUTSIDE the engine.
        Equivalent to clips' deffacts.
        """

        if self.running:
            warnings.warn("Declaring fixed facts while run()")

        self._fixed_facts.extend(facts)

    def load_initial_facts(self):
        """
        Declares all fixed_facts
        """

        if self._fixed_facts:
            self.__declare(*self._fixed_facts)

    def modify(self, declared_fact, **modifiers):
        """

        Modifies a fact.

        Facts are inmutable in Clips, thus, as documented in clips
        reference manual, this retracts a fact and then re-declares it

        `modifiers` must be a Mapping object containing keys and values
        to be changed.

        """

        self.retract(declared_fact)

        newfact = declared_fact.copy()
        newfact.update(modifiers)
        self.declare(newfact)

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

    def __retract(self, idx):
        idx = self.facts.retract(idx)
        self.agenda.remove_from_fact(idx)
        if not self.running:
            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

    def retract(self, declared_fact):
        """
        Retracts a specific fact, using its index

        .. note::
            This updates the agenda
        """
        self.__retract(declared_fact['__factid__'])

    def run(self, steps=float('inf')):
        """
        Execute agenda activations
        """

        self.running = True
        activation = None
        execution = 0
        while steps > 0 and self.running:

            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

            for idx, act in enumerate(self.agenda.activations):
                watchers.AGENDA.debug(
                    "%d: %r %r",
                    idx,
                    act.rule.__name__,
                    ", ".join(str(f) for f in act.facts))

            activation = self.agenda.get_next()

            if activation is None:
                break
            else:
                steps -= 1
                execution += 1

                watchers.RULES.info(
                    "FIRE %s %s: %s",
                    execution,
                    activation.rule.__name__,
                    ", ".join(str(f) for f in activation.facts))

                activation.rule(
                    self,
                    **{k: v
                       for k, v in activation.context.items()
                       if not k.startswith('__')})

        self.running = False

    def halt(self):
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
        self.matcher.reset()
        self.__declare(InitialFact())
        self.load_initial_facts()
        self.running = False

    def __declare(self, *facts):
        """
        Internal declaration method. Used for ``declare`` and ``deffacts``
        """
        for fact in facts:
            if any(isinstance(v, ConditionalElement) for v in fact.values()):
                raise TypeError(
                    "Declared facts cannot contain conditional elements")
            else:
                self.facts.declare(fact)

        if not self.running:
            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

    def declare(self, *facts):
        """
        Declare from inside a fact, equivalent to ``assert`` in clips.

        .. note::

            This updates the agenda.
        """

        if not self.running:
            warnings.warn("Declaring fact while not run()")
        self.__declare(*facts)
