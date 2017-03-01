TODO
====

This document contains a list of tasks to do in the
`feature-rete-algorithm` branch.


General goals
-------------

- Implement the RETE algorithm as described in the author original paper
  http://reports-archive.adm.cs.cmu.edu/anon/scan/CMU-CS-79-forgy.pdf.

- Any improvement of the original algorithm is OUT OF THE SCOPE of this
  branch and MUST NOT be implemented yet.

- Clean old/innecessary code and documentation.

- Create an ABC for each element of the system to have a well defined
  and clean interface. Namely: Fact, Rule, Strategy, Agenda and
  Activation. Besides any element needed by RETE.


Changes in already defined classes
----------------------------------


`Fact`
~~~~~~

- Facts must be completely hashable.

- At instantiation time, all passed pairs (key-value) must be stored
  internally and exposed as instance attributes.

- Facts don't handle activations/capturations anymore, this will be
  handled by the RETE network.


`Rule`
~~~~~~

- Rules don't handle activations/capturations anymore, this will be
  handled by the RETE network.


Implementation of the RETE algorithm
------------------------------------

- The used terminology is as in the original document. Quoting the
  original document as much as possible.

- The RETE algorithm MUST NOT be used directly by other parts in the
  system, but interfaced through a class that allow us to exchange the
  implementation in the future.

- Generation of the RETE network is a duty of the RETE network itself.
  This means that no logic of node generation can be hardcoded in Facts
  nor Rules, therefore Facts and Rules have to provide a clear interface
  to allow other objects to inspect them (iteration maybe?).


MOTO
----

https://ih1.redbubble.net/image.108756255.6023/raf,750x1000,075,t,322e3f:696a94a5d4.u5.jpg
