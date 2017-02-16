"""
``pyknow engine`` represents ``CLIPS modules``

"""
from inspect import getmembers

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact, Context, L
from pyknow.factlist import FactList
from pyknow.rule import Rule
from pyknow.strategies import Depth
from pyknow.watchers import FACT_WATCHER


class KnowledgeEngine:
    """
        This represents a clips' ``module``, wich is an ``inference engine``
        holding a set of ``rules`` (as :obj:`pyknow.rule.Rule` objects),
        an ``agenda`` (as :obj:`pyknow.agenda.Agenda` object)
        and a ``fact-list`` (as :obj:`pyknow.factlist.FactList` objects)

        This could be considered, when inherited from, as the
        ``knowlege-base``.

    """

    __strategy__ = Depth

    def __init__(self):
        self.context = Context()
        self._fixed_facts = []
        self._facts = FactList()
        self.agenda = Agenda()
        self.strategy = self.__strategy__()
        self._parent = False
        self.shared_attributes = {}

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.shared_attributes)

    def set_shared_attributes(self, **shared_attributes):
        """
        Stablises a dict with shared attributes to be used
        by this KE's childs on a tree

        """
        self.shared_attributes.update(shared_attributes)

    @property
    def parent(self):
        """
        Parent KE

        Note: This feels like it SHOULD return an exception, but since
        we're iterating over properties in Rules, I cannot
        make an unset property return an exception upon accessing.
        Also, that does not sound like a good idea

        :return: KnowledgeEngine

        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Set a parent for later use.

        You can use any class as a parent as long as it's compatible with
        KnowledgeEngine class

        We're not currently forcing this, it's a norm

        """
        self._parent = parent

    def declare_from_fact(self, *facts):
        """
        Declare from inside a fact, that is a non-persistent fact.
        """
        self.declare(*facts, persistent=True)

    def declare(self, *facts, persistent=True):
        """
        Declare a Fact in the KE.

        If persistent is specified, the facts will be there
        even after a reset() has been performed, as with
        clips' initialfacts

        .. note::

            This updates the agenda.

        """
        ids = []

        for fact in facts:
            FACT_WATCHER.debug("Declaring fact %s", self)
            for value in fact.value.values():
                if not isinstance(value, L):
                    raise TypeError("Cant use types T, C, V declaring a fact")
            idx = self._facts.declare(fact)
            ids.append(idx)

        if persistent:
            self._fixed_facts.extend(facts)
        return ids

    def retract(self, idx):
        """
        Retracts a specific fact, using index

        .. note::
            This updates the agenda

        """
        idx = self._facts.retract(idx)
        self.agenda.remove_from_fact(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

    def retract_matching(self, fact):
        """
        Retracts a specific fact, comparing against another fact

        .. note::
            This updates the agenda

        """
        for idx in self._facts.retract_matching(fact):
            self.agenda.remove_from_fact(idx)
        self.strategy.update_agenda(self.agenda, self.get_activations())

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
        Matches the rule-base (see :func:`pyknow.engine.get_rules`)
        with the fact-list and returns each match

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
                activation.rule(self, activation=activation)

    def load_initial_facts(self):
        """
        Declares all fixed_facts

        """
        if self._fixed_facts:
            self.declare(*self._fixed_facts)

    def reset(self):
        """
        Performs a reset as per CLIPS behaviour (resets the
        agenda and factlist and declares InitialFact())

        .. note:: If persistent facts have been added, they'll be
                  re-declared.

        """
        self.agenda = Agenda()
        self._facts = FactList()
        self.declare(InitialFact())
        self.load_initial_facts()
        self.strategy.update_agenda(self.agenda, self.get_activations())
