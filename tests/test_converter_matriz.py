

from api.services.distancia_e_litro_gastos import converter_matriz_m_para_km

def test_conversao_matriz_para_km():
    matriz = [
        [1000, 2000],
        [3000, 4000]
    ]

    resultado = converter_matriz_m_para_km(matriz)

    assert resultado == [
        [1.0, 2.0],
        [3.0, 4.0]
    ]