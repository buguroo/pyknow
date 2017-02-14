#!/usr/bin/env python
"""

Definitions of clips' Conditional Elements, except
``Pattern Conditional Element``.

``Pattern CE`` defines direct matching against patterns, wich is a special
case implemented in :mod:`pyknow.fact`.

"""

from functools import update_wrapper
from itertools import product

from pyknow.factlist import FactList
from pyknow.fact import InitialFact, Fact, Context, C
from pyknow.activation import Activation
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
           We also assign the KnowledgeEngine's context to the rule, if
           available and if we're being called from a KE.
           Otherwise, each rule will make their own Context() object, empty
           and not shared between rules, when they're being evaluated.

        .. note:: We can assign rules to variables and apply them directly
                  as well as using KEs

    """
    def __init__(self, *conds, salience=0):
        RULE_WATCHER.debug("Initialized rule with conds %s", conds)
        self.__fn = None
        self.ke = None

        if not conds:
            conds = (InitialFact(),)
        self.__conds = conds

        self.salience = salience

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__conds)

    @property
    def context(self):
        """
        Shared context between rule's facts.

        This is used to implement :obj:`pyknow.fact.C` and
        :obj:`pyknow.fact.V`

        """
        if self.ke:
            return self.ke.context
        else:
            return None

    def __call__(self, fst=None, *args, **kwargs):
        if 'activation' in kwargs:
            activation = kwargs.pop('activation')

        if self.__fn is None:
            if fst is not None:
                self.__fn = fst
                return update_wrapper(self, self.__fn)
            else:
                raise AttributeError("Mandatory function not provided.")
        else:
            if hasattr(fst, 'context') and isinstance(fst.context, Context):
                self.ke = fst

            def is_capturing_in_children(cond, name):
                """
                Check if we capture this value in any child.
                """
                for cond in cond.conds():
                    if isinstance(cond, Rule):
                        if is_capturing_in_children(cond, name):
                            return True
                    elif isinstance(cond.value.get(name, False), C):
                        return True
                return False

            def get_captured_facts():
                """ We expose as kwargs all captured facts. """
                if self.context is None:
                    return []

                for name, value in self.context.items():
                    if is_capturing_in_children(activation.rule, name):
                        yield name, value

            RULE_WATCHER.debug("Processing with context: %s", self.context)
            kwargs.update(dict(get_captured_facts()))
            args = (tuple() if fst is None else (fst,)) + args
            return self.__fn(*args, **kwargs)

    def get_activations(self, factlist):
        """
        For this :obj:`pyknow.rule.Rule`, returns all the
        :obj:`pyknow.activation.Activation`, for the provided factlist.

        :param factlist: :obj:`pyknow.factlist.FactList` to match against.
        :return: Tuple of unique :obj:`pyknow.activation.Activation` matches.

        """
        RULE_WATCHER.debug("Getting activations for %s on %s", self, factlist)

        if not isinstance(factlist, FactList):
            raise ValueError("factlist must be an instance of FactList")
        else:
            def _activations():
                matches = []

                for cond in self.__conds:
                    factlist.rule = self
                    if issubclass(cond.__class__, Rule):
                        cond.ke = self.ke
                        acts = cond.get_activations(factlist)
                        if not acts:
                            break
                        for act in acts:
                            for fact in act.facts:
                                matches.append([fact])
                    elif isinstance(cond, Fact):
                        cond.rule = self
                        match = factlist.matches(cond)
                        if match:
                            matches.append(match)
                        else:
                            break
                else:
                    for match in product(*matches):
                        facts = tuple(sorted(set(match)))
                        if facts:
                            act = Activation(rule=self, facts=facts)
                            RULE_WATCHER.debug("Got activation: %s", act)
                            yield act

            return tuple(set(_activations()))

    def conds(self):
        """
        Simple method to access Rule's conditions from heirs

        """
        return self.__conds

    def fn(self):
        """
        Simple method to access Rule's function from heirs

        """
        return self.__fn


class AND(Rule):
    """
        ``AND`` **conditional element.**

        See (:ref:`conditional_and`) narrative documentation.

    """
    pass


class NOT(Rule):
    """
    ``NOT CE``

    See (:ref:`conditional_not`) narrative documentation

    .. TODO:: Raise exception when multiple patterns are given to NOT

    """
    def __init__(self, *conds, salience=0):
        super().__init__(*conds, salience=salience)

    def get_activations(self, factlist):
        """
        Returns an Activation for each fact that
        **does not match** this rule

        This is the opposite of :obj:`pyknow.rule.Rule.get_activations`

        :param factlist: FactList of type :obj:`pyknow.factlist.FactList`
        :return: tuple containing the matching activation

        """
        activations = super().get_activations(factlist)
        if activations:
            return tuple()
        else:
            fact = factlist.matches(InitialFact())
            if fact:
                factidx = fact[0]
                act = tuple([Activation(rule=self, facts=(factidx, ))])
                RULE_WATCHER.debug("Got activation: %s", act)
                return act
            else:
                return tuple()


class OR(Rule):
    """

    ``Or CE``
    See (:ref:`conditional_or`) narrative documentation

    """
    def __init__(self, *conds, salience=0):
        super().__init__(*conds, salience=salience)

    def get_activations(self, factlist):
        """Return a tuple with the activations of this rule."""
        matches = []
        for cond in self._Rule__conds:
            for cond in self._Rule__conds:
                if issubclass(cond.__class__, Rule):
                    acts = cond.get_activations(factlist)
                    if not acts:
                        break
                    for act in acts:
                        for fact in act.facts:
                            matches.append([fact])
                elif isinstance(cond, Fact):
                    match = factlist.matches(cond)
                    if match:
                        matches.append(match)

        if matches:
            act = tuple([Activation(rule=self,
                                    facts=[fact[0] for fact in matches])])
            RULE_WATCHER.debug("Got activation: %s", act)
            return act
        else:
            return tuple()
