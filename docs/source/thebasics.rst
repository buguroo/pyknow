The Basics
==========

An expert system is a program capable of pairing up a set of **facts** with
a set of **rules** to those facts, and execute some actions based on the
matching rules.


Facts
-----

`Facts` are the basic unit of information of PyKnow. They are used by
the system to reason about the problem.

Let's enumerate some facts about `Facts`, so... metafacts ;)

#. The class `Fact` is a subclass of `dict`.

   .. code-block:: python

      >>> f = Fact(a=1, b=2)
      >>> f['a']
      1

#. Therefore a `Fact` does not mantain an internal order of items.

   .. code-block:: python

      >>> Fact(a=1, b=2)  # Order is arbirary :O
      Fact(b=2, a=1)


#. In contrast to `dict`, you can create a `Fact` without keys (only
   values), and `Fact` will create a numeric index for your values.

   .. code-block:: python

      >>> f = Fact('x', 'y', 'z')
      >>> f[0]
      'x'


#. You can mix autonumeric values with key-values, but autonumeric must
   be declared first:

   .. code-block:: python

      >>> f = Fact('x', 'y', 'z', a=1, b=2)
      >>> f[1]
      'y'
      >>> f['b']
      2

#. You can subclass `Fact` to express different kinds of data or extend
   it with your custom functionality.

   .. code-block:: python

      class Alert(Fact):
          """The alert level."""
          pass

      class Status(Fact):
          """The system status."""
          pass

      f1 = Alert('red')
      f2 = Status('critical')


   .. code-block:: python

      from pyknow import Fact
      from django.contrib.auth.models import User as DjangoUser

      class User(Fact):
          @classmethod
          def from_django_model(cls, obj):
              return cls(pk=obj.pk,
                         name=obj.name,
                         email=obj.email)

          def save_to_db(self):
              return DjangoUser.create(**self)

#. `Fact` fields can be validated automatically for you if you define them
   using `Field`. `Field` uses the Schema_ library internally for data validation.
   Also, a field can be declared *mandatory* or have a *default*.

   .. code-block:: python
      from uuid import uuid4

      class User(Fact):
          uid = Field(int, default=uuid4)
          username = Field(str, mandatory=True)
          password = Field(str, mandatory=True)
          description = Field(str, default="Just another user")


Rules
-----

In PyKnow a **rule** is a callable, decorated with `Rule`.

Rules have two components, LHS (left-hand-side) and RHS
(right-hand-side).

* The *LHS* describes (using **patterns**) the conditions on which the rule
  * should be executed (or fired).

* The *RHS* is the set of actions to perform when the rule is fired.

For a `Fact` to match a `Pattern`, all pattern restrictions must be
**True** when the `Fact` is evaluated against it.

.. code-block:: python

   class MyFact(Fact):
       pass

   @Rule(MyFact())  # This is the LHS
   def match_with_every_myfact():
       """This rule will match with every instance of `MyFact`."""
       # This is the RHS
       pass

   @Rule(Fact('animal', family='felinae'))
   def match_with_cats():
       """
       Match with every `Fact` which:

         * f[0] == 'animal'
         * f['family'] == 'felinae'

       """
       print("Meow!")

You can use logic operators to express complex *LHS* conditions.

.. code-block:: python

   @Rule(
       AND(
           OR(User('admin'),
              User('root')),
           NOT(Fact('drop-privileges'))
       )
   )
   def the_user_has_power():
       """
       The user is a privileged one and we are not dropping privileges.

       """
       enable_superpowers()


For a `Rule` to be useful, it must be a method of a `KnowledgeEngine` subclass.

.. note::

   For a list of more complex operators you can check the
   :py:mod:`pyknow.operator` module.


`Facts` vs `Patterns`
+++++++++++++++++++++

The difference between `Facts` and `Patterns` is small. In fact,
`Patterns` are just `Facts` containing **Pattern Conditional Elements**
instead of regular data. They are used only in the *LHS* of a rule.

If you don't provide the content of a pattern as a **PCE**, PyKnow will
enclose the value in a `LiteralPCE` automatically for you.

Also, you can't declare any Fact containing a **PCE**, if you do, you
will receive a nice exception back.

.. code-block:: python

   >>> ke = KnowledgeEngine()
   >>> ke.declare(Fact(L("hi")))
   Traceback (most recent call last):
     File "<ipython-input-4-b36cff89278d>", line 1, in <module>
       ke.declare(Fact(L('hi')))
     File "/home/pyknow/pyknow/engine.py", line 210, in declare
       self.__declare(*facts)
     File "/home/pyknow/pyknow/engine.py", line 191, in __declare
       "Declared facts cannot contain conditional elements")
   TypeError: Declared facts cannot contain conditional elements


DefFacts
--------

Most of the time expert systems needs a set of facts to be present for
the system to work. This is the purpose of the `DefFacts` decorator.


.. code-block:: python

   @DefFacts()
   def needed_data():
       yield Fact(best_color="red")
       yield Fact(best_body="medium")
       yield Fact(best_sweetness="dry")


