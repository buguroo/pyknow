Introduction
============

Philosophy
----------

We aim to implement a Python alternative to CLIPS, as compatible as
possible. With the goal of making it easy for the CLIPS programmer to
transfer all of his/her knowledge to this platform.


Features
--------

* Python 3 compatible.
* Pure Python implementation.
* Matcher based on the RETE algorithm.


Difference between CLIPS and PyKnow
-----------------------------------

#. CLIPS is a programming language, PyKnow is a Python library. This
   imposes some limitations on the constructions we can do (specially on
   the LHS of a rule).

#. CLIPS is written in C, PyKnow in Python. A noticeable impact in
   performance is to be expected.

#. In CLIPS you add facts using `assert`, in Python `assert` is a
   keyword, so we use `declare` instead.
