from pyknow.fact import BaseField, Field


def test_basefield_interface():
    assert BaseField.__abstractmethods__ == {'validate'}


def test_field_validator_is_Schema():
    from schema import Schema

    f1 = Field(int)

    assert isinstance(f1.validator, Schema)


def test_field_default_is_NODEFAULT():
    f1 = Field(int)

    assert f1.default is Field.NODEFAULT
