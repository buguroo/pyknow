from collections.abc import Iterable
from functools import update_wrapper

from pyknow import watchers
from pyknow.conditionalelement import ConditionalElement


class Rule(ConditionalElement):
    """
    Base ``CE``, all ``CE`` are to derive from this class.

    This class is used as a decorator, thus provoking __call__
    to be called twice:

    #. The first call is when the decorator is been created. At this
       point we assign the function decorated to ``self._wrapped`` and
       return ``self`` to be called the second time.

    #. The second call is to execute the decorated function, se we
       pass all the arguments along.
    """

    def __new__(cls, *args, salience=0):
        obj = super(Rule, cls).__new__(cls, *args)

        obj._wrapped = None
        obj._wrapped_self = None
        obj.salience = salience

        return obj

    def new_conditions(self, *args):
        """
        Generate a new rule with the same attributes but with the given
        conditions.

        """
        obj = self.__class__(*args, salience=self.salience)

        if self._wrapped:
            obj = obj(self._wrapped)

        return obj

    def __hash__(self):
        return hash(tuple(self)
                    + (self._wrapped, self._wrapped_self, self.salience))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            self_data = tuple(self) + (self._wrapped,
                                       self._wrapped_self,
                                       self.salience)
            other_data = tuple(other) + (other._wrapped,
                                         other._wrapped_self,
                                         other.salience)
            return self_data == other_data
        else:
            return False

    def __call__(self, *args, **kwargs):
        """
        Make method checks if it's the first call, and update wrapper.
        Othersise execute the RHS.
        """
        if self._wrapped is None:
            if not args:
                raise AttributeError("Mandatory function not provided.")
            else:
                self._wrapped = args[0]
                return update_wrapper(self, self._wrapped)
        elif self._wrapped_self is None:
            return self._wrapped(*args, **kwargs)
        else:
            return self._wrapped(self._wrapped_self, *args, **kwargs)

    def __repr__(self):
        return "%s => %r" % (super().__repr__(), self._wrapped)

    def __get__(self, instance, owner):
        self._wrapped_self = instance
        return self
