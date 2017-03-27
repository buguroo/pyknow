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
     "PCE" [label="Pattern Conditional Element (PCE)"];
     "Pattern" [label="Pattern", shape="box"];


     "CE" -> "CE" [label="contains"];
     "CE" -> "Pattern" [label="contains"];

     "PCE" -> "PCE" [label="some of them contains"];

     "Pattern" -> "PCE" [label="contains"]
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
     "CPCE" [label="Composable PCE\n&, \|, ~", shape="box"];
     "PCE" [label="Pattern Conditional Element (PCE)\nL(), W(), P()"];
     "Pattern" [label="Pattern", shape="box"];

     "CE" -> "CE" [label="contains"];
     "CE" -> "Pattern" [label="contains"];
     "CPCE" -> "PCE" [label="contains"];
     "Pattern" -> "PCE" [label="contains"]
     "Pattern" -> "CPCE" [label="contains"]
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

where
+++++

Callable or list of callables that will be called if the rule's pattern match.

The callable parameters are analyzed and if they match with a binded
value of the pattern, they will be passed along.

.. code-block:: python
   :caption: Will match only for facts where `x` + `y` equals 42.

   @Rule(Fact(x='x' << W(),
              y='y' << W())
         where=lambda x, y: x + y == 42)
   def _(x, y):
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


Pattern Conditional Elements: PCE for sort
------------------------------------------

`LiteralPCE` a.k.a. L()
+++++++++++++++++++++++

This element performs a exact match with the given value. The matching
is done using the equality operator `==`.

.. code-block:: python
   :caption: Match if the first element is exactly `3`

   @Rule(Fact(L(3)))
   def _():
       pass

.. note::

   This is the default PCE used when no PCE is given as a value in a
   pattern.


`WildcardPCE` a.k.a. W()
++++++++++++++++++++++++

This element matches with **any** value.

.. code-block:: python
   :caption: Match if some fact is declared with the key `mykey`.

   @Rule(Fact(mykey=W()))
   def _():
       pass

.. note::

   This element **only** match if the element exist.


`PredicatePCE` a.k.a. P()
+++++++++++++++++++++++++

The match of this element is the result of apply the given callable to
the fact extracted value. If the callable returns `True` the PCE will
match, in other case the PCE will not match.


.. code-block:: python
   :caption: Match if some fact is declared which first parameter is an instance of int

   @Rule(Fact(P(lambda x: isinstance(x, int))))
   def _():
       pass


Composing PCEs: `&`, `|` and `~`
--------------------------------

All PCE can be composed together using the composition operators `&`,
`|` and `~`.


`ANDPCE()` a.k.a. `&`
+++++++++++++++++++++

The composed PCE match if all the given PCE match.

.. code-block:: python
   :caption: Match if key `x` of `Point` is a value between 0 and 255.

   @Rule(Fact(x=P(lambda x: x >= 0) & P(lambda x: x <= 255)))
   def _():
       pass


`ORPCE()` a.k.a. `|`
++++++++++++++++++++

The composed PCE match if any of the given PCE matches.

.. code-block:: python
   :caption: Match if `name` is either `Alice` or `Bob`.

   @Rule(Fact(name=L('Alice') | L('Bob')))
   def _():
       pass


`NOTPCE()` a.k.a. `~`
+++++++++++++++++++++

This composed PCE negates the given PCE, reversing the logic. If the
given PCE matches this will not and vice versa.

.. code-block:: python
   :caption: Match if `name` is not `Charlie`.

   @Rule(Fact(name=~L('Charlie')))
   def _():
       pass


Variable Binding: The `<<` Operator
-----------------------------------

Any patterns and some PCE can be binded to a name using the `<<`
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
