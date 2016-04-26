TODO
____

- Implement initial facts (deffacts in clips), that is,
  Facts that are still present after reset
- Implement Test CE
- Implement variable getting/setting


Test CE
=======

::

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(Fact(name=T(lambda x: x.startswith('foo')))) #LHS
        def food_spoiled(self): #RHS
            return True


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
