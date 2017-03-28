Reference
=========

The following diagram shows all the system components and the relationships
among them.

.. graphviz::

   digraph relation {
     "Fact";
     "KnowledgeEngine" [label="KnowledgeEngine"];

     "CE" [label="Conditional Element (CE)"];
     "Fact" [label="Fact"];
     "FC" [label="Field Constraint (FC)"];
     "Pattern" [label="Pattern", shape="box"];


     "CE" -> "CE" [label="contains"];
     "CE" -> "Pattern" [label="contains"];

     "FC" -> "FC" [label="some of them contains"];

     "Pattern" -> "FC" [label="contains"]
     "Rule" -> "CE" [label="contains"];
     "Rule" -> "Pattern" [label="contains"];

     "Pattern" -> "Fact" [label="which is a special kind of"];

     "KnowledgeEngine" -> "Rule" [label="contains"];
     "Fact" -> "KnowledgeEngine" [label="declare"];
     "Fact" -> "KnowledgeEngine" [label="retract"];
     "KnowledgeEngine" -> "Agenda" [label="has"];
     "KnowledgeEngine" -> "FactList" [label="has"];
     "KnowledgeEngine" -> "Strategy" [label="has"];
     "FactList" -> "Fact" [label="contains"];
     "Agenda" -> "Activation" [label="contains"];
     "Activation" -> "Rule" [label="contains"];
     "Activation" -> "Fact" [label="contains"];
     "Activation" -> "Context" [label="contains"];
     "Strategy" -> "Agenda" [label="organize"];
   }


Rule
----

`Rule` is the basic method of composing patterns. You can add as many
patterns or conditional elements as you want to a Rule and it will fire
if every one of them matches. Meaning it by default behaves like `AND`.

.. code-block:: python

   @Rule(<pattern_1>,
         <pattern_2>,
         ...
         <pattern_n>)
   def _():
       pass


The following diagram shows the rules of composition of a rule:

.. graphviz::

   digraph relation {
     "CE" [label="Conditional Element (CE)\nAND, OR, NOT"];
     "CFC" [label="Composable FC\n&, \|, ~", shape="box"];
     "FC" [label="Field Constraint (FC)\nL(), W(), P()"];
     "Pattern" [label="Pattern", shape="box"];

     "CE" -> "CE" [label="contains"];
     "CE" -> "Pattern" [label="contains"];
     "CFC" -> "FC" [label="contains"];
     "Pattern" -> "FC" [label="contains"]
     "Pattern" -> "CFC" [label="contains"]
     "Rule" -> "CE" [label="contains"];
     "Rule" -> "Pattern" [label="contains"];

   }

salience
++++++++

This value, by default `0`, determines the priority of the rule in
relation to the others. Rules with a higher salience will be fired
before rules with a lower one.

.. code-block:: python
   :caption: `r1` has precedence over `r2`

   @Rule(salience=1)
   def r1():
       pass

   @Rule(salience=0)
   def r2():
       pass


Conditional Elements: Composing Patterns Together
-------------------------------------------------

AND
+++

`AND` creates a composed pattern containing all Facts passed as
arguments. All of the passed patterns must match for the composed
pattern to match.

.. code-block:: python
   :caption: Match if two facts are declared, one matching Fact(1) and other matching Fact(2)

   @Rule(AND(Fact(1),
             Fact(2)))
   def _():
       pass


OR
++

`OR` creates a composed pattern in which any of the given pattern will
make the rule to match.

.. code-block:: python
   :caption: Match if a fact matching Fact(1) exists **and/or** a fact matching Fact(2) exists

   @Rule(OR(Fact(1),
            Fact(2)))
   def _():
       pass


.. warning::

   If multiple facts match, the rule will be fired multiple times, one
   for each valid combination of matching facts. 


NOT
+++

This element matches if the given pattern does not match with any fact
or combination of facts. Therefore this element match the *absence* of
the given pattern.

.. code-block:: python
   :caption: Match if no fact match with Fact(1)

   @Rule(NOT(Fact(1)))
   def _():
       pass


