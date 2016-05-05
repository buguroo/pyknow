def test_basic_ce():
    from pyknow.rule import Rule
    from pyknow.factlist import FactList
    from pyknow.fact import Fact, L, T

    r = Rule(Fact(name=T(lambda x: x.startswith('D'))))
    fl = FactList()

    fl.declare(Fact(name=L("David")))
    fl.declare(Fact(name=L("Penelope")))
    fl.declare(Fact(name=L("Daniel")))

    activations = r.get_activations(fl)
    assert len(activations) == 2
