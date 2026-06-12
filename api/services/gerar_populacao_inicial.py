import random
from api.classes.individuo import Individuo

def gerar_populacao_inicial(lugares, tamanho_populacao):
    indices_pontos = []
    
    for i in range(1, len(lugares)):
        if lugares[i].tipo == "Ponto": 
            indices_pontos.append(i)
            
    populacao = []
    
    for _ in range(tamanho_populacao):
        rota_embaralhada = indices_pontos.copy()
        random.shuffle(rota_embaralhada)
        
        novo_individuo = Individuo(
            rota_pontos_obrigatorios=rota_embaralhada,
            rota_completa=[],
            fitness=0.0
        )
        populacao.append(novo_individuo)
        
    return populacao