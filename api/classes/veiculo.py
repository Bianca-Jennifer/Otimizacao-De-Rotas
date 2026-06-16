class Veiculo:
    def __init__(self, consumo_medio, capacidade_tanque, combustivel_atual, tipo):
        self.consumo_medio = consumo_medio
        self.capacidade_tanque = capacidade_tanque
        self.combustivel_atual = combustivel_atual
        self.tipo = tipo

    def obter_autonomia(self):
        return self.consumo_medio * self.capacidade_tanque
    
    def obter_alcance_atual(self):
        return self.combustivel_atual * self.consumo_medio