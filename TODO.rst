TODO
____

- Add more tests:
  - Tests for test_ce
  - More fact comparision tests, found a bug 
    on 2cdbe2f7a935a9e98e34b14d69f82ad78c0e3c83 that was not covered
- Make a good documentation
- Implement variable getting/setting


Variables
+++++++++

As stated before, we should be able to capture variables to reuse
in later rules.

That'd meant adding a context somewhere.
TBD: what the context should be and what should it contain.

::

    class RefrigeratorLogic(KnowledgeEngine):
        @Rule(Fact(name=C('name'), surname=C("surname")),
              Fact(name=V('name', surname=NOT(V('surname'))))
        def common_names(self): #RHSd
            return True
