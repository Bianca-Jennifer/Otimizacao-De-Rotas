class Lugar:
    def __init__(self, nome, latitude, longitude, tipo):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude
        self.tipo = tipo

    def to_osrm(self):
        return f"{self.longitude},{self.latitude}"    