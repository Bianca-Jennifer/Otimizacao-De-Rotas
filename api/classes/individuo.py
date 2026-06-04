class Individuo:
    def __init__(self, rota_pontos_obrigatorios: list, rota_completa: list, fitness):
        self.rota_pontos_obrigatorios = rota_pontos_obrigatorios
        self.rota_completa = rota_completa
        self.fitness = fitness