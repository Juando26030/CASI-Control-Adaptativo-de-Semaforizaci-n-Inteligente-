import random


class Semaforo:
    def __init__(self, posicion, datos_sensores=None):
        self.posicion = posicion
        self.color_actual = "rojo"
        self.temporizador = {"verde": 10, "amarillo": 3, "rojo": 15}
        self.datos_sensores = datos_sensores if datos_sensores else random.randint(1, 10)
        self.tiempo_actual = 0

    def cambiar_color(self):
        if self.color_actual == "verde":
            self.color_actual = "amarillo"
        elif self.color_actual == "amarillo":
            self.color_actual = "rojo"
        elif self.color_actual == "rojo":
            self.color_actual = "verde"

    def ajustar_tiempo(self):
        if self.datos_sensores > 5:
            self.temporizador["verde"] += 5
            self.temporizador["rojo"] -= 2
        else:
            self.temporizador["verde"] = max(10, self.temporizador["verde"] - 1)

    def actualizar(self):
        self.tiempo_actual += 1
        if self.tiempo_actual >= self.temporizador[self.color_actual]:
            self.cambiar_color()
            self.tiempo_actual = 0
            self.ajustar_tiempo()
