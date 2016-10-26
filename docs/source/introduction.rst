Basic usage
===========

Rule
++++

``pyknow`` :obj:`pyknow.rule.Rule` objects are equivalent to ``defrule``,
the LHS.


FactLists
+++++++++

``pyknow`` does not allow for Facts to use positional arguments, only
named arguments are allowed.

FactLists are equivalent to ``deffacts`` in ``CLIPS``

As of factlists themselves (see :obj:`pyknow.factlist.FactList`), you
can list their facts with :obj:`pyknow.factlist.Factlist._facts`, wich
will return all :obj:`pyknow.fact.Fact` representations, wich, as
opposite from ``CLIPS``, will show all conditions in the fact.

FactLists are declared in a :obj:`pyknow.engine.KnowledgeEngine`
and available vía :obj:`pyknow.engine.KnowledgeEngine._facts`.
Each KE has one FactList associated to it.


Conditional Elements
++++++++++++++++++++

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
    (:obj:`pyknow.fact.C`) and (:obj:`pyknow.fact.V`)

.. note:: Predicate constraints, Pattern‑Matching with Object Patterns
          and Return Value Constraints are both implemented as
          :obj:`pyknow.fact.T`

.. note:: Pyknow also has the hability to capture and use values inside
          an engine context, between different Fact objects using
          :obj:`pyknow.fact.C` and :obj:`pyknow.fact.V`. This is probably
          similar to Pattern-Matching with Object Patterns

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
       ke.declare(Fact(light="on"))
       ke.declare(Fact(door="open"))
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
        @Rule(f0=T(lambda True), f1="blue", f2="red")
        def matches(self):
            pass

    a = KE()
    a.reset()
    a.run()
    print(a.agenda)
    print(a._facts._facts)


Example
+++++++

A tipical usage would be a simple module, with some rules and methods
decaring other rules


.. code-block:: lisp

    (defmodule BASE)
    (defrule BASE::base (failure True) => (assert failed True))
    (defrule BASE::failed (failed True) => (printout t "Failed"))

    (deffacts BASE::init_facts
        (failure True))

    (focus BASE)
    (run)


Is equivalent on ``pyknow`` to:

.. code-block:: python

    from pyknow.rule import Rule
    from pyknow.engine import KnowledgeEngine
    from pyknow.fact import Fact

    class BASE(KnowledgeEngine):
        @Rule(Fact(failure=True))
        def base(self):
            self.declare(failed=True)

        @Rule(Fact(failed=True))
        def failed(self):
            print("Failed")

Pyknow way of things **forces** modules, there is not "MAIN" module on wich
declare things, but you could just as easily make one.

This is actually the same as CLIPs behavior, except that clips defaults to
a ``MAIN`` module, and its focus defaulted to it.


