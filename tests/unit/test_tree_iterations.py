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
    from pyknow.fact import Fact, L

    executions = []
    global executions

    class Child(KnowledgeEngine):
        @Rule(Fact(always_run=L(True)))
        def always_run(self):
            executions.append(1)
            self.parent.declare(Fact(inherited=L(True)))

    class Parent(KnowledgeEngine):
        @Rule(Fact(inherited=L(True)))
        def inherited(self):
            executions.append(2)

        @Rule(NOT(Fact(not_inherited=L(True))))
        def not_inherited(self):
            executions.append(3)

    tree_ = {
        'node': Parent(),
        'children': [{'node': Child(), 'children': []},
                     {'node': Child(), 'children': []}]}

    tree_['children'][0]['node'].deffacts(Fact(always_run=L(True)))

    # Parent does not inherit its children facts:
    tree_['children'][0]['node'].deffacts(Fact(not_inherited=L(True)))

    KETree(tree_).run_sequential()
    print(executions)
    assert len(executions) == 3


def test_tree_retract_matching():
    """
        Test tree not
    """

    from pyknow.tree import KETree
    from pyknow.engine import KnowledgeEngine
    from pyknow.rule import Rule, NOT
    from pyknow.fact import Fact, L

    executions = []
    global executions

    class Child(KnowledgeEngine):
        @Rule(Fact(always_run=L(True)))
        def always_run(self):
            executions.append(1)
            # pytest.set_trace()
            print(self.parent._facts._facts)
            ret = self.parent.retract_matching(Fact(initial=L(True)))
            print(ret)
            print(self.parent._facts._facts)
            # pytest.set_trace()
            self.parent.declare(Fact(inherited=L(True)))

    class Parent(KnowledgeEngine):
        @Rule(Fact(initial=L(True)))
        def shouldnot_run(self):
            # pytest.set_trace()
            print("Ran")
            executions.append(4)

        @Rule(Fact(inherited=L(True)))
        def inherited(self):
            executions.append(2)

        @Rule(NOT(Fact(not_inherited=L(True))))
        def not_inherited(self):
            executions.append(3)

    tree_ = {
        'node': Parent(),
        'children': [{'node': Child(), 'children': []},
                     {'node': Child(), 'children': []}]}

    tree_['node'].deffacts(Fact(initial=L(True)))

    tree_['children'][0]['node'].deffacts(Fact(always_run=L(True)))
    tree_['children'][0]['node'].deffacts(Fact(not_inherited=L(False)))

    KETree(tree_).run_sequential()
    print(executions)
    assert len(executions) == 3
