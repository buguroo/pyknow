from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def build_agenda(self, facts):
        pass


class Depth(Strategy):
    def build_agenda(self, kengine, current_agenda=None):
        agenda = OrderedDict()

        matches = kengine.get_matching_rules()
        if matches:
            if current_agenda is None:
                current_agenda = kengine.agenda

            for name in current_agenda:
                if name in matches:
                    agenda[name] = matches[name]

            for name, fn in matches.items():
                if not name in agenda:
                    agenda[name] = fn

        return agenda
