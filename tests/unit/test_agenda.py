"""
Tests related to the agenda object
"""


def test_agenda_has_activations():
    """ Agenda object has activations property """

    from pyknow.agenda import Agenda
    from collections import deque
    assert hasattr(Agenda(), "activations")
    assert isinstance(Agenda().activations, deque)


def test_agenda_has_executed_set():
    """ Agenda object has executed property """

    from pyknow.agenda import Agenda
    assert hasattr(Agenda(), "executed")
    assert isinstance(Agenda().executed, set)


def test_agenda_get_next():
    """
    Agenda has a get_next method that gets from activations and inserts
    into executed
    """

    from pyknow.agenda import Agenda
    agenda = Agenda()
    assert not agenda.executed
    agenda.activations.append("Foo")
    assert agenda.get_next() == "Foo"
    assert agenda.executed == set(["Foo"])
