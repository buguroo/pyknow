import enum


class FactState(enum.Enum):
    DEFINED = 'DEFINED'
    UNDEFINED = 'UNDEFINED'


class Fact:
    def __init__(self, **value):
        self.value = value 
        self.valueset = set((k, v)
                            for k, v in value.items()
                            if v not in FactState)
        self.wcvalueset = set((k, v)
                            for k, v in value.items()
                            if v in FactState)
        self.keyset = set(value.keys())

    def __contains__(self, other):
        """Does this Fact contain ``other``?."""
        if self.__class__ != other.__class__:
            return False
        elif not self.value:
            return True
        elif self.wcvalueset:
            # We have some wildcards.
            keys_to_skip = set()
            for k, v in self.wcvalueset:
                if v is FactState.DEFINED and not k in other.keyset:
                        return False
                elif v is FactState.UNDEFINED and k in other.keyset:
                        return False
                keys_to_skip.add(k)
            for k, v in self.valueset:
                if k in keys_to_skip:
                    continue
                else:
                    if not (k, v) in other.valueset:
                        return False
            return True
        else:
            return self.valueset.issuperset(other.valueset)

    def __eq__(self, other):
        return self.value == other.value


class InitialFact(Fact):
    pass
