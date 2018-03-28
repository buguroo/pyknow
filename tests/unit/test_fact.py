import pytest

from pyknow.fact import Fact
from pyknow.engine import KnowledgeEngine


def test_fact_mix_positional_and_kw_index():
    f = Fact('x', 'y', 'z', a=1, b=2)

    assert f[0] == 'x'
    assert f[1] == 'y'
    assert f[2] == 'z'
    assert f['a'] == 1
    assert f['b'] == 2


def test_fact_freeze_mutable_values():
    f = Fact([1, 2, 3])
    assert f[0] == (1, 2, 3)


def test_fact_setitem_does_not_raise_before_declare():
    f = Fact()
    f[0] = 1

    assert f[0] == 1


def test_fact_setitem_do_raise_after_declare():
    f = Fact()
    ke = KnowledgeEngine()
    ke.reset()
    ke.declare(f)

    with pytest.raises(RuntimeError):
        f[0] = 1


def test_double_underscore_raise_on_declare():
    ke = KnowledgeEngine()
    ke.reset()

    ke.declare(Fact(__startwithdoubleunderscore__=True))

    with pytest.raises(KeyError):
        ke.declare(Fact(key__with__double__underscores=True))
