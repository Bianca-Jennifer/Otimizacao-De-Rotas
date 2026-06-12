from api.classes.veiculo import Veiculo
from api.classes.definicao_problema import DefinicaoProblema
from api.algoritmo_genetico.AlgoritmoGenetico import AlgoritmoGenetico
from api.services.gerar_populacao_inicial import gerar_populacao_inicial
from api.cliente_distancia.cliente_distancia import gerar_matriz_de_distancias
from api.services.leitor_de_arquivo import ler_arquivo_de_lugares

def processar(dados_frontend):
    tamanho_populacao = dados_frontend.tamanho_populacao
    limite_geracoes = dados_frontend.limite_geracoes
    dados_veiculo = dados_frontend.veiculo

    lista_lugares = ler_arquivo_de_lugares()

    matriz_distancias = gerar_matriz_de_distancias(lista_lugares)

    veiculo = Veiculo(
        consumo_medio =dados_veiculo.consumo_medio,
        capacidade_tanque = dados_veiculo.capacidade_tanque,
        combustivel_atual = dados_veiculo.combustivel_atual,
        tipo = dados_veiculo.tipo
    )

    definicao_problema = DefinicaoProblema(
        lugares = lista_lugares,
        matriz_distancias = matriz_distancias,
        veiculo = veiculo
    )

    algoritmo_genetico = AlgoritmoGenetico(
        limite_geracoes = limite_geracoes,
        tamanho_populacao = tamanho_populacao,
        definicao_problema = definicao_problema,
    )

    populacao_inicial = gerar_populacao_inicial(lista_lugares, tamanho_populacao)

    return algoritmo_genetico, populacao_inicial