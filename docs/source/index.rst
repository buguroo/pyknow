.. pyknow documentation master file, created by
   sphinx-quickstart on Tue Oct 25 12:19:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyknow's documentation!
==================================

Pyknow is a `CLIPS <clipsrules.sourceforge.net>`_-inspired inference engine
implemented in pure-python and enhanced with the hability to create a
inference-engine tree structure.

Extracted from CLIPS documentation::

    CLIPS is an expert system tool developed by the Software Technology Branch
    (STB), NASA/Lyndon B. Johnson Space Center. Since its first release in
    1986, CLIPS has undergone continual refinement and improvement. It is now
    used by thousands of people around the world. The Internet news group
    comp.ai.shells often has discussions of CLIPS.  CLIPS is designed to
    facilitate the development of software to model human knowledge or
    expertise.

    There are three ways to represent knowledge in CLIPS:

    - Rules, which are primarily intended for heuristic knowledge based
      on experience.
    - Deffunctions and generic functions, which are primarily intended for
      procedural knowledge.
    - Object-oriented programming, also primarily intended for procedural
      knowledge. The five generally accepted features of object-oriented
      programming are supported: classes, message-handlers, abstraction,
      encapsulation, inheritance, polymorphism. Rules may pattern match on
      objects and facts.

For that matter, ``pyknow`` implements:

:obj:`pyknow.engine.KnowledgeEngine`
    ``modules`` on clips. Handles set of rules and facts, ``encapsulating``
    the knowledge.

:obj:`pyknow.rule.Rule`
    ``rules`` on clips, made with the same intent in mind, act as a decorator
    for the LHS methods of a :obj:`pyknow.engine.KnowledgeEngine`.

:obj:`pyknow.fact.Fact`
    Facts are objects that, by default, have implemented the basic types
    behavior (:obj:`pyknow.fact.T`, :obj:`pyknow.fact.V`,
    :obj:`pyknow.fact.C`, :obj:`pyknow.fact.L`), and can be extended.

Reasoning behind pyknow
-----------------------

CLIPs is a mature, widely tested and used expert system.

Pyknow implementation aims to behave as much as CLIPs as possible, thus
inheriting part of that maturity, but respecting a more pythonic syntax,
having all the advantages of a python implementation.

::

        CLIPS is a type of computer language designed for writing applications
        called expert systems. An expert system is a program which is
        specifically intended to model human expertise or knowledge. In
        contrast, common programs such as payroll programs, word processors,
        spreadsheets, computer games, and so forth, are not intended to embody
        human expertise or knowledge. (One definition of an expert is someone
        more than 50 miles from home and carrying a briefcase.)

        CLIPS is calledan expert system tool because it is a complete
        environment for developing expert systems which includes features such
        as an integrated editor and a debugging tool. The word shell is
        reserved for that portion of CLIPS which performs inferences or
        reasoning.

        The CLIPS shell provides the basic elements of an expert system:
        1. fact-list and instance-list:  Global memory for data
        2. knowledge-base:  Contains all the rules, the rule-base
        3. inference engine:  Controls overall execution of rules

        A program written in CLIPS may consist of rules, facts, and objects.
        The inference engine decides which rules should be executed and when. A
        rule‑based  expert system written in CLIPS is a data-driven program
        where the facts, and objects if desired, are the data that stimulate
        execution via the inference engine.

Pyknow's basic intent is to:

    #. Be pure-python and as pythonic as possible
    #. Behave as much as ``CLIPS`` as possible
    #. Provide the basic elements of an expert system

        #. A ``fact-list`` and ``instance-list`` -> \
                   :obj:`pyknow.factlist.FactList`
        #. A inference engine, via :obj:`pyknow.engine.KnowledgeEngine`
        #. A ``knowledge-base``, available via
           :func:`pyknow.engine.KnowledgeEngine.get_rules`

    #. Provide a tree structure to ``inference engines`` interaction.


Narrative documentation
-----------------------


.. toctree::
   introduction
   ce
   trees
   :maxdepth: 2

Source documentation
--------------------

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
