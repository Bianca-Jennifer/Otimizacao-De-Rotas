import random
from api.classes.definicao_problema import DefinicaoProblema
import random
from api.classes.individuo import Individuo
from api.services.rotas_postos import criar_rota_com_postos3
from api.classes.lugar import Lugar


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

        
        r = random.random()

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
    
    def executar_algoritmo(self, populacao_inicial, tipo_selecao="torneio", usar_mutacao=True, taxa_mutacao=0.1, usar_elitismo=True, quantidade_elite=1, tamanho_torneio=3):
        populacao_atual = []

        # =========================================
        # CALCULA FITNESS DA POPULAÇÃO INICIAL
        # =========================================

        for individuo in populacao_inicial:

            rota_completa, rota_inviavel = (
                criar_rota_com_postos3(
                    self.definicao_problema,
                    individuo.rota_pontos_obrigatorios
                )
            )

            individuo.rota_completa = (
                rota_completa
            )

            individuo.fitness = (
                self.calcular_fitness(
                    rota_completa,
                    rota_inviavel
                )
            )

            populacao_atual.append(
                individuo
            )

        # =========================================
        # MELHOR GLOBAL
        # =========================================

        melhor_global = (
            self.obter_melhor_individuo(
                populacao_atual
            )
        )

        # =========================================
        # LOOP DAS GERAÇÕES
        # =========================================

        for geracao in range(
            self.limite_geracoes
        ):

            nova_populacao = []

            # =====================================
            # ELITISMO
            # =====================================

            if usar_elitismo:

                melhor_individuo = (
                    self.obter_melhor_individuo(
                        populacao_atual
                    )
                )

                nova_populacao.append(
                    melhor_individuo
                )

            # =====================================
            # CRIA NOVA POPULAÇÃO
            # =====================================

            while (
                len(nova_populacao)
                < self.tamanho_populacao
            ):

                # =================================
                # SELEÇÃO
                # =================================

                if tipo_selecao == "torneio":

                    pai1 = self.torneio(
                        populacao_atual,
                        tamanho_torneio
                    )

                    pai2 = self.torneio(
                        populacao_atual,
                        tamanho_torneio
                    )

                elif tipo_selecao == "roleta":

                    indice1 = (
                        self.selecao_roleta(
                            populacao_atual
                        )
                    )

                    indice2 = (
                        self.selecao_roleta(
                            populacao_atual
                        )
                    )

                    pai1 = (
                        populacao_atual[
                            indice1
                        ]
                    )

                    pai2 = (
                        populacao_atual[
                            indice2
                        ]
                    )

                else:

                    raise ValueError(
                        "Tipo de seleção inválido"
                    )

                # =================================
                # CROSSOVER
                # =================================

                filho = self.crossover(
                    pai1,
                    pai2
                )
                print("o filho antes:" + str(filho.rota_pontos_obrigatorios))

                # =================================
                # MUTAÇÃO
                # =================================

                if usar_mutacao:

                    filho = self.mutacao(
                        filho,
                        taxa_mutacao
                    )
                print("filho dps")    
                print(filho.rota_pontos_obrigatorios)    

                # =================================
                # CRIA ROTA COMPLETA
                # =================================

                rota_completa, rota_inviavel = (
                    criar_rota_com_postos3(
                        self.definicao_problema,
                        filho.rota_pontos_obrigatorios
                    )
                )

                filho.rota_completa = (
                    rota_completa
                )

                # =================================
                # FITNESS
                # =================================

                filho.fitness = (
                    self.calcular_fitness(
                        rota_completa,
                        rota_inviavel
                    )
                )

                nova_populacao.append(
                    filho
                )

            # =====================================
            # ATUALIZA POPULAÇÃO
            # =====================================

            populacao_atual = (
                nova_populacao
            )

            print("\nPOPULAÇÃO ATUAL")

            for i, individuo in enumerate(
                populacao_atual
            ):

                print(
                    f"Indivíduo {i}"
                )

                print(
                    "Rota obrigatória:",
                    individuo.rota_pontos_obrigatorios
                )

                print(
                    "Rota completa:",
                    individuo.rota_completa
                )

                print(
                    "Fitness:",
                    individuo.fitness
                )

                print("--------")

            # =====================================
            # MELHOR DA GERAÇÃO
            # =====================================

            melhor_geracao = (
                self.obter_melhor_individuo(
                    populacao_atual
                )
            )

            # =====================================
            # ATUALIZA MELHOR GLOBAL
            # =====================================

            if (
                melhor_geracao.fitness <
                melhor_global.fitness
            ):

                melhor_global = (
                    melhor_geracao
                )

            # =====================================
            # DEBUG
            # =====================================

            print(
                f"\nGeração {geracao}"
            )

            print(
                "Melhor da geração:"
            )

            print(
                "Fitness:",
                melhor_geracao.fitness
            )

            print(
                "Rota:",
                melhor_geracao.rota_completa
            )

            print()

            print(
                "Melhor global:"
            )

            print(
                "Fitness:",
                melhor_global.fitness
            )

            print(
                "Rota:",
                melhor_global.rota_completa
            )

            print(
                "--------------------------------"
            )

        return melhor_global

