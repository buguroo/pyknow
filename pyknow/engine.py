from collections import OrderedDict
import inspect

from pyknow.strategies import Depth


class DuplicatedFactError(ValueError):
    pass


class InmutableFactError(ValueError):
    pass


class KnowledgeEngine:

    strategy = Depth()

    def __init__(self):
        self._facts = OrderedDict()
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

    def __setitem__(self, name, value):
        self.retract(name)
        self.asrt(name, value)

    def __contains__(self, name):
        try:
            self[name]
        except KeyError:
            return False
        else:
            return True

    def run(self, steps=None):
        self.running = True
        self.agenda = self.strategy.build_agenda(self)
        while self.agenda:
            _, fn = self.agenda.popitem()

            fn()

            self.agenda = self.strategy.build_agenda(self)

            if steps is not None:
                steps -= 1
                if steps == 0:
                    break


    def reset(self):
        self.running = False
        self.agenda = OrderedDict()
        self._facts = dict()

    def get_matching_rules(self):
        def _rules():
            for name, method in inspect.getmembers(self,
                                                   predicate=inspect.ismethod):
                if hasattr(method, 'is_rule') and method.is_rule:
                    match, fn = method(self)
                    if match:
                        yield (name, fn)

        return dict(_rules())
