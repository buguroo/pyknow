Introduction
============

Philosophy
----------

We aim to implement a Python alternative to CLIPS, as compatible as
possible. With the goal of making it easy for the CLIPS programmer to
transfer all the already knowledge she/he has to this platform.


Features
--------

* Python 3 compatible.
* Pure Python implementation.
* Matcher based on the RETE algorithm.


Differences between CLIPS and PyKnow
------------------------------------

#. CLIPS is a programming language, PyKnow is a Python library. This
   imposes some limitations in the expressivity of the LHS.

#. CLIPS is written in C, PyKnow in Python. A noticiable impact in
   performance is to be expected.

#. In CLIPS you add facts using `assert`, in Python `assert` is a
   keyword, so we use `declare` instead.
