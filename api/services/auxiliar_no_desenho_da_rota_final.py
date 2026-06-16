from api.cliente_distancia.cliente_distancia import obter_caminho_entre_dois_pontos

def gerar_caminho_para_desenho(individuo, definicao_problema):
    segmentos = []

    rota = individuo.rota_completa
    lugares = definicao_problema.lugares

    for i in range(len(rota) - 1):
        origem_obj = lugares[rota[i]]
        destino_obj = lugares[rota[i + 1]]

        segmento = obter_caminho_entre_dois_pontos(origem_obj, destino_obj)

        segmentos.append({
            "origem": origem_obj.nome,
            "destino": destino_obj.nome,
            "geometry": segmento
        })

    return segmentos

