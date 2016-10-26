Basic concepts
==============

A :obj:`pyknow.engine.KnowledgeEngine` runs a :obj:`pyknow.factlist.FactList`
against a set of rules defined in the KnowledgeEngine.


Rule
++++

``pyknow`` :obj:`pyknow.rule.Rule` objects are equivalent to ``defrule``,
the LHS, except the rule 'name' is actually defined by the method it triggers.

The clips user guide states that:

::

        You can have any number of patterns or actions in a rule. The important
        point to realize is that the rule is placed on the agenda only if all
        the patterns are satisfied by facts. This type of restriction is called
        a logical AND conditional element  (CE)

Wich implies the Rule's behavior defaults to the :ref:`conditional_and`'s behavior.
:ref:`conditional_and` can have nested conditional elements.

Rules can actually be swapped by Conditional Elements, but, for convention, a
Rule object must be used as the parent::

    @Rule(AND(...)) # Good
    @Rule(Fact(), Fact()) # Good
    @Rule(OR(...)) # Good

    @AND(Fact(), Fact()) # Will actually work, not recomended for clarity reasons
    @OR(...) # Will actually work, not recomended for clarity reasons


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


Example
+++++++

A tipical usage would be a simple module, with some rules and methods
decaring other rules


.. code-block:: lisp

    (defmodule BASE)
    (focus BASE)

    (defrule BASE::base (failure True) => (assert failed True))
    (defrule BASE::failed (failed True) => (printout t "Failed"))

    (deffacts BASE::init_facts
        (failure True))

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

Pyknow's way of things **forces** modules, there is not "MAIN" module on wich
declare things, but you could just as easily make one.

This is actually the same as CLIPs behavior, except that clips defaults to
a ``MAIN`` module, and its focus defaulted to it.
