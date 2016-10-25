#!/usr/bin/env python

"""
Tree structures for ``pyknow.engine.KnowledgeEngine`` objects that
allows interaction between multiple ``pyknow.engine.KnowledgeEngine``
in an orderly manner

"""


class KETree:
    """
    Given a prestablished *dictionary tree*, this acts
    as an iterator that yields results from farthest to nearest
    element, to execute them.

    The given dictionary tree should have a structure like this::

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

    That is, given::

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

    And all children have its parent defined.

    :param tree: Dictionary tree, following the described form

    """
    def __init__(self, tree):
        self.tree = tree
        self.finished = False
        self._tree = tree.copy()
        try:
            assert isinstance(self.tree, dict)
            assert self.is_valid_node(self.tree)
        except AssertionError:
            raise Exception("Not a valid KETree node specified")

    @classmethod
    def is_valid_node(cls, node):
        """
        Check if a given node is a valid node, that is, a dictionary
        structure containing a 'node', and optionally childrens (that
        must follow this same conditions)

        """
        try:
            assert isinstance(node, dict)
            assert 'node' in node
            if 'children' in node:
                assert isinstance(node['children'], list)
                for child in node['children']:
                    KETree.is_valid_node(child)
        except AssertionError:
            return False
        else:
            return True

    def pop_furthest_elements(self):
        """
            Pop the furthest elements in the tree

            If parent is not set, this automatically
            sets it, that way it'll be available on
            processing but it's easily overrideable

        """

        def recurse(parent, results):
            """
            Recurse over tree
            """
            curr = []
            for num, child in enumerate(parent.get('children', {})):
                if not child['node'].parent:
                    child['node'].parent = parent['node']
                if 'children' in child and child['children']:
                    recurse(child, results)
                else:
                    results.append(child['node'])
                    curr.append(num)

            for num in reversed(curr):
                parent['children'].pop(num - 1)

            return result

        result = []
        recurse(self._tree, result)
        return result

    def __iter__(self):
        return self

    def __next__(self):
        results = self.pop_furthest_elements()
        if self.finished:
            raise StopIteration()
        if not results:
            self.finished = True
            return [self.tree['node']]
        return results

    @property
    def nodes(self):
        """
        Get all the nodes, plain, as should be executed.

        """
        result = []

        def recurse(parent):
            """ walk the tree """
            result.append(parent.get('node'))
            for element in parent.get('children', {}):
                recurse(element)

        recurse(self.tree)
        return result

    def run_sequential(self):
        """
        Sequential implementation of the tree execution.

        Just iterate over the tree (wich will be done as explained in
        :obj:`pyknow.tree.KETree` and call
        :func:`pyknow.engine.KnowledgeEngine.run`.

        """
        for elements in self:
            for element in elements:
                element.run()
