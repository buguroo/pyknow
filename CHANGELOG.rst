1.3.0
+++++

* `pyknow.operator` module.
* Nested matching.
* Added Talk 'Sistemas Expertos en Python con PyKnow - PyConES 2017' to docs
  folder.


1.2.0
+++++

* Freeze fact values as the default behavior to address Issue #9.
* Added `pyknow.utils.anyof` to mitigate Issue #7.
* Raise RuntimeError if a fact value is modified after declare().
* Added MATCH and AS objects.


1.1.1
+++++

* Removing the borg optimization for P field constraints.
* Use the hash of the check in the sorting of the nodes to always
  generate the same alpha part of the network.


1.1.0
+++++

* Allow any kind of callable in Predicate Field Constraints (P()).


1.0.1
+++++

* DNF of OR clause inside AND or Rule was implemented wrong.


1.0.0
+++++

* RETE matching algorithm.
* Better Rule decorator system.
* Facts are dictionaries.
* Documentation.


<1.0.0
++++++

* Unestable API.
* Wrong matching algorithm.
* Bad performance
* PLEASE DON'T USE THIS.
