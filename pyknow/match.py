"""
Matcheable metaclass, rule and fact must implement this.
"""


from itertools import chain


class Capturation(dict):
    """
    Relation between contexts and facts
    """
    def __add__(self, other):
        result = Capturation()
        for key in self.keys() | other.keys():
            result[key] = self.get(key, Context()) + other.get(key, Context())
        return result


class Context(dict):
    """
    Context for capturing values
    """
    def __setitem__(self, key, value):
        if key in self and value != self[key]:
            raise ValueError()
        return super().__setitem__(key, value)

    def __add__(self, other):
        return Context(**dict(chain(self.items(), other.items())))

    def __hash__(self):
        return hash(tuple(self.items()))
