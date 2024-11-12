import pandas as pd


class ControladorCASI:
    def __init__(self, intersecciones):
        self.intersecciones = intersecciones
        self.datos_trafico = pd.read_csv("data/sensor_data.csv")

    def recopilar_datos(self):
        """
        Recopila datos de sensores de cada intersección.
        """
        datos = [interseccion.reportar_datos_sensores() for interseccion in self.intersecciones]
        return datos

    def optimizar_semaforos(self):
        """
        Ajusta el temporizador de los semáforos en función de los datos de tráfico.
        """
        for interseccion in self.intersecciones:
            for semaforo in interseccion.semaforos.values():  # Iterar sobre cada semáforo
                semaforo.ajustar_tiempo()

