#!/usr/bin/env python
"""

Definitions of clips' Conditional Elements, except
``Pattern Conditional Element``.

``Pattern CE`` defines direct matching against patterns, wich is a special
case implemented in :mod:`pyknow.fact`.

"""

from functools import update_wrapper
from itertools import chain, product

from pyknow.fact import InitialFact
from pyknow.factlist import FactList
from pyknow.activation import Activation
from pyknow.watchers import RULE_WATCHER
from pyknow.match import Capturation


def sum_objs(objs):
    """
    Sum objects. This is done like this for if not, sum() by default uses
    '0' as start, thus tries to sum whatever with provide with zero.
    """

    first_obj = next(objs, None)
    if first_obj is not None:
        return sum(objs, first_obj)


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
        self.salience = salience
        RULE_WATCHER.debug("Initialized rule with conds %s", conds)

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
            RULE_WATCHER.debug("Executing rule %s for activation %s",
                               self, activation)

        return self.__fn(*tuple(obj for obj in (fst,) if obj) + args, **kwargs)

    def get_activations(self, factlist, capturations=Capturation()):
        """
        For this :obj:`pyknow.rule.Rule`, returns all the
        :obj:`pyknow.activation.Activation`, for the provided factlist.

        :param factlist: :obj:`pyknow.factlist.FactList` to match against.
        :return: Tuple of unique :obj:`pyknow.activation.Activation` matches.
        """

        if not isinstance(factlist, FactList):
            raise ValueError("Factlist must be a factlist instance")

        def _all_activations():
            """
            Tengo un problema aqui al sacar las activaciones.
            El InitialFact tambien matchea y entra dentro del product(),
            entonces acabo con una activación con el initialfact y otra
            sin el en el caso de los or
            """
            for cond in self._conds:
                yield (a for a in cond.get_activations(factlist, capturations))

        return (sum_objs(iter(a)) for a in product(*_all_activations()))

    def get_capturations(self, factlist):
        """
        Return captured values with its facts from all our children
        """
        capturations = Capturation()
        for cond in self._conds:
            for capturation in cond.get_capturations(factlist):
                capturations += capturation
        return capturations


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

    def get_activations(self, factlist, capturations):
        activations = (cond.get_activations(factlist, capturations)
                       for cond in self._conds)
        return iter(set(chain(*activations)))


class NOT(Rule):
    """
    ``NOT CE``
    ----------
    See (:ref:`conditional_not`) narrative documentation
    """
    def get_activations(self, factlist, capturations):
        if next(super().get_activations(factlist, capturations), None) is None:
            if factlist.facts:
                yield Activation(rule=None, facts=(0,))
