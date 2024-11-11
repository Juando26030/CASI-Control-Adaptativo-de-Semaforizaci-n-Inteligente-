import math


class Auto:
    def __init__(self, posicion, velocidad, direccion):
        self.posicion = posicion
        self.velocidad = velocidad
        self.direccion = direccion

    def mover(self):
        rad = math.radians(self.direccion)
        self.posicion[0] += self.velocidad * math.cos(rad)
        self.posicion[1] += self.velocidad * math.sin(rad)

    def revisar_semaforo(self, semaforo):
        if semaforo.color_actual == "rojo":
            self.velocidad = 0
        else:
            self.velocidad = 1
