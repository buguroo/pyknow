#!/usr/bin/env python
"""

Definitions of clips' Conditional Elements, except
``Pattern Conditional Element``.

``Pattern CE`` defines direct matching against patterns, wich is a special
case implemented in :mod:`pyknow.fact`.

.. note:: We only implemente ``deftemplate``
          patterns in pyknow. Ordered patterns are not (and will not be)
          supported

All Conditional Elements MUST be enclosed in Rule decorators,
and only contain Fact objects or other Connective Constraints, as per
convention.

.. note:: A Rule object behaves the same as an AND CE,
          and can be swapped if needed.

Here, the following CEs are defined:

    #. Or Conditional Element
    #. And Conditional Element
    #. Not Conditional Element

As described in clips' basic programming guide,
sections 5.4.3, 5.4.4 and 5.4.5 respectively.

See section 5.4.X in the `BPG <http://clipsrules.sourceforge.net/docum\
        entation/v624/bpg.htm#_Toc11859658>`_



>>> from pyknow.rule import AND, Rule
>>> from pyknow.fact import Fact, L
>>> from pyknow.engine import KnowledgeEngine

>>> def foo():
...    class RefrigeratorLogic(KnowledgeEngine):
...        food_spoiled = False
...        @Rule(AND(Fact(light=L("on")), Fact(door=L("open"))))
...        def food_spoiled(self):
...            self.food_spoiled = True
...    ke = RefrigeratorLogic()
...    ke.reset()
...    ke.declare(Fact(light="on"))
...    ke.declare(Fact(door="open"))
...    ke.run()
...    return ke.food_spoiled

>>> assert foo()


As from the CLIPS userguide (\
`Chapter 2   Following the Rules <http://clipsrules.sourceforge.net/doc\
        umentation/v624/ug.htm#_Toc412126080>`_)


.. code-block:: lisp

    (defrule duck "Here comes the quack"     ; Rule header
       (animal-is duck)                      ; Pattern
       =>                                       ; THEN arrow
          (assert (sound-is quack)))            ; Action


More examples from the manual:

.. code-block:: lisp

    (clear)

    (defrule find-data
      (data ? blue red $?)
      =>)
    (reset)
    (agenda)

    ! 0      find-data: f-5
    ! 0      find-data: f-3
    ! For a total of 2 activations.

    (facts)

    !f-0     (initial-fact)
    !f-1     (data 1.0 blue "red")
    !f-2     (data 1 blue)
    !f-3     (data 1 blue red)
    !f-4     (data 1 blue RED)
    !f-5     (data 1 blue red 6.9)
    !For a total of 6 facts.


.. note:: Right now we don't have Connective Constraints implemented (CC)
          This means that we can't have partially-matching facts (so $? won't
          have an equivalent. That's why it's ommited in the python equivalent)

.. code-block:: python

    class KE(KnowledgeEngine):
        @Rule(f0=T(lambda True), f1="blue", f2="red")
        def matches(self):
            pass

    a = KE()
    a.reset()
    a.run()
    print(a.agenda)
    print(a._facts._facts)
"""

from functools import update_wrapper
from itertools import product

from pyknow.factlist import FactList
from pyknow.fact import InitialFact, Fact, Context
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
        return "Rule(conds={})".format(self.__conds)

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
        if self.__fn is None:
            if fst is not None:
                self.__fn = fst
                return update_wrapper(self, self.__fn)
            else:
                raise AttributeError("Mandatory function not provided.")
        else:
            if hasattr(fst, 'context') and isinstance(fst.context, Context):
                self.ke = fst

            args = (tuple() if fst is None else (fst,)) + args
            return self.__fn(*args, **kwargs)

    def get_activations(self, factlist):
        """
        For this :obj:`pyknow.rule.Rule`, returns all the
        :obj:`pyknow.activation.Activation`, for the provided factlist.

        :param factlist: :obj:`pyknow.factlist.FactList` to match against.
        :return: Tuple of unique :obj:`pyknow.activation.Activation` matches.

        """

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
        ``AND`` **operator.**

        This is the default Rule behavior

        For convention, :obj:`pyknow.rule.Rule` objects should not be
        nested, but the CEs (:obj:`pyknow.rule.AND`, :obj:`pyknow.rule.OR`,
        :obj:`pyknow.rule.NOT`) can.

        Example:

        .. code-block:: python

            # Valid
            @Rule(AND(Fact(foo=L('1'), bar=L('2')),
                     Fact(baz=L('2'))))
            def foo():
                self.declare(stuff=1)

        Clips equivalent:

        .. code-block:: lisp

            (defrule system-fault-3 (and((foo 1) (bar 2) (baz 2)))
            => (assert stuff 1))


        Example:

        .. code-block:: python

            # Valid
            @Rule(Fact(foo=L('1'), bar=L('2')),
                 Fact(baz=L('2')))
            def foo():
                self.declare(stuff=1)

        Clips equivalent:

        .. code-block:: lisp

            (defrule system-fault-3 (and((foo 1) (bar 2) (baz 2)))
            => (assert stuff 1))


        As per convention, **this should not be done**:

        .. code-block:: python

            # Not valid
            Rule(Rule(Fact(foo=L('1'), bar=L('2')),
                      Fact(baz=L('2'))))
            def foo():
                self.declare(stuff=1)


        From clips documentation::

            CLIPS assumes that all rules have an implicit and conditional
            element surrounding the conditional elements on the LHS. This means
            that all conditional elements on the LHS must be satisfied before
            the rule can be activated. An explicit and conditional element is
            provided to allow the mixing of and CEs and or CEs. This allows
            other types of conditional elements to be grouped together within
            or and not CEs. The and CE is satisfied if all of the CEs inside of
            the explicit and CE are satisfied.

    """
    pass


class NOT(Rule):
    """
        ``NOT CE``

        The opposite of AND constraint, ensures that a condition is **not**
        met.

        Extracted from CLIPs' manual::

             Sometimes the lack of information is meaningful; i.e., one wishes
             to fire a rule if a pattern entity or other CE does not exist. The
             not conditional element provides this capability. The not CE is
             satisfied only if the conditional element contained within it is
             not satisfied. As with other conditional elements, any number of
             additional CEs may be on the LHS of the rule and field constraints
             may be used within the negated pattern.  Syntax <not-CE> ::= (not
             <conditional-element>)

             Only one CE may be negated at a time. Multiple patterns may be
             negated by using multiple not CEs. Care must be taken when
             combining not CEs with or and and CEs; the results are not always
             obvi­ous!  The same holds true for variable bindings within a not
             CE. Previously bound variables may be used freely inside of a not
             CE. However, variables bound for the first time within a not CE
             can be used only in that pattern.


        That said, we actually **allow** multiple patterns to be negated.

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
    Or CE, ensures that ANY condition in
    the rule matches.

    From clips documentation::

        The or conditional element allows any one of several conditional
        elements to activate a rule. If any of the conditional elements inside
        of the or CE is satisfied, then the or CE is satisfied. If all other
        LHS condi­tional elements are satisfied, the rule will be activated.
        Note that a rule will be activated for each conditional element with an
        or CE that is satisfied (assuming the other conditional elements of the
        rule are also satisfied). Any number of conditional elements
        may appear within an or CE.

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
