from api.classes.definicao_problema import DefinicaoProblema
from api.classes.lugar import Lugar


class AlgoritmoGeneticoFake:
    def __init__(self, definicao_problema):
        self.definicao_problema = definicao_problema

    def calcular_fitness(self, rota, rota_inviavel: bool):

        if rota_inviavel:
            return 999999

        distancia_total = 0

        for i in range(len(rota) - 1):
            origem = rota[i]
            destino = rota[i + 1]

            distancia_total += self.definicao_problema.matriz_distancias[origem][destino]

        quantidade_postos = 0

        for indice_local in rota:

            if indice_local >= self.definicao_problema.obter_indice_inicial_para_postos():
                quantidade_postos += 1

        PENALIDADE_POSTO = 10

        fitness = distancia_total + (quantidade_postos * PENALIDADE_POSTO)

        return fitness


def test_calcular_fitness():

    lugares = [
        Lugar("Ponto A", -5.1, -35.1, "Ponto"),   # índice 0
        Lugar("Ponto B", -5.2, -35.2, "Ponto"),   # índice 1
        Lugar("Posto X", -5.3, -35.3, "Posto"),   # índice 2
        Lugar("Posto Y", -5.4, -35.4, "Posto")    # índice 3
    ]

    matriz_distancias = [
        [0, 10, 20, 30],
        [10, 0, 15, 25],
        [20, 15, 0, 12],
        [30, 25, 12, 0]
    ]

    problema = DefinicaoProblema(
        lugares=lugares,
        matriz_distancias=matriz_distancias
    )

    ag = AlgoritmoGeneticoFake(problema)

    rota = [0, 1, 2, 3]

    fitness = ag.calcular_fitness(
        rota=rota,
        rota_inviavel=False
    )

    # Distâncias:
    # 0 -> 1 = 10
    # 1 -> 2 = 15
    # 2 -> 3 = 12
    # Total = 37
    #
    # Postos:
    # índices 2 e 3 = 2 postos
    # penalidade = 2 * 10 = 20
    #
    # fitness = 37 + 20 = 57

    assert fitness == 57


def test_calcular_fitness_rota_inviavel():

    problema = DefinicaoProblema([])

    ag = AlgoritmoGeneticoFake(problema)

    fitness = ag.calcular_fitness(
        rota=[0, 1],
        rota_inviavel=True
    )

    assert fitness == 999999