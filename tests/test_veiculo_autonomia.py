from api.classes.veiculo import Veiculo

def test_autonomia():
    v = Veiculo(10, 50, 5, "moto")

    assert v.obter_autonomia() == 500