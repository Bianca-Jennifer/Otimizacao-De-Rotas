import csv
from api.classes.lugar import Lugar
def ler_arquivo_de_lugares(arquivo_csv):
    lugares = []

    with open(arquivo_csv, "r", encoding="utf-8") as arquivo:
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

lugares = ler_arquivo_de_lugares("api/services/teste.csv")

print(lugares)
cont = 0
for l in lugares:
    print(l.nome, l.latitude, l.longitude, l.tipo, cont)
    cont+=1

print("----------")
print(lugares[0].nome, lugares[0].to_osrm())    