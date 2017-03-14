"""
Rewrite engine to get disjuntive normal form of the rules
"""
from functools import singledispatch
from itertools import chain

from pyknow.rule import AND, OR, NOT, Rule
from pyknow.fact import Fact


def unpack_exp(exp, op):
    for x in exp:
        if isinstance(x, op):
            yield from x
        else:
            yield x


@singledispatch
def dnf(exp):
    return exp


@dnf.register(Rule)
def _(exp):
    last, current = None, Rule(*[dnf(e) for e in exp])

    while last != current:
        last, current = current, Rule(*[dnf(e) for e in current])

    return current


@dnf.register(NOT)
def _(exp):
    if isinstance(exp[0], NOT):  # Double negation
        return dnf(exp[0][0])
    elif isinstance(exp[0], OR):  # De Morgan's law (OR)
        return AND(*[NOT(dnf(x)) for x in exp[0]])
    elif isinstance(exp[0], AND):  # De Morgan's law (AND)
        return OR(*[NOT(dnf(x)) for x in exp[0]])
    else:  # `exp` is already dnf. We have nothing to do.
        return exp


@dnf.register(OR)
def _(exp):
    if len(exp) == 1:
        return dnf(exp[0])
    else:
        return OR(*[dnf(x) for x in unpack_exp(exp, OR)])


@dnf.register(AND)
def _(exp):
    if len(exp) == 1:
        return dnf(exp[0])
    elif any(isinstance(e, OR) for e in exp):  # Distributive property
        and_part = []
        or_part = []
        for e in exp:
            if isinstance(e, OR):
                or_part.extend(e)
            else:
                and_part.append(e)
        return OR(*[dnf(AND(*(and_part + [dnf(e)]))) for e in or_part])
    else:
        return AND(*[dnf(x) for x in unpack_exp(exp, AND)])
