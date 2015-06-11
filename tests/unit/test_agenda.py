import pytest

from hypothesis import given
from hypothesis import strategies as st


def test_agenda_exists():
    try:
        from pyknow import agenda
    except ImportError as exc:
        assert False, exc
    else:
        assert True


def test_Agenda_exists():
    from pyknow import agenda

    assert hasattr(agenda, 'Agenda')


def test_Agenda_is_class():
    from pyknow.agenda import Agenda 

    assert isinstance(Agenda, type)


def test_Agenda_has_activations():
    from pyknow.agenda import Agenda

    assert hasattr(Agenda(), 'activations')


def test_Agenda_activations_is_deque():
    from pyknow.agenda import Agenda
    from collections import deque

    a = Agenda()

    assert type(a.activations) == deque


def test_Agenda_has_get_next_method():
    from pyknow.agenda import Agenda

    assert hasattr(Agenda, 'get_next')


def test_Agenda_get_next_returns_None_when_empty():
    from pyknow.agenda import Agenda

    a = Agenda()

    assert a.get_next() is None


def test_Agenda_get_next_returns_next_when_not_empty():
    from pyknow.agenda import Agenda

    a = Agenda()
    a.activations.append(True)

    assert a.get_next() is True
