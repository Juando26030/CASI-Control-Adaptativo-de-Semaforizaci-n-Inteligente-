import pandas as pd


class ControladorCASI:
    def __init__(self, intersecciones):
        self.intersecciones = intersecciones
        self.datos_trafico = pd.read_csv("data/sensor_data.csv")

    def recopilar_datos(self):
        datos = [interseccion.reportar_datos_sensores() for interseccion in self.intersecciones]
        return datos

    def optimizar_semaforos(self):
        for interseccion in self.intersecciones:
            interseccion.semaforo.ajustar_tiempo()
