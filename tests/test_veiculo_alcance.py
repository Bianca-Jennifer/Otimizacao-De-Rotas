from api.classes.veiculo import Veiculo

def test_alcance_atual():
    veiculo = Veiculo(
        consumo_medio=10,   
        capacidade_tanque=50,
        combustivel_atual=20,
        tipo="moto"
    )

    resultado = veiculo.obter_alcance_atual()

    assert resultado == 200