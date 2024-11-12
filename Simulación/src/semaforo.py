import random


# Clase Semaforo para representar un semáforo individual
class Semaforo:
    def __init__(self, id, tiempos, posicion):
        """
        Inicializa un semáforo con los tiempos configurados en el archivo JSON.

        :param id: Identificador del semáforo
        :param tiempos: Diccionario con tiempos de verde, amarillo y rojo
        """
        self.id = id
        self.tiempos = tiempos  # {'verde': 10, 'amarillo': 3, 'rojo': 15}
        self.color_actual = "rojo"
        self.tiempo_restante = tiempos["rojo"]
        self.posicion = posicion

    def actualizar_estado(self):
        """
        Actualiza el estado del semáforo según el tiempo restante.
        """
        self.tiempo_restante -= 1
        if self.tiempo_restante <= 0:
            if self.color_actual == "rojo":
                self.color_actual = "verde"
                self.tiempo_restante = self.tiempos["verde"]
            elif self.color_actual == "verde":
                self.color_actual = "amarillo"
                self.tiempo_restante = self.tiempos["amarillo"]
            elif self.color_actual == "amarillo":
                self.color_actual = "rojo"
                self.tiempo_restante = self.tiempos["rojo"]

    def ajustar_tiempo(self, nuevo_tiempo_verde):
        """
        Ajusta el tiempo en verde del semáforo en función del tráfico.
        """
        self.tiempos["verde"] = nuevo_tiempo_verde