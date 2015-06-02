from pyknow import DynamicFact
from collections import OrderedDict


class DuplicatedFactError(ValueError):
    pass


class InmutableFactError(ValueError):
    pass


class KnowledgeEngine:
    def __init__(self):
        self._facts = dict()
        self.agenda = OrderedDict()
        self.running = False

    def asrt(self, name, value):
        if name in self._facts or hasattr(self, name):
            raise DuplicatedFactError('Fact %s exists already.' % name)

        self._facts[name] = value

    def retract(self, name):
        if name in self._facts:
            del self._facts[name]
        elif hasattr(self, name):
            raise InmutableFactError('Cannot retract fact %s' % name)

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

    def run(self):
        self.running = True

    def reset(self):
        self.running = False
        self.agenda = OrderedDict()
        self._facts = dict()
