from api.classes.veiculo import Veiculo
from api.classes.lugar import Lugar

class DefinicaoProblema:
    def __init__(self, lugares: list, matriz_distancias=None, veiculo: Veiculo=None):
        self.lugares = lugares
        self.matriz_distancias = matriz_distancias
        self.veiculo = veiculo

    def obter_distancia(self, origem, destino):
        return

    def obter_lugares(self):
        return self.lugares

    def obter_pontos_obrigatorios(self):
        return 

    def obter_indice_inicial_para_postos(self):
        for cont, lugar in enumerate(self.lugares):
            if lugar.tipo == "Posto":
                return cont
        return len(self.lugares)    

    def rota_completa_com_lugares(self, rota_completa):
        rota = []

        for indice in rota_completa:
            lugar = self.lugares[indice]

            rota.append({
                "nome": lugar.nome,
                "lat": lugar.latitude,
                "long": lugar.longitude,
                "tipo": lugar.tipo
            })

        return rota