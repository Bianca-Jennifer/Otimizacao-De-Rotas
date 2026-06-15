import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi import Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.services.auxiliar_no_desenho_da_rota_final import gerar_caminho_para_desenho
from api.services.distancia_e_litro_gastos import calcular_distancia_total, calcular_litros_gastos
from api.services.processar_service import processar
from api.services.gerar_populacao_inicial import gerar_populacao_inicial

app = FastAPI(
    title="API - Otimização de Rotas com Algoritmo Genético",
    description="Calcula a melhor rota considerando postos de combustível e limites do veículo."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VeiculoInput(BaseModel):
    consumoMedio: float
    capacidadeTanque: float
    combustivelAtual: float
    tipo: str = "moto"

class ExecutarAlgoritmoRequest(BaseModel):
    limiteGeracoes: int = 10
    tamanhoPopulacao: int = 4
    formaSelecao: str = "torneio"
    mutacao: bool = True

    veiculo: VeiculoInput

@app.post("/algoritmo/executar", tags=["Algoritmo Genético"])
def executar_algoritmo_completo(
    limiteGeracoes: int = Form(...),
    tamanhoPopulacao: int = Form(...),
    formaSelecao: str = Form(...),
    mutacao: bool = Form(...),

    consumoMedio: float = Form(...),
    capacidadeTanque: float = Form(...),
    combustivelAtual: float = Form(...),

    arquivoCSV: UploadFile = File(...)
):
    try:
        dados = ExecutarAlgoritmoRequest(
            limiteGeracoes=limiteGeracoes,
            tamanhoPopulacao=tamanhoPopulacao,
            formaSelecao=formaSelecao,
            mutacao=mutacao,

            veiculo=VeiculoInput(
                consumoMedio=consumoMedio,
                capacidadeTanque=capacidadeTanque,
                combustivelAtual=combustivelAtual
            )
        )

        conteudo_csv = arquivoCSV.file.read().decode("utf-8")

        print("Dados recebidos:", dados)

        ag = processar(dados, conteudo_csv)
        print(ag.definicao_problema.matriz_distancias)

        populacao_inicial = gerar_populacao_inicial(ag.definicao_problema.lugares, ag.tamanho_populacao)

        melhor_individuo = ag.executar_algoritmo(
            populacao_inicial=populacao_inicial,
            tipo_selecao=dados.formaSelecao,
            usar_mutacao=dados.mutacao
        )

        caminho_para_desenho = gerar_caminho_para_desenho(melhor_individuo, ag.definicao_problema)
        distancia_total = calcular_distancia_total(melhor_individuo, ag.definicao_problema)
        litros_gastos = calcular_litros_gastos(distancia_total, ag.definicao_problema)
        ordem_de_visita_lugares = ag.definicao_problema.rota_completa_com_lugares(melhor_individuo.rota_completa)
        fitness_da_solucao = melhor_individuo.fitness
        
        return {
            "sucesso": True,

            "parametros_utilizados": {
                "geracoes": dados.limiteGeracoes,
                "selecao": dados.formaSelecao
            },

            "resultado": {
                "distancia_total": distancia_total,
                "litros_gastos": litros_gastos,
                "fitness": fitness_da_solucao,

                "ordem_de_visita_nomes": ordem_de_visita_lugares,
                "caminho_para_desenho": caminho_para_desenho
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)