if __name__ == "__main__":

    from api.classes.veiculo import Veiculo
    from api.classes.definicao_problema import (
        DefinicaoProblema
    )

    # =====================================
    # MATRIZ DE DISTÂNCIAS
    # =====================================

    matriz = [
        [0, 10, 15, 20, 8],
        [10, 0, 35, 25, 12],
        [15, 35, 0, 30, 14],
        [20, 25, 30, 0, 18],
        [8, 12, 14, 18, 0]
    ]

    # =====================================
    # LUGARES
    # =====================================

    lugares = [

    Lugar(
        "A",
        -5.0,
        -35.0,
        "Destino"
    ),

    Lugar(
        "B",
        -5.1,
        -35.1,
        "Destino"
    ),

    Lugar(
        "C",
        -5.2,
        -35.2,
        "Destino"
    ),

    Lugar(
        "D",
        -5.3,
        -35.3,
        "Destino"
    ),

    Lugar(
        "POSTO",
        -5.4,
        -35.4,
        "Posto"
    )
]

    # =====================================
    # VEÍCULO
    # =====================================

    veiculo = Veiculo(
        consumo_medio=10,
        capacidade_tanque=4,
        combustivel_atual=4,
        tipo="carro"
    )
    print(veiculo.obter_autonomia())
    print(veiculo.obter_alcance_atual())
    print("--------")

    # =====================================
    # DEFINIÇÃO DO PROBLEMA
    # =====================================

    definicao = DefinicaoProblema(
        lugares,
        matriz,
        veiculo
    )

    # =====================================
    # POPULAÇÃO INICIAL
    # =====================================

    populacao = [

        Individuo(
            [0, 1, 2, 3],
            [],
            0
        ),

        Individuo(
            [1, 0, 3, 2],
            [],
            0
        ),

        Individuo(
            [3, 1, 0, 2],
            [],
            0
        ),

        Individuo(
            [1, 3, 2, 0],
            [],
            0
        )
    ]

    # =====================================
    # ALGORITMO
    # =====================================

    alg = AlgoritmoGenetico(
        limite_geracoes=10,
        tamanho_populacao=4,
        definicao_problema=definicao
    )

    # =====================================
    # EXECUÇÃO
    # =====================================

    melhor = alg.executar_algoritmo(
        populacao_inicial=populacao,
        tipo_selecao="torneio",
        usar_mutacao=True,
        taxa_mutacao=1.0,
        usar_elitismo=False,
        tamanho_torneio=2
    )

    # =====================================
    # RESULTADO FINAL
    # =====================================

    print("\nRESULTADO FINAL")

    print(
        "Melhor rota obrigatória:",
        melhor.rota_pontos_obrigatorios
    )

    print(
        "Melhor rota completa:",
        melhor.rota_completa
    )

    print(
        "Fitness:",
        melhor.fitness
    )