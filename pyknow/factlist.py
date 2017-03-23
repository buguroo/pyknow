"""
``fact-list`` implementation from CLIPS.

See `Making a List <http://clipsrules.sourceforge.net/docume\
    ntation/v624/ug.htm#_Toc412126071>`_  section on the user guide. \
Also see `retrieving the fact-list \
  <http://clipsrules.sourceforge.net/d\
          ocumentation/v624/bpg.htm#_Toc11859921>`_ on the clips\
          programming manual
"""

from collections import OrderedDict
from pyknow.fact import Fact
from pyknow import watchers


class FactList:
    """
    Contains a list of facts (``asserted`` data).

    In clips, there is the concept of "modules"
    (:obj:`pyknow.engine.KnowledgeEngine`), wich have their own
    :obj:`pyknow.factlist.FactList` and :obj:`pyknow.agenda.Agenda`

    A factlist acts as both the module's factlist and a ``fact-set``
    yet currently most methods from a ``fact-set`` are not yet
    implemented
    """

    def __init__(self):
        self.facts = OrderedDict()
        self._ifacts = dict()
        self.last_read = OrderedDict()
        self._fidx = 0
        self.added = list()
        self.removed = list()

    def __repr__(self):
        return "\n".join(
            "{idx}: {fact}".format(idx=idx, fact=fact)
            for idx, fact in self.facts.items())

    def declare(self, fact):
        """
        Assert (in clips terminology) a fact.

        This keeps insertion order.

        .. warning:: This will reject any object that not descend
                     from the Fact class.

        :param fact: The fact to declare, **must** be derived from
                     :obj:`pyknow.fact.Fact`.
        :return: (int) The index of the fact in the list.
        :throws ValueError: If the fact providen is not a Fact object

        """

        if not isinstance(fact, Fact):
            raise ValueError('The fact must descend the Fact class.')

        if fact not in self.facts.values():
            idx = self._fidx
            fact['__factid__'] = idx
            self.facts[idx] = fact
            self._ifacts[fact] = idx
            self._fidx += 1
            self.added.append(fact)
            watchers.FACTS.debug("==> %s: %r", idx, fact)
            return idx
        else:
            return None

    def retract(self, idx):
        """
        Retract a previously asserted fact.

        See `"Retract that fact" in Clips User Guide
        <http://clipsrules.sourceforge.net/doc\
                umentation/v624/ug.htm#_Toc412126077>`_.

        :param idx: The index of the fact to retract in the factlist
        :return: (int) The retracted fact's index
        :throws IndexError: If the fact's index providen does not exist
        """

        if idx not in self.facts:
            raise IndexError('Fact not found.')

        fact = self.facts[idx]

        watchers.FACTS.debug("<== %s: %r", idx, fact)
        self.removed.append(fact)

        del self.facts[idx]
        del self._ifacts[fact]

        return idx

    def retract_matching(self, fact):
        """
        Retract all matching facts

        :return: list of indexes of the facts retracted
        :throws ValueError: If no fact matches in the factlist
        """

        def search_matching(model_fact):
            model_fact_set = set(model_fact.items())

            for fact in self.facts.values():
                this_fact_set = {(k, v)
                                 for k, v in fact.items()
                                 if k != '__factid__'}
                if model_fact_set == this_fact_set:
                    yield fact['__factid__'][0]

        retracted = [self.retract(f) for f in search_matching(fact)]
        if retracted:
            return retracted
        else:
            raise ValueError("No matching fact.")

    @property
    def changes(self):
        """
        Return a tuple with the removed and added facts since last run.
        """
        try:
            return self.added, self.removed
        finally:
            self.added = list()
            self.removed = list()

    def idx_from_fact(self, fact):
        return self._ifacts[fact]

    def indexes_from_facts(self, facts):
        for f in facts:
            if f in self._ifacts:
                yield self._ifacts[f]
