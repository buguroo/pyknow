import enum


class FactState(enum.Enum):
    DEFINED = 'DEFINED'
    UNDEFINED = 'UNDEFINED'


class FactType:
    def __init__(self, value):
        self.value = value

    def resolve(self):
        return self.value


class L(FactType):
    pass


class Fact:
    def __init__(self, **value):
        def resolve(set_):
            return {(a, b.resolve()) for a, b in set_}
        self.value = value
        for a in value.values():
            if not isinstance(a, FactType):
                raise TypeError("Fact values inherit from FactType")
        self.valueset = set((k, v)
                            for k, v in value.items()
                            if v.value not in FactState)
        self.wcvalueset = set((k, v)
                              for k, v in value.items()
                              if v.value in FactState)

        self.resolved_valueset = resolve(self.valueset)
        self.resolved_wcvalueset = resolve(self.wcvalueset)
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
            for k, v in self.resolved_wcvalueset:
                if v is FactState.DEFINED and k not in other.keyset:
                    return False
                elif v is FactState.UNDEFINED and k in other.keyset:
                    return False
                keys_to_skip.add(k)

            for k, v in self.resolved_valueset:
                if k in keys_to_skip:
                    continue
                else:
                    if not (k, v) in self.resolved_valueset:
                        return False
            return True
        else:
            return self.resolved_valueset.issuperset(other.resolved_valueset)

    def __eq__(self, other):
        return self.value == other.value


class InitialFact(Fact):
    pass
