from collections import deque


class Agenda:
    def __init__(self):
        self.activations = deque()
        self.executed = set()

    def get_next(self):
        try:
            act = self.activations.popleft()
            self.executed.add(act)
            return act
        except IndexError:
            return None

    def remove_from_fact(self, fact):
        """
        Remove a matching activation
        """
        activations_to_remove = []
        for activation in self.activations:
            if activation.facts == (fact,):
                activations_to_remove.append(activation)
        for activation in activations_to_remove:
            self.activations.remove(activation)
