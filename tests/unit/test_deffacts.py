import pytest


def test_deffacts_module_exists():
    try:
        from pyknow import deffacts
    except ImportError as exc:
        assert False, exc


def test_deffacts_class_exists():
    from pyknow import deffacts

    assert hasattr(deffacts, 'DefFacts')


def test_deffacts_can_decorate_generator():
    from pyknow import DefFacts, Fact

    @DefFacts()
    def mygenerator():
        yield Fact()

    assert list(mygenerator()) == [Fact()]


def test_deffacts_return_copies_of_facts():
    from pyknow import DefFacts, Fact

    f0 = Fact()

    @DefFacts()
    def mygenerator():
        yield f0

    assert list(mygenerator())[0] is not f0


def test_deffacts_stores_order():
    from pyknow import DefFacts, Fact

    @DefFacts(order=-10)
    def mygenerator():
        yield Fact()

    assert mygenerator.order == -10


def test_deffacts_does_not_accept_non_generators():
    from pyknow import DefFacts, Fact

    with pytest.raises(TypeError):
        @DefFacts()
        def mygenerator():
            return Fact()


def test_deffacts_can_decorate_methods():
    from pyknow import DefFacts, Fact

    class Test:
        @DefFacts()
        def mygenerator(self):
            yield Fact()

    t = Test()
    assert list(t.mygenerator()) == [Fact()]


def test_deffacts_without_parenthesis():
    from pyknow import DefFacts

    with pytest.raises(SyntaxError):
        @DefFacts
        def mygenerator(self):
            yield Fact()
