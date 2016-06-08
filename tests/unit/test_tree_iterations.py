
def test_tree_iterations():
    """ test tree iteration """
    from pyknow.tree import KETree
    from pyknow.engine import KnowledgeEngine

    a = KETree(
        {'node': KnowledgeEngine(), 'children': [
            {'node': KnowledgeEngine(), 'children': []},
            {'node': KnowledgeEngine(), 'children': []}
        ]}
    )

    assert len(a.nodes) == 3

    b = 3
    for elements in a:
        b -= 1
        assert len(elements) == b
