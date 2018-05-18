from unittest.mock import MagicMock

import pytest

from pyknow.fact import Fact, Field
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


def test_fields_got_registered_in_fact():

    class MockFact(Fact):
        myfield = Field(int)
        somethingelse = int

    f1 = MockFact()

    assert "myfield" in f1.__fields__
    assert "somethingelse" not in f1.__fields__


def test_field_with_default_returns_default_value():

    class MockFact(Fact):
        myfield = Field(int, default=0)

    f1 = MockFact()

    assert f1["myfield"] == 0


def test_field_with_default_calls_it_if_its_callable():

    class MockFact(Fact):
        myfield = Field(int, default=lambda: 0)

    f1 = MockFact()

    assert f1["myfield"] == 0


def test_validate_returns_none_on_validation_success():

    class MockFact(Fact):
        myfield = Field(int)

    f1 = MockFact(myfield=0)

    assert f1.validate() is None


def test_validate_raise_valueerror_on_validation_error():

    class MockFact(Fact):
        myfield = Field(int)

    f1 = MockFact(myfield="A")

    with pytest.raises(ValueError):
        f1.validate()


def test_validate_raise_valueerror_on_missing_field():

    class MockFact(Fact):
        myfield = Field(int, mandatory=True)

    f1 = MockFact()

    with pytest.raises(ValueError):
        f1.validate()


def test_fields_are_not_present_in_class():
    class MockFact(Fact):
        myfield = Field(int)

    assert not hasattr(MockFact, 'myfield')


def test_fields_are_not_present_in_instance():
    class MockFact(Fact):
        myfield = Field(int)

    obj = MockFact()

    assert not hasattr(obj, 'myfield')


def test_fields_are_inherited():
    class MockFactBase(Fact):
        mybasefield = Field(str, default="base")

    class MockFact(MockFactBase):
        myfield = Field(str, default="class")

    obj = MockFact()
    assert obj["myfield"] == "class"
    assert obj["mybasefield"] == "base"


def test_inherited_fields_can_be_overwritten():
    class MockFactBase(Fact):
        mybasefield = Field(str, default="base")

    class MockFact(MockFactBase):
        mybasefield = Field(str, default="notbase")
        myfield = Field(str, default="class")

    obj = MockFact()
    assert obj["myfield"] == "class"
    assert obj["mybasefield"] == "notbase"


def test_fields_default_are_called_once_per_instance():
    mymock = MagicMock(return_value="TEST")

    class MockFact(Fact):
        myfield = Field(str, default=mymock)

    mymock.assert_not_called()

    f1 = MockFact()
    assert mymock.call_count == 0
    assert f1["myfield"] == "TEST"
    assert mymock.call_count == 1
    f1["myfield"]
    assert mymock.call_count == 1

    f2 = MockFact()
    assert f2["myfield"] == "TEST"
    assert mymock.call_count == 2
