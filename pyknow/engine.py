from pyknow import DynamicFact


class DuplicatedFactError(ValueError):
    pass


class KnowledgeEngine:
    def __init__(self):
        self._facts = dict()

    def asrt(self, name, value):
        if name in self._facts or hasattr(self, name):
            raise DuplicatedFactError('Fact %s exists already.' % name)

        self._facts[name] = value

    def __getitem__(self, name):
        if hasattr(self, name):
            is_asserted, fn = getattr(self, name)()
            if is_asserted:
                return fn()
            else:
                raise KeyError()
        elif name in self._facts:
            return self._facts[name]
        else:
            raise KeyError()

    def __contains__(self, name):
        try:
            self[name]
        except KeyError:
            return False
        else:
            return True
