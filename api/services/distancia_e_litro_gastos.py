def calcular_distancia_total(individuo, problema):
    total = 0

    rota = individuo.rota_completa
    matriz = problema.matriz_distancias

    for i in range(len(rota) - 1):
        origem = rota[i]
        destino = rota[i + 1]

        total += matriz[origem][destino]

    return total

def calcular_litros_gastos(distancia_km, problema):

    consumo = problema.veiculo.consumo_medio  # km/L

    litros = distancia_km / consumo

    return litros

def converter_matriz_m_para_km(matriz):
    return [
        [valor / 1000 for valor in linha]
        for linha in matriz
    ]    