TEST
++++

Check the received callable against the current binded values. If the
execution returns `True` the evaluation will continue and stops
otherwise.

.. code-block:: python
   :caption: Match for all numbers `a`, `b`, `c` where a > b > c

   @Rule(Number('a' << W()),
         Number('b' << W()),
         TEST(lambda a, b: a > b),
         Number('c' << W()),
         TEST(lambda b, c: b > c))
   def _(a, b, c):
       pass


EXISTS
++++++

This CE receives a pattern and matches if one or more facts matches this
pattern. This will match only once while one or more matching facts
exists and will stop matching when there is no matching facts.

.. code-block:: python
   :caption: Match once when one or more Color exists

   @Rule(EXISTS(Color()))
   def _():
       pass


FORALL
++++++

The FORALL conditional element provides a mechanism for determining if a
group of specified CEs is satisfied for every occurence of another
specified CE.

.. code-block:: python
   :caption: Match when for every Student fact there is a Reading, Writing and Arithmetic fact with the same name.

   @Rule(FORALL(Student(W('name')),
                Reading(W('name')),
                Writing(W('name')),
                Arithmetic(W('name')))
   def all_students_passed():
       pass


.. note::

   All binded variables captured inside a `FORALL` clause won't be
   passed as context to the RHS of the rule.
   
.. note::

   Any time the rule is activated the matching fact is the InitialFact.


Field Constraints: FC for sort
------------------------------

L (Literal Field Constraint)
++++++++++++++++++++++++++++

This element performs a exact match with the given value. The matching
is done using the equality operator `==`.

.. code-block:: python
   :caption: Match if the first element is exactly `3`

   @Rule(Fact(L(3)))
   def _():
       pass

.. note::

   This is the default FC used when no FC is given as a value in a
   pattern.


W (Wildcard Field Constraint)
+++++++++++++++++++++++++++++

This element matches with **any** value.

.. code-block:: python
   :caption: Match if some fact is declared with the key `mykey`.

   @Rule(Fact(mykey=W()))
   def _():
       pass

.. note::

   This element **only** match if the element exist.


P (Predicate Field Constraint)
++++++++++++++++++++++++++++++

The match of this element is the result of apply the given callable to
the fact extracted value. If the callable returns `True` the FC will
match, in other case the FC will not match.


.. code-block:: python
   :caption: Match if some fact is declared which first parameter is an instance of int

   @Rule(Fact(P(lambda x: isinstance(x, int))))
   def _():
       pass


Composing FCs: `&`, `|` and `~`
-------------------------------

All FC can be composed together using the composition operators `&`,
`|` and `~`.


`ANDFC()` a.k.a. `&`
+++++++++++++++++++++

The composed FC match if all the given FC match.

.. code-block:: python
   :caption: Match if key `x` of `Point` is a value between 0 and 255.

   @Rule(Fact(x=P(lambda x: x >= 0) & P(lambda x: x <= 255)))
   def _():
       pass


`ORFC()` a.k.a. `|`
++++++++++++++++++++

The composed FC match if any of the given FC matches.

.. code-block:: python
   :caption: Match if `name` is either `Alice` or `Bob`.

   @Rule(Fact(name=L('Alice') | L('Bob')))
   def _():
       pass


`NOTFC()` a.k.a. `~`
+++++++++++++++++++++

This composed FC negates the given FC, reversing the logic. If the
given FC matches this will not and vice versa.

.. code-block:: python
   :caption: Match if `name` is not `Charlie`.

   @Rule(Fact(name=~L('Charlie')))
   def _():
       pass


Variable Binding: The `<<` Operator
-----------------------------------

Any patterns and some FC can be binded to a name using the `<<`
operator.

.. code-block:: python
   :caption: The first value of the matching fact will be binded to the name `value` and passed to the function when fired.

   @Rule(Fact('value' << W()))
   def _(value):
       pass

.. code-block:: python
   :caption: The whole matching fact will be binded to `f1` and passed to the function when fired.

   @Rule('f1' << Fact())
   def _(f1):
       pass
