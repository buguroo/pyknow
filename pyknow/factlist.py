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
from pyknow.watchers import FACT_WATCHER


class FactList:
    """
    Contains a list of facts (``asserted`` data).

    In clips, there is the concept of "modules"
    (:obj:`pyknow.engine.KnowledgeEngine`), wich have their own
    :obj:`pyknow.factlist.FactList` and :obj:`pyknow.agenda.Agenda`

    A factlist acts as both the module's factlist and a ``fact-set``
    yet currently most methods from a ``fact-set`` are not yet
    implemented

    .. TODO:: Implement remaining ``fact-set`` methods

    """
    def __init__(self):
        self._facts = OrderedDict()
        self._fidx = 0

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

        if fact not in self._facts.values():
            idx = self._fidx
            self._facts[idx] = fact
            self._fidx += 1
            FACT_WATCHER.debug("Declared fact: %s", fact)
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
        if idx not in self._facts:
            raise IndexError('Fact not found.')
        else:
            FACT_WATCHER.debug("Retracted fact %s", idx)
            del self._facts[idx]
        return idx

    def retract_matching(self, fact):
        """
        Retract all matching facts

        Iterates through the factlist looking for matches
        against a given fact and calls
        :func:`pyknow.factlist.FactList.retract` for each match.

        :return: list of indexes of the facts retracted
        :throws ValueError: If no fact matches in the factlist

        """
        facts = []
        for idx, value in self._facts.items():
            if fact == value:
                facts.append(idx)

        if facts:
            for fact in facts:
                self.retract(fact)
            return facts

        raise ValueError("No matching fact")

    def matches(self, fact):
        """
        Checks for matches of a fact inside this factlist

        :param fact: :obj:`pyknow.fact.Fact` to match against
        :return: list of indexes of matching facts

        """

        def _matches():
            for idx, value in self._facts.items():
                if value in fact:
                    FACT_WATCHER.debug("Match found for %s on %s", value, fact)
                    yield idx
        result = list(_matches())
        return result

    def get_by_idx(self, idx):
        """
        Return a fact by its position in the fact list

        """
        return self._facts[idx]

    def __repr__(self):
        return str(self._facts.values())
