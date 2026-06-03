from api.classes.veiculo import Veiculo

class DefinicaoProblema:
    def __init__(self, lugares: list, matriz_distancias, veiculo: Veiculo):
        self.lugares = lugares
        self.matriz_distancias = matriz_distancias
        self.veiculo = veiculo

    def obter_distancia(self, origem, destino):
        return

    def obter_lugares(self):
        return self.lugares

    def obter_pontos_obrigatorios(self):
        return 

    def obter_postos(self):
        return 