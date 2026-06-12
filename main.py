import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from api.algoritmo_genetico.AlgoritmoGenetico import AlgoritmoGenetico
from api.classes.individuo import Individuo
from api.classes.definicao_problema import DefinicaoProblema
from api.classes.veiculo import Veiculo
from api.classes.lugar import Lugar

app = FastAPI(
    title="API - Otimização de Rotas com Algoritmo Genético",
    description="Calcula a melhor rota considerando postos de combustível e limites do veículo."
)

class LugarInput(BaseModel):
    nome: str
    latitude: float
    longitude: float
    tipo: str

class VeiculoInput(BaseModel):
    consumo_medio: float
    capacidade_tanque: float
    combustivel_atual: float
    tipo: str

class ExecutarAlgoritmoRequest(BaseModel):
    limite_geracoes: int = 10
    tamanho_populacao: int = 4
    tipo_selecao: str = "torneio"
    usar_mutacao: bool = True
    taxa_mutacao: float = 1.0
    usar_elitismo: bool = False
    quantidade_elite: int = 1
    tamanho_torneio: int = 2
    
    matriz_distancias: List[List[float]]
    lugares: List[LugarInput]
    veiculo: VeiculoInput
    
    populacao_inicial: List[List[int]]

@app.post("/algoritmo/executar", tags=["Algoritmo Genético"])
def executar_algoritmo_completo(dados: ExecutarAlgoritmoRequest):
    try:
        lugares_obj = [
            Lugar(l.nome, l.latitude, l.longitude, l.tipo) 
            for l in dados.lugares
        ]
        
        veiculo_obj = Veiculo(
            consumo_medio=dados.veiculo.consumo_medio,
            capacidade_tanque=dados.veiculo.capacidade_tanque,
            combustivel_atual=dados.veiculo.combustivel_atual,
            tipo=dados.veiculo.tipo
        )
        
        definicao = DefinicaoProblema(
            lugares=lugares_obj,
            matriz_distancias=dados.matriz_distancias,
            veiculo=veiculo_obj
        )
        
        populacao_obj = [
            Individuo(rota_pontos_obrigatorios=rota, rota_completa=[], fitness=0.0) 
            for rota in dados.populacao_inicial
        ]
        
        ag = AlgoritmoGenetico(
            limite_geracoes=dados.limite_geracoes,
            tamanho_populacao=dados.tamanho_populacao,
            definicao_problema=definicao
        )
        
        melhor_individuo = ag.executar_algoritmo(
            populacao_inicial=populacao_obj,
            tipo_selecao=dados.tipo_selecao,
            usar_mutacao=dados.usar_mutacao,
            taxa_mutacao=dados.taxa_mutacao,
            usar_elitismo=dados.usar_elitismo,
            quantidade_elite=dados.quantidade_elite,
            tamanho_torneio=dados.tamanho_torneio
        )
        
        return {
            "sucesso": True,
            "parametros_utilizados": {
                "geracoes": dados.limite_geracoes,
                "selecao": dados.tipo_selecao
            },
            "resultado": {
                "melhor_rota_obrigatoria": melhor_individuo.rota_pontos_obrigatorios,
                "melhor_rota_completa": melhor_individuo.rota_completa,
                "fitness": melhor_individuo.fitness
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)