import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.services.processar_service import processar

app = FastAPI(
    title="API - Otimização de Rotas com Algoritmo Genético",
    description="Calcula a melhor rota considerando postos de combustível e limites do veículo."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    veiculo: VeiculoInput

@app.post("/algoritmo/executar", tags=["Algoritmo Genético"])
def executar_algoritmo_completo(dados: ExecutarAlgoritmoRequest):
    try:
        ag, populacao_inicial = processar(dados)

        melhor_individuo = ag.executar_algoritmo(
            populacao_inicial=populacao_inicial,
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