.. _`trees`:

KnowledgeEngine Trees
=====================

Tree structures for :obj:`pyknow.engine.KnowledgeEngine` are objects that
allow interaction between multiple :obj:`pyknow.engine.KnowledgeEngine`
in an orderly manner.

A :obj:`pyknow.tree.KETree` object is built given a tree-like dictionary
structure of nodes and children, like::

        {
            'node': KETree(),
            'children': [
                {
                    'node': KETree()
                },
                {
                    'node': KETree(),
                    'children': [
                        {'node': KETree()}
                    ]
                }
            ]
        }

Given a tree made of `pyknow.engine.KnowledgeEngine` ::

    Parent1
    │
    └──┬─ Children1
       │  ├─ SubChildren1
       │  │
       │  └─ SubChildren2
       │
       └─ Children2

We get an execution order of::

    SubChildren1 → SubChildren2 → Children2 → Children1 → Parent1

And all children have its parent defined as the KnowlegeEngine that
is its parent in the tree.
