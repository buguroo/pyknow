from collections import OrderedDict
from pyknow.fact import Fact
from pyknow.watchers import FACT_WATCHER


class FactList:
    """
    Contains a list of facts.

    Handles if a fact matches against the list of facts,
    their declaration and retracting

    """
    def __init__(self):
        self._facts = OrderedDict()
        self._fidx = 0

    def declare(self, fact):
        """
        Assert (in clips terminology) a fact.

        Insert the fact into `_facts` using `self._fidx` as the index.
        `self.fidx` should be the last fact inserted's id.

        Reject any object that not descend from the Fact class.

        :params fact: The fact to declare.
        :returns: (int) The index of the fact in the list.
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
        Retract a previous asserted fact.

        :params idx: The index of the fact to retract in the factlist

        """
        if idx not in self._facts:
            raise IndexError('Fact not found.')
        else:
            FACT_WATCHER.debug("Retracted fact %s", idx)
            del self._facts[idx]
        return idx

    def retract_matching(self, fact):
        """
            Retract all (exact) matching facts

            Iterates through the factlist looking for matches
            and calls `self.retract` for each one.

            :returns: list of idxs of the facts retracted

        """
        facts = []
        for idx, value in self._facts.items():
            if fact == value:
                facts.append(idx)
                self.retract(idx)

        if facts:
            return facts

        raise ValueError("No matching fact")

    def matches(self, fact):
        """
        Return the indexes of the matching facts.

        """

        def _matches():
            for idx, value in self._facts.items():
                if value in fact:
                    FACT_WATCHER.debug("Match found for %s on %s", value, fact)
                    yield idx
        result = list(_matches())
        return result
