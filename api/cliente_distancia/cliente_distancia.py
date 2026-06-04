import requests
import os
import api.classes.lugar as Lugar
from api.services.leitor_de_arquivo import ler_arquivo_de_lugares

OSRM_URL = os.getenv("OSRM_URL", "http://10.0.0.119:5000")


def obter_distancia_entre_dois_pontos(lugar1, lugar2):
    url = f"{OSRM_URL}/route/v1/driving/" \
          f"{lugar1.to_osrm()};" \
          f"{lugar2.to_osrm()}?overview=false"

    resposta = requests.get(url)
    dados = resposta.json()

    return dados["routes"][0]["distance"]

def obter_caminho_entre_dois_pontos(lugar1, lugar2):
    url = f"{OSRM_URL}/route/v1/driving/" \
          f"{lugar1.to_osrm()};" \
          f"{lugar2.to_osrm()}?overview=full&geometries=geojson"  

    resposta = requests.get(url)
    dados = resposta.json()

    return dados["routes"][0]["geometry"]    


def gerar_matriz_de_distancias(lugares):
    coordenadas_lugares = ";".join(lugar.to_osrm() for lugar in lugares)
    url = f"{OSRM_URL}/table/v1/driving/{coordenadas_lugares}?annotations=distance"

    resposta = requests.get(url).json()

    return resposta["distances"]

 
def gerar_rota_final(lugares_solucao):
    coordenadas_lugares = ";".join(lugar.to_osrm() for lugar in lugares_solucao)
    url = f"{OSRM_URL}/route/v1/driving/{coordenadas_lugares}?overview=full&geometries=geojson"

    resposta = requests.get(url).json()
    
    return resposta["routes"][0]["geometry"]



