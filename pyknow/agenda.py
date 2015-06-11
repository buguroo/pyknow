from collections import deque


class Agenda:
    def __init__(self):
        self.activations = deque()

    def get_next(self):
        try:
            return self.activations.popleft()
        except IndexError:
            return None
