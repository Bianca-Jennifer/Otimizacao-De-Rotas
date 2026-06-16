from api.services.leitor_de_arquivo import ler_arquivo_de_lugares

def test_ler_arquivo_de_lugares():
    csv_teste = """NOME,LATITUDE,LONGITUDE,TIPO
Ponto A,-5.123,-35.456,Ponto
Posto B,-5.789,-35.111,Posto
"""

    lugares = ler_arquivo_de_lugares(csv_teste)

    assert len(lugares) == 2

    assert lugares[0].nome == "Ponto A"
    assert lugares[0].latitude == -5.123
    assert lugares[0].longitude == -35.456
    assert lugares[0].tipo == "Ponto"

    assert lugares[1].nome == "Posto B"
    assert lugares[1].latitude == -5.789
    assert lugares[1].longitude == -35.111
    assert lugares[1].tipo == "Posto"