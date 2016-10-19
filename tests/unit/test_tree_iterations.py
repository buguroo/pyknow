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


def test_tree_NOT():
    """
        Test tree not
    """

    from pyknow.tree import KETree
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, NOT
    from pyknow.fact import Fact, InitialFact

    executions = []
    global executions

    class Child(KnowledgeEngine):
        @Rule(Fact(always_run=True))
        def always_run(self):
            executions.append(1)
            self.parent.declare(Fact(inherited=True))

    class Parent(KnowledgeEngine):
        @Rule(Fact(inherited=True))
        def inherited(self):
            executions.append(2)

        @Rule(NOT(Fact(not_inherited=True)))
        def not_inherited(self):
            executions.append(3)

    tree_ = {
        'node': Parent(),
        'children': [{'node': Child(), 'children': []},
                     {'node': Child(), 'children': []}]}

    tree_['node'].declare(InitialFact())
    tree_['children'][0]['node'].declare(InitialFact())
    tree_['children'][0]['node'].declare(Fact(always_run=True))
    tree_['children'][0]['node'].declare(Fact(not_inherited=False))

    KETree(tree_).run_sequential()
    print(executions)
    assert len(executions) == 3
