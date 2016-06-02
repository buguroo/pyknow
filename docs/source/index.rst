Pyknow
------

Pyknow is a clips-inspired knowledge engine tool for python3.4+


Rules and Facts, basic concepts
-------------------------------


Engines
-------


Data Types
----------

L
++

This is the basic data type, it means a literal.
So, when compared, it'll be compared to it as a literal, that is:

::

    L('foo') -> 'foo'

T
++

Test data type. In clips, this is called test CE.
It accepts a callable as argument, and evaluates it against its counterpart in the other fact.
So:

::

    Fact(something=T(lambda x: x == 'foo')) == Fact(something=L('foo'))


C & V
++++++
