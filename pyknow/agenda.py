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
