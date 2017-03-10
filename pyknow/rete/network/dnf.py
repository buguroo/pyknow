"""
Rewrite engine to get disjuntive normal form of the rules
"""

from itertools import chain, product
from pyknow.fact import Fact
from pyknow.rule import OR, NOT, AND


def _dnf_and(and_children):
    """
      - if node is AND:
        - combine AND children (conjunctions)
        - Combine OR children (disjunctions)
        - If we found disjunctions:
          - Consider the cartesian product of conjunctions and disjunctions
            a list of conjunctions, then return an OR node with the

          Return an OR node with the cartesian product of
          conjunctions and disjunctions
        - If we found no disjunctions:
          - Return the combined conjunctions
        - Return a OR node with the cartesian product of
          AND children and OR children
          - The cartesian product of AND and OR children should
            result in a list of ANDS if there are any conjunctions.
            Otherwise just return the combined OR.
    """
    # pylint: disable=protected-access
    dis = list(chain(*(list(a) for a in and_children if isinstance(a, OR))))
    ands = list(chain(*(list(a) for a in and_children if isinstance(a, AND))))
    facts = list((a for a in and_children if isinstance(a, Fact)))
    con = facts + ands
    if not dis:
        return AND(*con)
    else:
        return OR(*(AND(*a) for a in product(con, dis)))


def _dnf_not(not_child):
    """
    - De morgan's law to push negation nodes to the leaves.
      That is, if we've got a NOT(AND(a=1, b=1)) we should
      convert it to an AND(NOT(a=1), NOT(b=1))
      - Given:
        + The child is a NOT()
          - Return the child (NOT(NOT(a=1))) is equivalent to (a=1)
        + The child is AND():
          - Return OR() with (NOT() for each child)
        + The child is OR():
          - Return AND() with (NOT() for each child)
    """
    if isinstance(not_child, OR):
        return OR(*(NOT(cond) for cond in not_child))
    elif isinstance(not_child, AND):
        return AND(*(NOT(cond) for cond in not_child))
    elif isinstance(not_child, NOT):
        if len(not_child) != 1:
            raise Exception("Found a not with multiple child")
        return not_child[0]


def _dnf_or(cond):
    """
    Merge ORs, return the rest untouched.
    """
    dis = chain(*(list(a) for a in cond if isinstance(a, OR)))
    rest = (a for a in cond if not isinstance(a, OR))
    return OR(*list(rest) + list(dis))


def _dnf_single(cond):
    """
    If we have only one child, we can dispose of its container.
    """
    return cond[0]


def dnf(cond):
    """
    Get the disjunctive normal form of a Rule
    """

    if isinstance(cond, OR) or isinstance(cond, AND):
        if len(cond) == 1:
            return _dnf_single(cond)
    if isinstance(cond, AND):
        return _dnf_and([dnf(a) for a in cond])
    elif isinstance(cond, NOT):
        if len(cond) != 1:
            raise Exception("Found a not with multiple children")
        return _dnf_not(dnf(list(cond)[0]))
    elif isinstance(cond, OR):
        return _dnf_or([dnf(a) for a in cond])
    elif isinstance(cond, Fact):
        return cond
