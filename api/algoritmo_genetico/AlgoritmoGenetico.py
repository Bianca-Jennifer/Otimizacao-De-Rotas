import random
from api.classes.definicao_problema import DefinicaoProblema
import random


class AlgoritmoGenetico:
    def __init__(self, limite_geracoes: int, tamanho_populacao: int, definicao_problema: DefinicaoProblema):
        self.limite_geracoes = limite_geracoes
        self.tamanho_populacao = tamanho_populacao
        self.definicao_problema = definicao_problema


    def calcular_fitness(self,rota, rota_inviavel: bool):
        if rota_inviavel:
            return 999999
    

        distancia_total = 0   

        for i in range(len(rota) - 1):
            origem = rota[i]
            destino = rota[i + 1]

            distancia_total += self.definicao_problema.matriz_distancias[origem][destino] 

        quantidade_postos = 0
        for indice_local in rota:

            # Se estiver na área dos postos
            if indice_local >= self.definicao_problema.obter_indice_inicial_para_postos():
                quantidade_postos += 1

        PENALIDADE_POSTO = 10

        fitness = distancia_total + (quantidade_postos * PENALIDADE_POSTO)
            

        return fitness  
    


    def selecao_roleta(self,populacao):
       
        epsilon = 1e-9

        # transforma fitness em aptidão (quanto menor fitness, maior peso)
        aptidoes = [
            1 / (ind.fitness + epsilon)
            for ind in populacao
        ]

        soma_aptidoes = sum(aptidoes)

        # roleta acumulada
        acumulado = 0
        probabilidades = []

        for a in aptidoes:
            acumulado += a / soma_aptidoes
            probabilidades.append(acumulado)

        print(probabilidades)
        r = random.random()
        print(r)

        for i, p in enumerate(probabilidades):
            if r <= p:
                return i

        return len(populacao) - 1      


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
