import random
from api.classes.definicao_problema import DefinicaoProblema

class AlgoritmoGeneticos:
    def __init__(self, limite_geracoes, tamanho_populacao, definicao_problema: DefinicaoProblema):
        self.limite_geracoes = limite_geracoes
        self.tamanho_populacao = tamanho_populacao
        self.definicao_problema = definicao_problema

    def obter_melhor_individuo(self, populacao_atual):
        if not populacao_atual:
            return None
        
        melhor_individuo = populacao_atual[0]
        
        for individuo in populacao_atual[1:]:
            if individuo.fitness < melhor_individuo.fitness:
                melhor_individuo = individuo

        return melhor_individuo
    
    def torneio(self, populacao, tamanho_torneio):
        participantes = random.sample(populacao, tamanho_torneio)
        melhor_participante = min(participantes, key=lambda individuo: individuo.fitness)
        return melhor_participante