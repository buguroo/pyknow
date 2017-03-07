import pytest


@pytest.mark.wip
def test_alpha_normalization_rule_two():
    """
    Given an already normalized (two elements) network,
    the result should be the same
    """
    from pyknow.rete.alpha import EngineWalker
    from pyknow.rule import Rule
    from pyknow.fact import Fact

    rule_ = Rule(Fact(a=1), Fact(a=1))
    branch = EngineWalker.normalize_tree(rule_, Rule)

    assert branch == rule_


@pytest.mark.wip
def test_alpha_normalization_rule_three():
    r"""
    Given a not-normalized 3-nodes network,
    check the following results:

    Rule
      |-> Node1
      |-> Node2
      \-> Node3

    Rule
      |-> Node3
      \-> Rule
          |-> Node2
          \-> Node1
    """
    from pyknow.rete.alpha import EngineWalker
    from pyknow.rule import Rule
    from pyknow.fact import Fact

    rule_ = Rule(Fact(a=1), Fact(a=2), Fact(a=3))
    rule_result = Rule(Fact(a=3), Rule(Fact(a=2), Fact(a=1)))
    branch = EngineWalker.normalize_tree(rule_, Rule)

    assert branch == rule_result


@pytest.mark.wip
def test_alpha_normalization_rule_one():
    r"""
    Given a single node, the node should remain
    the same
    """
    from pyknow.rete.alpha import EngineWalker
    from pyknow.rule import Rule
    from pyknow.fact import Fact

    rule_ = Rule(Fact(a=1))
    branch = EngineWalker.normalize_tree(rule_, Rule)

    assert branch == rule_
