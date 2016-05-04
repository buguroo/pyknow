#!/usr/bin/env python
"""
Connective Constraints
++++++++++++++++++++++

Pyknow approach to a KE makes it mandatory for all the arguments to be
named, that is, no positional arguments here.

Connective constraints are AND, OR and NOT. Of those, only NOT
is currently implemented.

Usage should be the same for them as actually is for NOT

::


    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(AND(foo=L("bar"), bar=L("baz"))) #LHS
        def food_spoiled(self): #RHS
            return True

    ke = RefrigeratorLogic()
    ke.reset()
    ke.declare(Fact(
        foo=L("on"),
        bar=L("off")))
"""

from functools import update_wrapper
from itertools import product

from pyknow.factlist import FactList
from pyknow.fact import InitialFact, Fact, Context
from pyknow.activation import Activation


class Rule:
    """
        Base connective constraint.
        All connective constraints are to derive from this class,

        A Rule's behavior defaults to be the same as AND cc.
    """
    def __init__(self, *conds, salience=0):
        self.__fn = None
        self.context = Context()

        if not conds:
            conds = (InitialFact(),)
        self.__conds = conds

        self.salience = salience

    def __call__(self, fst=None, *args, **kwargs):
        """
        Decorate or call a function.

        This function is going to be called twice.

        - The first call is when the decorator is been created. At this
          point we assign the function decorated to ``self.__fn`` and
          return ``self`` to be called the second time.

        - The second call is to execute the decorated function, se we
          pass all the arguments along.
          We also assign the KnowledgeEngine's context to the rule, if
          available and if we're being called from a KE.
          Otherwise, each rule will make their own Context() object, empty
          and not shared between rules, when they're being evaluated.

          That allows us to assign rules to variables and apply them directly
          as well as using KEs

        """
        if self.__fn is None:
            if fst is not None:
                self.__fn = fst
                return update_wrapper(self, self.__fn)
            else:
                raise AttributeError("Mandatory function not provided.")
        else:
            if hasattr(fst, 'context') and isinstance(fst.context, Context):
                self.context = fst.context

            args = (tuple() if fst is None else (fst,)) + args
            return self.__fn(*args, **kwargs)

    def get_activations(self, factlist):
        """Return a tuple with the activations of this rule."""

        if not isinstance(factlist, FactList):
            raise ValueError("factlist must be an instance of FactList")
        else:
            def _activations():
                matches = []

                for cond in self.__conds:
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
                        else:
                            break
                else:
                    for match in product(*matches):
                        facts = tuple(sorted(set(match)))
                        if facts:
                            yield Activation(rule=self, facts=facts)

            return tuple(set(_activations()))

    def conds(self):
        """ Not-so-nice way to access __conds """
        return self.__conds


class AND(Rule):
    """
        AND operator.
        It's the default Rule behavior, except that a Rule cannot
        be nested for clarity reasons.
        This way, we've got::

            # Valid
            Rule(AND(Fact(foo=L('1'), bar=L('2')),
                     Fact(baz=L('2'))))

            # Valid
            Rule(Fact(foo=L('1'), bar=L('2')),
                 Fact(baz=L('2')))

            # Not valid
            Rule(Rule(Fact(foo=L('1'), bar=L('2')),
                      Fact(baz=L('2'))))
    """
    pass


class NOT(Rule):
    """
        NOT connective constraint.
        Effectively the opposite of AND constraint, ensures
        that a condition is NOT met.
    """
    def __init__(self, *conds, salience=0):
        super().__init__(*conds, salience=salience)

    def get_activations(self, factlist):
        """Returns the opposite of Rule.get_activations."""
        activations = super().get_activations(factlist)
        if activations:
            return tuple()
        else:
            fact = factlist.matches(InitialFact())
            if fact:
                factidx = fact[0]
                return tuple([Activation(rule=self, facts=(factidx, ))])
            else:
                return tuple()


class OR(Rule):
    """
        Or connective constraint, ensures that ANY condition in
        the rule matches.
    """
    def __init__(self, *conds, salience=0):
        super().__init__(*conds, salience=salience)

    def get_activations(self, factlist):
        """Return a tuple with the activations of this rule."""
        for cond in self._Rule__conds:
            matches = []

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
            return tuple([Activation(rule=self,
                                     facts=[fact[0] for fact in matches])])
