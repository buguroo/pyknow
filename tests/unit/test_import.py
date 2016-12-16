def test_import():
    try:
        import pyknow
    except ImportError as exc:
        assert False, exc
    else:
        assert True
