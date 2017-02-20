.. _`conditional_elements`:

Conditional Elements
++++++++++++++++++++

Here, the following CEs are defined:

.. contents::
    :local:

Pattern Conditional Element
___________________________

``Pattern CE`` defines direct matching against patterns, wich is a special
case implemented in :mod:`pyknow.fact`.

The following constraints are defined in CLIPs:

 #. Literal Constraints
 #. Wildcards Single‑ and Multifield
 #. Variables Single‑ and Multifield
 #. Connective Constraints
 #. Predicate Constraints
 #. Return Value Constraints
 #. Pattern‑Matching with Object Patterns
 #. Pattern‑Addresses

Of those, the following are currently implemented in ``pyknow``:

 #. Literal constraints (:obj:`pyknow.fact.L`)
 #. Predicate Constraints (:obj:`pyknow.fact.T`)
 #. Return Value Constraints (:obj:`pyknow.fact.T`)
 #. Pattern‑Matching with Object Patterns (:obj:`pyknow.fact.T`),
    (:obj:`pyknow.fact.C`), (:func:`pyknow.fact.V`) (:func:`pyknow.fact.N`)
 #. Wildcard ($?) facts with (:obj:`pyknow.fact.W`)


.. note:: Predicate constraints, Pattern‑Matching with Object Patterns
          and Return Value Constraints are both implemented as
          :obj:`pyknow.fact.T` or derivatives.

.. note:: Pyknow also has the hability to capture and use values inside
          an engine context, between different Fact objects using
          :obj:`pyknow.fact.C`, :func:`pyknow.fact.V` :func:`pyknow.fact.N`.
          This is probably similar to Pattern-Matching with Object Patterns

According to clips' documentation::

    Pattern conditional elements consist of a collection of field constraints,
    wildcards, and variables which are used to constrain the set of facts or
    instances which match the pattern CE. A pattern CE is satisfied by each and
    every pattern entity that satisfies its constraints. Field constraints are
    a set of constraints that are used to test a single field or slot of a
    pattern entity


This is implemented by ``FactTypes`` wich represent different comparision
methods, and ``ValueSets``, wich represents a set of facts or instances
to test for pattern CE matching.

Facts MUST be of type ``Fact`` and its values should be of type
``FactType`` (wich defaults to L if not provided).

When declaring a fact in a KnowledgeEngine, fact must only be
of literal type (``L``).

.. note:: We only implemente ``deftemplate``
          patterns in pyknow. Ordered patterns are not (and will not be)
          supported

All Conditional Elements MUST be enclosed in Rule decorators,
and only contain Fact objects or other Conditional Elements, as per
convention.

.. note:: A Rule object behaves the same as an AND CE,
          and can be swapped if needed.

As described in clips' basic programming guide,
sections 5.4.3, 5.4.4 and 5.4.5 respectively.

See section 5.4.X in the
`BPG
<http://clipsrules.sourceforge.net/documentation/v624/bpg.htm#_Toc11859658>`_

.. code-block:: python

    from pyknow.rule import AND, Rule
    from pyknow.fact import Fact, L
    from pyknow.engine import KnowledgeEngine

    def foo():
       class RefrigeratorLogic(KnowledgeEngine):
           food_spoiled = False
           @Rule(AND(Fact(light=L("on")), Fact(door=L("open"))))
           def food_spoiled(self):
               self.food_spoiled = True

       ke = RefrigeratorLogic()
       ke.reset()
       ke.deffacts(Fact(light="on"))
       ke.deffacts(Fact(door="open"))
       # or:
       # ke.deffacts(Fact(light="on"), Fact(door="open"))
       ke.run()
       return ke.food_spoiled

    assert foo()


As from the CLIPS userguide (\
`Chapter 2: Following the Rules
<http://clipsrules.sourceforge.net/documentation/v624/ug.htm#_Toc412126080>`_)


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
        @Rule(Fact(f0=W(True), f1=L("blue"), f2=L("red")))
        def find_data(self):
            pass

    a = KE()
    a.reset()
    a.run()
    print(a.agenda)
    print(a._facts._facts)

.. _`conditional_or`:

Or Conditional Element
_______________________

Ensures that ANY condition in the rule matches.

From clips documentation::

    The or conditional element allows any one of several conditional
    elements to activate a rule. If any of the conditional elements inside
    of the or CE is satisfied, then the or CE is satisfied. If all other
    LHS condi­tional elements are satisfied, the rule will be activated.
    Note that a rule will be activated for each conditional element with an
    or CE that is satisfied (assuming the other conditional elements of the
    rule are also satisfied). Any number of conditional elements
    may appear within an or CE.


.. _`conditional_and`:

And Conditional Element
_______________________

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


.. _`conditional_not`:

Not Conditional Element
_______________________

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


That said, we actually **allow** multiple patterns to be negated, but
it **must not** be used like that.
