TODO
____

- Implement Test CE
- Implement variable getting/setting


Test CE
=======

Test CE, executes a callable

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
