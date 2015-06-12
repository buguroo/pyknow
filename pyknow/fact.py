class Fact:
    def __init__(self, **value):
        self.value = value 
        self.valueset = set(value.items())
        self.keyset = set(value.keys())

    def __contains__(self, other):
        """Does this Fact contain ``other``?."""
        if self.__class__ != other.__class__:
            return False
        elif not self.value:
            return True
        else:
            return self.valueset.issuperset(other.valueset)

    def __eq__(self, other):
        return self.value == other.value


class InitialFact(Fact):
    pass
