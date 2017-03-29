from functools import update_wrapper
import inspect


class DefFacts:
    def __new__(cls, order=0):
        obj = super(DefFacts, cls).__new__(cls)

        obj._wrapped = None
        obj._wrapped_self = None
        obj.order = order

        return obj

    def __repr__(self):
        return "DefFacts(%r)" % (self._wrapped)

    def __call__(self, *args, **kwargs):
        if args and self._wrapped is None:
            if inspect.isgeneratorfunction(args[0]):
                self._wrapped = args[0]
                return update_wrapper(self, self._wrapped)
            else:
                raise TypeError("DefFact can only decorate generators.")
        elif self._wrapped is not None:
            if self._wrapped_self is None:
                gen = self._wrapped(*args, **kwargs)
            else:
                gen = self._wrapped(self._wrapped_self, *args, **kwargs)
            return (x.copy() for x in gen)
        else:
            raise RuntimeError("Usage error.")

    def __get__(self, instance, owner):
        self._wrapped_self = instance
        return self
