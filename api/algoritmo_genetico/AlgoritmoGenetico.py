from api.classes.definicao_problema import DefinicaoProblema

class AlgoritmoGeneticos:
    def __init__(self, limite_geracoes, tamanho_populacao, definicao_problema: DefinicaoProblema):
        self.limite_geracoes = limite_geracoes
        self.tamanho_populacao = tamanho_populacao
        self.definicao_problema = definicao_problema