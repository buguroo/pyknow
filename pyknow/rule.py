#!/usr/bin/env python
"""

Definitions of clips' Conditional Elements, except
``Pattern Conditional Element``.

``Pattern CE`` defines direct matching against patterns, wich is a special
case implemented in :mod:`pyknow.fact`.

"""

from functools import update_wrapper
from pyknow.fact import InitialFact
from pyknow.watchers import RULE_WATCHER


class Rule:
    """
    Base ``CE``, all ``CE`` are to derive from this class.

    This class is used as a decorator, thus provoking __call__
    to be called twice:

    #. The first call is when the decorator is been created. At this
       point we assign the function decorated to ``self.__fn`` and
       return ``self`` to be called the second time.

    #. The second call is to execute the decorated function, se we
       pass all the arguments along.
    """

    def __init__(self, *conds, salience=0):
        if not conds:
            conds = (InitialFact(),)
        self.__fn = None
        self._conds = conds
        self._curr = 0
        self.salience = salience
        RULE_WATCHER.debug("Initialized rule with conds %s", conds)

    def __iter__(self):
        return self

    def __next__(self):
        self._curr += 1
        try:
            return self._conds[self._curr - 1]
        except IndexError:
            raise StopIteration()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self._conds)

    def __call__(self, fst=None, *args, **kwargs):
        """
        Make method checks if it's the first call, and update wrapper.
        Othersise execute the RHS.
        """
        if self.__fn is None and fst is None:
            raise AttributeError("Mandatory function not provided.")

        if self.__fn is None and fst is not None:
            self.__fn = fst
            return update_wrapper(self, self.__fn)

        if 'activation' in kwargs:
            activation = kwargs.pop('activation')
            RULE_WATCHER.debug("Executing %s for rule %s, activation %s",
                               self.__fn.__name__, self, activation)
            if activation.context:
                kwargs.update(activation.context)

        return self.__fn(*tuple(obj for obj in (fst,) if obj) + args, **kwargs)

    def __eq__(self, other):
        return self._conds == other._conds


class AND(Rule):
    """
    ``AND CE``
    ----------

    See (:ref:`conditional_and`) narrative documentation.
    """
    pass


class OR(Rule):
    """
    ``Or CE``
    ---------
    See (:ref:`conditional_or`) narrative documentation
    """
    pass


class NOT(Rule):
    """
    ``NOT CE``
    ----------
    See (:ref:`conditional_not`) narrative documentation
    """
    pass
