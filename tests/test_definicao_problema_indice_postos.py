from api.classes.definicao_problema import DefinicaoProblema
from api.classes.lugar import Lugar


def test_obter_indice_inicial_para_postos():

    lugares = [
        Lugar(
            nome="Ponto A",
            latitude=-5.10,
            longitude=-35.10,
            tipo="Ponto"
        ),

        Lugar(
            nome="Ponto B",
            latitude=-5.20,
            longitude=-35.20,
            tipo="Ponto"
        ),

        Lugar(
            nome="Posto Central",
            latitude=-5.30,
            longitude=-35.30,
            tipo="Posto"
        ),

        Lugar(
            nome="Posto Secundario",
            latitude=-5.40,
            longitude=-35.40,
            tipo="Posto"
        )
    ]

    problema = DefinicaoProblema(lugares)

    indice = problema.obter_indice_inicial_para_postos()

    assert indice == 2

def test_obter_indice_inicial_para_postos_sem_posto():

    lugares = [
        Lugar("Ponto A", -5.1, -35.1, "Ponto"),
        Lugar("Ponto B", -5.2, -35.2, "Ponto")
    ]

    problema = DefinicaoProblema(lugares)

    indice = problema.obter_indice_inicial_para_postos()

    assert indice == 2