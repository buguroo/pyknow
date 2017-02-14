PyKnow
======

Pure Python knowledge-based inference engine (inspired by CLIPS).


Why?
----

There are a few ways to use CLIPS directly within python (such as pyclips),
but those are actually using CLIPS behind and does not allow you to provide
custom RHS in python. Also, you need to write the code in CLIPS and call
it within python, wich is not very pythonic.


How
---

We are trying to get an implementation as close as possible to CLIPS.
That means most of our examples and docs are direct references to CLIPs
reference manual or their examples


Example
-------

::

    class MyKnowledgeEngine(KnowledgeEngine):
        @Rule(Fact(a=L(1)))
        def my_rhs(self):
           pass

    engine = MyKnowledgeEngine()
    engine.reset()
    engine.declare(Fact(a=L(1)))
    engine.run()
