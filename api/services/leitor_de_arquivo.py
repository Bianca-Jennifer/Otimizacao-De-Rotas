import csv
import io
from api.classes.lugar import Lugar

def ler_arquivo_de_lugares(conteudo_csv: str):
    lugares = []

    arquivo = io.StringIO(conteudo_csv)
    leitor = csv.DictReader(arquivo)

    for registro in leitor:
        lugares.append(
            Lugar(
                nome=registro["NOME"],
                latitude=float(registro["LATITUDE"]),
                longitude=float(registro["LONGITUDE"]),
                tipo=registro["TIPO"]
            )
        )

    return lugares
