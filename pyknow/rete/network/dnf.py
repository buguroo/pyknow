"""
Rewrite engine to get disjuntive normal form of the rules
"""
from collections import OrderedDict
from functools import singledispatch
from itertools import chain, product

from pyknow.rule import AND, OR, NOT, Rule, ORPCE, NOTPCE, ANDPCE
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

    return Rule(*unpack_exp(current, AND))


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


@dnf.register(Fact)
def _(exp):
    fact_class = exp.__class__
    if any(isinstance(v, ORPCE) for v in exp.values()):
        and_part = OrderedDict()
        or_part = OrderedDict()
        for k, v in exp.items():
            if isinstance(v, ORPCE):
                or_part[k] = v
                and_part[k] = None
            else:
                and_part[k] = v

        facts = []
        for p in product(*or_part.values()):
            current_or = OrderedDict(zip(or_part.keys(), p))
            ces = [(k, dnf(v)) if v is not None else (k, dnf(current_or[k]))
                   for k, v in and_part.items()]
            facts.append(fact_class.from_iter(ces))

        return OR(*facts)
    else:
        return fact_class.from_iter(((k, dnf(v)) for k, v in exp.items()))


@dnf.register(NOTPCE)
def _(exp):
    if isinstance(exp[0], NOTPCE):  # Double negation
        return dnf(exp[0][0])
    elif isinstance(exp[0], ORPCE):  # De Morgan's law (ORPCE)
        return ANDPCE(*[NOTPCE(dnf(x)) for x in exp[0]])
    elif isinstance(exp[0], ANDPCE):  # De Morgan's law (ANDPCE)
        return ORPCE(*[NOTPCE(dnf(x)) for x in exp[0]])
    else:  # `exp` is already dnf. We have nothing to do.
        return exp
