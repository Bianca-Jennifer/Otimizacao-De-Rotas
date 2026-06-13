from api.classes.lugar import Lugar
from api.classes.veiculo import Veiculo
from api.classes.definicao_problema import DefinicaoProblema

def criar_rota_com_postos(definicao_problema, rota):

    rota_final = [rota[0]]

    combustivel = (
        definicao_problema.veiculo.obter_alcance_atual()
    )

    indice_postos = (
        definicao_problema
        .obter_indice_inicial_para_postos()
    )

    autonomia = (
        definicao_problema
        .veiculo
        .obter_autonomia()
    )

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        distancia_direta = (
            definicao_problema
            .matriz_distancias[origem][destino]
        )

        # =====================================
        # CONSEGUE IR DIRETO
        # =====================================

        if distancia_direta <= combustivel:

            combustivel -= distancia_direta

            rota_final.append(destino)

            continue

        # =====================================
        # PRECISA DE POSTO
        # =====================================

        melhor_posto = None
        menor_custo = float("inf")

        for possible_posto in range(
            indice_postos,
            len(definicao_problema.matriz_distancias)
        ):

            if possible_posto == origem:
                continue

            if possible_posto == destino:
                continue

            distancia_ate_posto = (
                definicao_problema
                .matriz_distancias[origem][possible_posto]
            )

            distancia_posto_destino = (
                definicao_problema
                .matriz_distancias[possible_posto][destino]
            )

            # Consegue chegar ao posto
            if distancia_ate_posto <= combustivel:

                # Após abastecer,
                # consegue chegar ao destino
                if distancia_posto_destino <= autonomia:

                    custo = (
                        distancia_ate_posto +
                        distancia_posto_destino
                    )

                    if custo < menor_custo:

                        menor_custo = custo
                        melhor_posto = possible_posto

        # =====================================
        # NÃO EXISTE POSTO VIÁVEL
        # =====================================

        if melhor_posto is None:
            return rota_final, True

        # Vai até o posto
        combustivel -= (
            definicao_problema
            .matriz_distancias[origem][melhor_posto]
        )

        rota_final.append(melhor_posto)

        # Reabastece
        combustivel = autonomia

        # Vai do posto ao destino
        combustivel -= (
            definicao_problema
            .matriz_distancias[melhor_posto][destino]
        )

        rota_final.append(destino)

    return rota_final, False


def criar_rota_com_postos2(definicao_problema, rota):

    rota_final = [rota[0]]

    combustivel = (
        definicao_problema
        .veiculo
        .obter_alcance_atual()
    )

    indice_postos = (
        definicao_problema
        .obter_indice_inicial_para_postos()
    )

    autonomia = (
        definicao_problema
        .veiculo
        .obter_autonomia()
    )

    i = 0

    while i < len(rota) - 1:

        origem = rota[i]
        destino = rota[i + 1]



        distancia_direta = (definicao_problema.matriz_distancias[origem][destino])

       

        # =====================================
        # CONSEGUE IR DIRETO
        # =====================================

        if distancia_direta <= combustivel:
            print("CONSEGUE IR DIRETO")

            combustivel -= distancia_direta

            print(f"COMBUSTÍVEL RESTANTE: {combustivel}")

            rota_final.append(destino)

            i += 1

            continue

        # =====================================
        # TENTA INSERIR POSTO
        # =====================================
        
        melhor_posto = None
        menor_custo = float("inf")

        for possible_posto in range(
            indice_postos,
            len(definicao_problema.matriz_distancias)
        ):

            if possible_posto == origem:
                continue

            if possible_posto == destino:
                continue

            distancia_ate_posto = (
                definicao_problema
                .matriz_distancias[origem][possible_posto]
            )

            distancia_posto_destino = (
                definicao_problema
                .matriz_distancias[possible_posto][destino]
            )

            if distancia_ate_posto <= combustivel:

                if distancia_posto_destino <= autonomia:

                    custo = (
                        distancia_ate_posto +
                        distancia_posto_destino
                    )

                    if custo < menor_custo:

                        menor_custo = custo
                        melhor_posto = possible_posto

        # =====================================
        # ENCONTROU POSTO
        # =====================================

        if melhor_posto is not None:
            

            combustivel -= (
                definicao_problema
                .matriz_distancias[origem][melhor_posto]
            )

            rota_final.append(melhor_posto)

            combustivel = autonomia

            combustivel -= (
                definicao_problema
                .matriz_distancias[melhor_posto][destino]
            )

            rota_final.append(destino)

            i += 1

            continue

        # =====================================
        # SE JÁ VEIO DE POSTO
        # É INVIÁVEL
        # =====================================

        if len(rota_final) >= 2:

            anterior = rota_final[-2]

            if anterior >= indice_postos:
                return rota_final, True

        # =====================================
        # RECUPERAÇÃO
        # =====================================

        if len(rota_final) < 2:
            return rota_final, True

        anterior = rota_final[-2]

        melhor_posto_recuperacao = None
        menor_custo = float("inf")

        for possible_posto in range(
            indice_postos,
            len(definicao_problema.matriz_distancias)
        ):

            if possible_posto == anterior:
                continue

            if possible_posto == origem:
                continue

            distancia_ate_posto = (
                definicao_problema
                .matriz_distancias[anterior][possible_posto]
            )

            distancia_posto_origem = (
                definicao_problema
                .matriz_distancias[possible_posto][origem]
            )

            combustivel_no_anterior = (
                combustivel +
                definicao_problema
                .matriz_distancias[anterior][origem]
            )

            if distancia_ate_posto <= combustivel_no_anterior:

                if distancia_posto_origem <= autonomia:

                    combustivel_na_origem = (
                        autonomia -
                        distancia_posto_origem
                    )

                    consegue_continuar = False

                    if (
                        distancia_direta <=
                        combustivel_na_origem
                    ):

                        consegue_continuar = True

                    else:

                        for outro_posto in range(
                            indice_postos,
                            len(
                                definicao_problema
                                .matriz_distancias
                            )
                        ):

                            if outro_posto == origem:
                                continue

                            distancia_ate_outro_posto = (
                                definicao_problema
                                .matriz_distancias[
                                    origem
                                ][outro_posto]
                            )

                            if (
                                distancia_ate_outro_posto <=
                                combustivel_na_origem
                            ):

                                consegue_continuar = True
                                break

                    if consegue_continuar:

                        custo = (
                            distancia_ate_posto +
                            distancia_posto_origem
                        )

                        if custo < menor_custo:

                            menor_custo = custo
                            melhor_posto_recuperacao = (
                                possible_posto
                            )

        if melhor_posto_recuperacao is None:
            return rota_final, True

        # Remove origem antiga
        rota_final.pop()

        # Insere posto
        rota_final.append(
            melhor_posto_recuperacao
        )

        # Reabastece
        combustivel = autonomia

        # Vai até origem
        combustivel -= (
            definicao_problema
            .matriz_distancias[
                melhor_posto_recuperacao
            ][origem]
        )

        rota_final.append(origem)

        # NÃO AVANÇA i
        # tenta novamente origem -> destino

    return rota_final, False

def criar_rota_com_postos3(definicao_problema, rota):

    rota_caixeiro_viajante = [0] + rota + [0]

    print(rota_caixeiro_viajante)

    return criar_rota_com_postos2(definicao_problema, rota_caixeiro_viajante)


