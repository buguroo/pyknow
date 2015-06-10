class Fact:
    def __init__(self, **value):
        self.value = value 
        self.valueset = set(value.items())
        self.keyset = set(value.keys())


class InitialFact(Fact):
    pass
