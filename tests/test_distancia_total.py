
from api.services.distancia_e_litro_gastos import calcular_distancia_total

class MockProblema:
    def __init__(self):
        self.matriz_distancias = [
            [0, 10, 20],
            [10, 0, 30],
            [20, 30, 0]
        ]

class MockIndividuo:
    def __init__(self):
        self.rota_completa = [0, 1, 2, 0]

def test_distancia_total():
    problema = MockProblema()
    individuo = MockIndividuo()

    resultado = calcular_distancia_total(individuo, problema)

    assert resultado == 60