All `DefFacts` inside a KnowledgeEngine will be called every time the `reset`
method is called.

.. note::

   The decorated method MUST be generators.

   
.. versionadded:: 1.7.0

   The `reset()` method accepts any number of keyword parameters whose gets
   passed to `DefFacts` decorated methods if those methods present the same
   parameters.



KnowledgeEngine
---------------

This is the place where all the magic happens.

The first step is to make a subclass of it and use `Rule` to decorate its
methods.

After that, you can instantiate it, populate it with facts, and finally run it.

.. code-block:: python
   :caption: greet.py

   from pyknow import *

   class Greetings(KnowledgeEngine):
       @DefFacts()
       def _initial_action(self):
           yield Fact(action="greet")

       @Rule(Fact(action='greet'),
             NOT(Fact(name=W())))
       def ask_name(self):
           self.declare(Fact(name=input("What's your name? ")))

       @Rule(Fact(action='greet'),
             NOT(Fact(location=W())))
       def ask_location(self):
           self.declare(Fact(location=input("Where are you? ")))

       @Rule(Fact(action='greet'),
             Fact(name=MATCH.name),
             Fact(location=MATCH.location))
       def greet(self, name, location):
           print("Hi %s! How is the weather in %s?" % (name, location))

   engine = Greetings()
   engine.reset()  # Prepare the engine for the execution.
   engine.run()  # Run it!


.. code-block:: bash

   $ python greet.py
   What's your name? Roberto
   Where are you? Madrid
   Hi Roberto! How is the weather in Madrid?


Handling facts
++++++++++++++

The following methods are used to manipulate the set of facts the engine knows
about.


`declare`
~~~~~~~~~

Adds a new fact to the factlist (the list of facts known by the engine).

.. code-block:: python

   >>> engine = KnowledgeEngine()
   >>> engine.reset()
   >>> engine.declare(Fact(score=5))
   <f-1>
   >>> engine.facts
   <f-0> InitialFact()
   <f-1> Fact(score=5)

.. note::

   The same fact can't be declared twice unless `facts.duplication` is set to
   `True`.


`retract`
~~~~~~~~~

Removes an existing fact from the factlist.

.. code-block:: python
   :caption: Both, the index and the fact can be used with retract

   >>> engine.facts
   <f-0> InitialFact()
   <f-1> Fact(score=5)
   <f-2> Fact(color='red')
   >>> engine.retract(1)
   >>> engine.facts
   <f-0> InitialFact()
   <f-2> Fact(color='red')


`modify`
~~~~~~~~

Retracts some fact from the factlist and declares a new one with some changes.
Changes are passed as arguments.

.. code-block:: python

   >>> engine.facts
   <f-0> InitialFact()
   <f-1> Fact(color='red')
   >>> engine.modify(engine.facts[1], color='yellow', blink=True)
   <f-2>
   >>> engine.facts
   <f-0> InitialFact()
   <f-2> Fact(color='yellow', blink=True)


`duplicate`
~~~~~~~~~~~

Adds a new fact to the factlist using an existing fact as a template and adding
some modifications.

.. code-block:: python

   >>> engine.facts
   <f-0> InitialFact()
   <f-1> Fact(color='red')
   >>> engine.duplicate(engine.facts[1], color='yellow', blink=True)
   <f-2>
   >>> engine.facts
   <f-0> InitialFact()
   <f-1> Fact(color='red')
   <f-2> Fact(color='yellow', blink=True)


Engine execution procedure
++++++++++++++++++++++++++

This is the usual process to execute a `KnowledgeEngine`.

#. The class must be instantiated, of course.

#. The **reset** method must be called:

   * This declares the special fact *InitialFact*. Necessary for some
     rules to work properly.

   * Declare all facts yielded by the methods decorated with
     `@DefFacts`.

#. The **run** method must be called. This starts the cycle of execution.


Cycle of execution
++++++++++++++++++

In a conventional programming style, the starting point, the stopping point,
and the sequence of operations are defined explicitly by the programmer. With
PyKnow, the program flow does not need to be defined quite so explicitly. The
knowledge (`Rules`) and the data (`Facts`) are separated, and the
`KnowledgeEngine` is used to apply the knowledge to the data.

The basic execution cycle is as follows:

#. If the rule firing limit has been reached the execution is halted.

#. The top rule on the agenda is selected for execution. If there are no rules
   on the agenda, the execution is halted.

#. The RHS actions of the selected rule are executed (the method is called). As
   a result, rules may be **activated** or **deactivated**. Activated rules (those
   rules whose conditions are currently satisfied) are placed on the **agenda**.
   The placement on the agenda is determined by the **salience** of the rule and
   the current **conflict resolution strategy**. Deactivated rules are removed
   from the agenda.


Difference between `DefFacts` and `declare`
+++++++++++++++++++++++++++++++++++++++++++

Both are used to declare facts on the engine instance, but:

* `declare` adds the facts directly to the working memory.

* Generators declared with `DefFacts` are called by the **reset**
  method, and all the yielded facts they are added to the working
  memory using `declare`.


.. _Schema: https://github.com/keleshev/schema
