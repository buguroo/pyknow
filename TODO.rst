TODO
____

- Implement AND and OR connective constraints
- Implement initial facts (deffacts in clips), that is,
  Facts that are still present after reset
- Implement more CEs
- Implement variable getting/setting


ConditionalElements
+++++++++++++++++++

All conditional elements must be typed, that is:

    - Literal
    - Test
    - Variable Management

Clips' wildcard CE won't be available in pyknow

Literal CE
==========

::

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(Fact(refrigerator_light=L("on")), 
            NOT(Fact(refrigerator_door=L("closed")))) #LHS
        def food_spoiled(self): #RHS
            return True



Test CE
=======

::

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(Fact(name=T(lambda x: x.startswith('foo')))) #LHS
        def food_spoiled(self): #RHS
            return True


Deftemplates
++++++++++++

On the other hand, deftemplates are hardly improbable.
That be said, Ruso stablished deftemplates as simply facts

::


    class Person(Fact): pass

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(name=L("David"))
        def is_david(self):
            return True

        @Rule(foo=L(True),
              bar=L(True))
        def is_XayOn(self):
            return True

        @Rule(AND(name=L("David"), 
                  surname=L("Moran")))
        def is_moran(self):
            return True

    ke = RefrigeratorLogic()

    ke.declare(Person(name=L("David"), surname=L("Francos"), bar=L(True), foo=L(True)))
    ke.declare(Person(name=L("David"), surname=L("Moran"), foo=L(True), bar=L(False)))
    ke.declare(Person(name=L("David"), surname=L("Reguera"), foo=L(False), bar=L(False)))

    ke.get_activations() # Esto dará tres is_david, un is_XayOn y un is_moran



Variables
+++++++++

As stated before, we should be able to capture variables to reuse
in later rules.

::

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(Fact(name=C('name'), surname=C("surname")),
              Fact(name=V('name', surname=NOT(V('surname'))))
        def common_names(self): #RHSd
            return True


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


EXISTS CE
+++++++++

Clips' exista conditional element is implemented as a literal
CE in pyknow comparing against DEFINED and UNDEFINED constants.
