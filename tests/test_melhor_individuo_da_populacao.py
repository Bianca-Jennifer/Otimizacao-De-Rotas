class IndividuoFake:
    def __init__(self, fitness):
        self.fitness = fitness


class AlgoritmoGeneticoFake:

    def obter_melhor_individuo(self, populacao_atual):

        if not populacao_atual:
            return None

        melhor_individuo = populacao_atual[0]

        for individuo in populacao_atual[1:]:

            if individuo.fitness < melhor_individuo.fitness:
                melhor_individuo = individuo

        return melhor_individuo


def test_obter_melhor_individuo():

    populacao = [
        IndividuoFake(fitness=120),
        IndividuoFake(fitness=80),
        IndividuoFake(fitness=200),
        IndividuoFake(fitness=50),
        IndividuoFake(fitness=90)
    ]

    ag = AlgoritmoGeneticoFake()

    melhor = ag.obter_melhor_individuo(populacao)

    assert melhor.fitness == 50


def test_obter_melhor_individuo_populacao_vazia():

    ag = AlgoritmoGeneticoFake()

    melhor = ag.obter_melhor_individuo([])

    assert melhor is None