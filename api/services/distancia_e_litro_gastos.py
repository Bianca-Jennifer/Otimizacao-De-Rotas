def calcular_distancia_total(individuo, problema):
    total = 0

    rota = individuo.rota_completa
    matriz = problema.matriz_distancias

    for i in range(len(rota) - 1):
        origem = rota[i]
        destino = rota[i + 1]

        total += matriz[origem][destino]

    return total

def calcular_litros_gastos(distancia_metros, problema):

    consumo = problema.veiculo.consumo_medio

    distancia_km = distancia_metros / 1000
    litros = distancia_km / consumo

    return litros    