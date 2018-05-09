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

     "Pattern" -> "Fact" [label="which is a special usage for"];

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
if every one of them matches. Therefore, it behaves like `AND` by default.

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
make the rule match.

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
or combination of facts. Therefore this element matches the *absence* of
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

   @Rule(Number(MATCH.a),
         Number(MATCH.b),
         TEST(lambda a, b: a > b),
         Number(MATCH.c),
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

   @Rule(FORALL(Student(MATCH.name),
                Reading(MATCH.name),
                Writing(MATCH.name),
                Arithmetic(MATCH.name)))
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

This element performs an exact match with the given value. The matching
is done using the equality operator `==`.

.. code-block:: python
   :caption: Match if the first element is exactly `3`

   @Rule(Fact(L(3)))
   def _():
       pass

.. note::

   This is the default FC used when no FC is given as a pattern value.
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

   This element **only** matches if the element exist.


P (Predicate Field Constraint)
++++++++++++++++++++++++++++++

The match of this element is the result of applying the given callable to
the fact-extracted value. If the callable returns `True` the FC will
match, in other case the FC will not match.

.. code-block:: python
   :caption: Match if some fact is declared whose first parameter is an instance of int

   @Rule(Fact(P(lambda x: isinstance(x, int))))
   def _():
       pass


Composing FCs: `&`, `|` and `~`
-------------------------------

All FC can be composed together using the composition operators `&`, `|`
and `~`.


`ANDFC()` a.k.a. `&`
+++++++++++++++++++++

The composed FC matches if all the given FC match.

.. code-block:: python
   :caption: Match if key `x` of `Point` is a value between 0 and 255.

   @Rule(Fact(x=P(lambda x: x >= 0) & P(lambda x: x <= 255)))
   def _():
       pass


`ORFC()` a.k.a. `|`
++++++++++++++++++++

The composed FC matches if any of the given FC matches.

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

Any pattern and some FCs can be binded to a name using the `<<` operator.

.. code-block:: python
   :caption: The first value of the matching fact will be binded to the name `value` and passed to the function when fired.

   @Rule(Fact('value' << W()))
   def _(value):
       pass


.. deprecated:: 1.2.0

   Use *MATCH* object instead.


.. code-block:: python
   :caption: The whole matching fact will be binded to `f1` and passed to the function when fired.

   @Rule('f1' << Fact())
   def _(f1):
       pass

.. deprecated:: 1.2.0

   Use *AS* object instead.


MATCH object
------------

The MATCH objects helps generating more readable name bindings. Is syntactic
sugar for a `Wildcard Field Constraint` binded to a name. For example:

.. code-block:: python

   @Rule(Fact(MATCH.myvalue))
   def _(myvalue):
       pass

Is exactly the same as:

.. code-block:: python

   @Rule(Fact("myvalue" << W()))
   def _(myvalue):
       pass


AS object
---------

The AS object like the MATCH object is syntactic sugar for generating bindable
names. In this case any attribute requested to the AS object will return a
string with the same name.

.. code-block:: python

   @Rule(AS.myfact << Fact(W()))
   def _(myfact):
       pass

Is exactly the same as:

.. code-block:: python

   @Rule("myfact" << Fact(W()))
   def _(myfact):
       pass

.. warning::

   This behavior will vary in future releases of PyKnow and the string flavour
   of the operator may disappear.


Nested matching
---------------

.. versionadded:: 1.3.0

Nested matching is useful to match against Fact values which contains nested
structures like dicts or lists.

.. code-block:: python

   >>> Fact(name="scissors", against={"scissors": 0, "rock": -1, "paper": 1})
   >>> Fact(name="paper", against={"scissors": -1, "rock": 1, "paper": 0})
   >>> Fact(name="rock", against={"scissors": 1, "rock": 0, "paper": -1})

Nested matching take the form field__subkey=value. (That’s a
double-underscore). For example:

.. code-block:: python

   >>> @Rule(Fact(name=MATCH.name, against__scissors=1, against__paper=-1)) 
   ... def what_wins_to_scissors_and_losses_to_paper(self, name):
   ...     print(name)


Is possible to match against an arbitrary deep structure following the same method.

.. code-block:: python

   >>> class Ship(Fact):
   ...    pass
   ...
   >>> Ship(data={
   ...     "name": "SmallShip",
   ...     "position": {
   ...         "x": 300,
   ...         "y": 200},
   ...     "parent": {
   ...         "name": "BigShip",
   ...         "position": {
   ...             "x": 150,
   ...             "y": 300}}})

In this example we can check for collision between a ship and its parent with
the following rule:

.. code-block:: python

   >>> @Rule(Ship(data__name=MATCH.name1,
   ...            data__position__x=MATCH.x,
   ...            data__position__y=MATCH.y,
   ...            data__parent__name=MATCH.name2,
   ...            data__parent__position__x=MATCH.x,
   ...            data__parent__position__y=MATCH.y))
   ... def collision_detected(self, name1, name2, **_):
   ...     print("COLLISION!", name1, name2)

If the nested data structure contains list, tuples or any other sequence you
can use numeric indexes as needed.

.. code-block:: python

   >>> Ship(data={
   ...     "name": "SmallShip",
   ...     "position": {
   ...         "x": 300,
   ...         "y": 200},
   ...     "enemies": [
   ...         {"name": "Destroyer"},
   ...         {"name": "BigShip"}]})
   >>>
   >>> @Rule(Ship(data__enemies__0__name="Destroyer"))
   ... def next_enemy_is_destroyer(self):
   ...     print("Bye byee!")


Mutable objects
---------------

PyKnow's matching algorithm depends on the values of the declared facts being
immutable.

When a `Fact` is created, all its values are transformed to an immutable type
if they are not. For this matter the method `pyknow.utils.freeze` is used
internally.


.. code-block:: python

   >>> class MutableTest(KnowledgeEngine):
   ...     @Rule(Fact(v1=MATCH.v1, v2=MATCH.v2, v3=MATCH.v3))
   ...     def is_immutable(self, v1, v2, v3):
   ...         print(type(v1), "is Immutable!")
   ...         print(type(v2), "is Immutable!")
   ...         print(type(v3), "is Immutable!")
   ...
   >>> ke = MutableTest()
   >>> ke.reset()
   >>> ke.declare(Fact(v1={"a": 1, "b": 2}, v2=[1, 2, 3], v3={1, 2, 3}))
   >>> ke.run()
   frozendict is Immutable
   frozenlist is Immutable
   frozenset is Immutable
   >>>


.. note::

   You can import `frozendict` and `frozenlist` from `pyknow.utils` module.
   However `frozenset` is a Python built-in type.


Register your own mutable freezer
+++++++++++++++++++++++++++++++++

If you need to include your own custom mutable types as fact values you have to
register a specialized type freezer for your custom type.

.. code-block:: python

   >>> from pyknow.utils import freeze
   >>> @freeze.register(MyType)
   ... def freeze_mytype(obj):
   ...     return ... # My frozen version of my type


Unfreeze frozen objects
+++++++++++++++++++++++

To easily unfreeze the frozen objects `pyknow.utils` contains an `unfreeze` method.

.. code-block:: python

   >>> class MutableTest(KnowledgeEngine):
   ...     @Rule(Fact(v1=MATCH.v1, v2=MATCH.v2, v3=MATCH.v3))
   ...     def is_immutable(self, v1, v2, v3):
   ...         print(type(unfreeze(v1)), "is Mutable!")
   ...         print(type(unfreeze(v2)), "is Mutable!")
   ...         print(type(unfreeze(v3)), "is Mutable!")
   ...
   >>> ke = MutableTest()
   >>> ke.reset()
   >>> ke.declare(Fact(v1={"a": 1, "b": 2}, v2=[1, 2, 3], v3={1, 2, 3}))
   >>> ke.run()
   dict is Mutable
   list is Mutable
   set is Mutable
   >>>

.. note::

   The same `freeze` registration procedure shown above also applies to
   `unfreeze`.
