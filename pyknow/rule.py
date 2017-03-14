#!/usr/bin/env python
"""
Definitions of clips' Conditional Elements, except ``Pattern Conditional
Element``.

``Pattern CE`` defines direct matching against patterns, wich is a
special case implemented in :mod:`pyknow.fact`.

"""
from collections.abc import Callable
from functools import update_wrapper

from pyknow.watchers import RULE_WATCHER


class ConditionalElement(tuple):
    """Base Conditional Element"""

    def __new__(cls, *args):
        return super(ConditionalElement, cls).__new__(cls, args)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, super().__repr__())


class Rule(ConditionalElement):
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

    def __new__(cls, *args, salience=0):
        obj = super(Rule, cls).__new__(cls, *args)

        obj.__fn = None
        obj.salience = salience

        RULE_WATCHER.debug("Initialized rule : %r", obj)

        return obj

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
        else:
            RULE_WATCHER.debug("Executing %s for rule %s, with context %s",
                               self.__fn.__name__, self, kwargs)

            return self.__fn(self, **kwargs)


class AND(ConditionalElement):
    """
    ``AND CE``
    ----------

    See (:ref:`conditional_and`) narrative documentation.
    """

    pass


class OR(ConditionalElement):
    """
    ``Or CE``
    ---------
    See (:ref:`conditional_or`) narrative documentation
    """

    pass


class NOT(ConditionalElement):
    """
    ``NOT CE``
    ----------
    See (:ref:`conditional_not`) narrative documentation
    """

    pass


class PatternConditionalElement(ConditionalElement):
    def __and__(self, other):
        return ANDPCE(self, other)

    def __or__(self, other):
        return ORPCE(self, other)

    def __invert__(self):
        return NOTPCE(self)


class ANDPCE(PatternConditionalElement):
    pass


class ORPCE(PatternConditionalElement):
    pass


class NOTPCE(PatternConditionalElement):
    pass


class LiteralPCE(PatternConditionalElement):
    def __new__(cls, *args):
        if len(args) != 1:
            raise ValueError("LiteralPCE must contain only one element.")
        else:
            return super(LiteralPCE, cls).__new__(cls, *args)

    def __repr__(self):
        return repr(self[0])


class WildcardPCE(PatternConditionalElement):
    def __new__(cls, *args, bind_to=None):
        if len(args) != 0:
            raise ValueError("WildcardPCE cannot contain any element.")
        else:
            obj = super(WildcardPCE, cls).__new__(cls, *args)
            obj.bind_to = bind_to
            return obj


class PredicatePCE(PatternConditionalElement):
    def __new__(cls, *args, bind_to=None):
        if len(args) != 1:
            raise ValueError("PredicatePCE must contain only one element.")
        elif not isinstance(args[0], Callable):
            raise TypeError("PredicatePCE needs a callable.")
        else:
            obj = super(PredicatePCE, cls).__new__(cls, *args)
            obj.bind_to = bind_to
            return obj
