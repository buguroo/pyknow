import pytest

@pytest.mark.wip
def test_engine_import():
    try:
        from pyknow import engine
    except ImportError as exc:
        assert False, exc
    else:
        assert True


@pytest.mark.wip
def test_KnowledgeEngine_exists():
    from pyknow import engine
    assert hasattr(engine, 'KnowledgeEngine')


@pytest.mark.wip
def test_KnowledgeEngine_is_class():
    from pyknow import engine
    assert isinstance(engine.KnowledgeEngine, type)


@pytest.mark.wip
def test_KnowledgeEngine_has__facts():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, '_facts')


@pytest.mark.wip
def test_KnowledgeEngine_has_asrt():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    assert hasattr(ke, 'asrt')

@pytest.mark.wip
def test_KnowledgeEngine_asrt_define_fact():
    from pyknow.engine import KnowledgeEngine
    ke = KnowledgeEngine()
    ke.asrt('test', True)
    assert ke._facts['test'] is True

@pytest.mark.wip
def test_KnowledgeEngine_asrt_cant_define_twice():
    from pyknow.engine import KnowledgeEngine, DuplicatedFactError

    ke = KnowledgeEngine()
    ke.asrt('test', True)

    with pytest.raises(DuplicatedFactError):
        ke.asrt('test', True)


@pytest.mark.wip
def test_KnowledgeEngine_getitem_asserted():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()

    ke.asrt('NAME', 'VALUE')

    assert ke['NAME'] == 'VALUE'


@pytest.mark.wip
def test_KnowledgeEngine_getitem_not_asserted():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()

    with pytest.raises(KeyError):
        ke['NAME']

@pytest.mark.wip
def test_KnowledgeEngine_getitem_DynamicFact():
    from pyknow import fact
    from pyknow.engine import KnowledgeEngine

    class Test(KnowledgeEngine):
        @fact
        def my_fact(self):
            return 'FACT'

    ke = Test()

    assert ke['my_fact'] == 'FACT'

@pytest.mark.wip
def test_KnowledgeEngine_DynamicFact_cant_asrt():
    from pyknow import fact
    from pyknow.engine import KnowledgeEngine, DuplicatedFactError

    class Test(KnowledgeEngine):
        @fact
        def my_fact(self):
            return 'FACT'

    ke = Test()
    with pytest.raises(DuplicatedFactError):
        ke.asrt('my_fact', 'SOMETHING')

@pytest.mark.wip
def test_KnowledgeEngine__contains__True():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()
    ke.asrt('name', 'value')

    assert 'name' in ke

@pytest.mark.wip
def test_KnowledgeEngine__contains__False():
    from pyknow.engine import KnowledgeEngine

    ke = KnowledgeEngine()

    assert 'name' not in ke

@pytest.mark.wip
def test_KnowledgeEngine_DynamicFact_if_defined__True():
    from pyknow import fact
    from pyknow.engine import KnowledgeEngine

    class Test(KnowledgeEngine):
        @fact(if_defined='other_fact')
        def my_fact(self):
            return 'FACT'

    ke = Test()
    ke.asrt('other_fact', 'SOMETHING')

    assert ke['my_fact'] == 'FACT'

@pytest.mark.wip
def test_KnowledgeEngine_DynamicFact_if_defined__False():
    from pyknow import fact
    from pyknow.engine import KnowledgeEngine

    class Test(KnowledgeEngine):
        @fact(if_defined='other_fact')
        def my_fact(self):
            return 'FACT'

    ke = Test()

    with pytest.raises(KeyError):
        assert ke['my_fact']
