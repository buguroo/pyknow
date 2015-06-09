from collections import OrderedDict
from pyknow.fact import Fact


class FactList:
    def __init__(self):
        self._facts = OrderedDict()
        self._fidx = 0

    def declare(self, fact):
        """
        Assert a fact.

        Insert the fact into `_facts` using `_fidx` as the index.
        Reject any object that not descend from the Fact class.

        :params fact: The fact to declare.
        :returns: (int) The index of the fact in the list.

        """
        if not isinstance(fact, Fact):
            raise ValueError('The fact must descend the Fact class.')

        if fact not in self._facts.values():
            idx = self._fidx
            self._facts[idx] = fact
            self._fidx += 1
    
            return idx
        else:
            return None

    def retract(self, idx):
        """
        Retract a previous asserted fact.

        :params idx: The index of the fact to retract.

        """
        if not idx in self._facts:
            raise IndexError('Fact not found.')
        else:
            del self._facts[idx]
