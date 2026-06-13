from api.classes.veiculo import Veiculo
from api.classes.definicao_problema import DefinicaoProblema
from api.algoritmo_genetico.AlgoritmoGenetico import AlgoritmoGenetico
from api.cliente_distancia.cliente_distancia import gerar_matriz_de_distancias
from api.services.leitor_de_arquivo import ler_arquivo_de_lugares

def processar(dados_frontend, conteudo_csv):
    tamanho_populacao = dados_frontend.tamanhoPopulacao
    limite_geracoes = dados_frontend.limiteGeracoes
    dados_veiculo = dados_frontend.veiculo

    lista_lugares = ler_arquivo_de_lugares(conteudo_csv)

    matriz_distancias = gerar_matriz_de_distancias(lista_lugares)

    veiculo = Veiculo(
        consumo_medio =dados_veiculo.consumoMedio,
        capacidade_tanque = dados_veiculo.capacidadeTanque,
        combustivel_atual = dados_veiculo.combustivelAtual,
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

    

    return algoritmo_genetico