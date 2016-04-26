TODO
____

- Implement initial facts (deffacts in clips), that is,
  Facts that are still present after reset
- Implement Test CE
- Implement variable getting/setting


Initial Facts
=============

Defined facts that, once the KE has been reset, remain there.

::

    ke.declare_initial(Fact(foo=L('r')))

or maybe

::

    ke.declare(Fact(foo=L('r')), persistent=True)


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
