Basic usage
===========

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


Rule
++++

``pyknow`` :obj:`pyknow.rule.Rule` objects are equivalent to ``defrule``,
the LHS.


Engine
++++++


Asserting facts
+++++++++++++++


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


