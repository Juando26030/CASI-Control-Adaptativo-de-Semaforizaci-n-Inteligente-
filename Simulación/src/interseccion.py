from src.semaforo import Semaforo


class Interseccion:
    def __init__(self, posicion):
        self.posicion = posicion
        self.semaforo = Semaforo(posicion)
        self.autos_en_espera = []

    def actualizar_flujo_trafico(self):
        self.semaforo.datos_sensores = len(self.autos_en_espera)

    def reportar_datos_sensores(self):
        return self.semaforo.datos_sensores
