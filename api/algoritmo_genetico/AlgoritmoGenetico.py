import random
from api.classes.definicao_problema import DefinicaoProblema
from api.classes.individuo import Individuo

class AlgoritmoGeneticos:
    def __init__(self, limite_geracoes, tamanho_populacao, definicao_problema: DefinicaoProblema):
        self.limite_geracoes = limite_geracoes
        self.tamanho_populacao = tamanho_populacao
        self.definicao_problema = definicao_problema

    def crossover(self, pai1: Individuo, pai2: Individuo):
        tamanho = len(pai1.rota_pontos_obrigatorios)
        ponto1 = random.randint(0, tamanho - 2)
        ponto2 = random.randint(ponto1 + 1, tamanho - 1)
        
        trecho = pai1.rota_pontos_obrigatorios[ponto1:ponto2]
        restantes = [lugar for lugar in pai2.rota_pontos_obrigatorios if lugar not in trecho]
        
        rota_filho = restantes[:ponto1] + trecho + restantes[ponto1:]
        
        return Individuo(rota_filho, [], 0.0)
    
    def mutacao(self, individuo: Individuo, taxa_de_mutacao):
        tamanho = len(individuo.rota_pontos_obrigatorios)
        posicao1 = random.randint(0, tamanho - 1)
        posicao2 = random.randint(0, tamanho - 1)
        
        if random.random() < taxa_de_mutacao:
            
            temp = individuo.rota_pontos_obrigatorios[posicao1]
            individuo.rota_pontos_obrigatorios[posicao1] = individuo.rota_pontos_obrigatorios[posicao2]
            individuo.rota_pontos_obrigatorios[posicao2] = temp

        return individuo
