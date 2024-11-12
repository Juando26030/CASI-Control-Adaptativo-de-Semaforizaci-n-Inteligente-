import pandas as pd
import json
import random

class ControladorCASI:
    def __init__(self, intersecciones, config_path="config/settings.json"):
        """
        Inicializa el controlador CASI con las intersecciones y la configuración.
        """
        self.intersecciones = intersecciones
        self.datos_trafico = pd.read_csv("data/sensor_data.csv")

        # Cargar la configuración del archivo JSON
        with open(config_path) as f:
            self.config = json.load(f)

        # Configuración de la velocidad y frecuencia de autos
        self.car_speed = self.config["car_speed"]
        self.car_frequency = self.config["car_frequency"]
        self.update_frequency = self.config["update_frequency"]

        # Cálculo del intervalo entre autos en segundos
        self.intervalo_entre_autos = 60 / self.car_frequency

        # Tiempos de semáforos independientes
        self.tiempos_semaforo_norte_sur = self.config["semaforo_timing"]["norte_sur"]
        self.tiempos_semaforo_este_oeste = self.config["semaforo_timing"]["este_oeste"]

        # Estados de alternancia de semáforos
        self.estado_actual = "norte_sur_verde"  # Comienza con semáforos norte-sur en verde
        self.tiempo_estado_actual = 0  # Contador para el tiempo en el estado actual

    def recopilar_datos(self):
        """
        Simula la recopilación de datos de tráfico para cada intersección.
        """
        for interseccion in self.intersecciones:
            datos_sensores = interseccion.reportar_datos_sensores()
            print(f"Datos de sensores para intersección {interseccion.id}: {datos_sensores}")

    def optimizar_semaforos(self):
        """
        Alterna los semáforos entre los estados norte-sur y este-oeste basado en los tiempos de configuración.
        """
        # Incrementar el contador de tiempo en el estado actual
        self.tiempo_estado_actual += self.update_frequency

        # Definir los tiempos según el estado actual
        if self.estado_actual == "norte_sur_verde":
            tiempo_actual = self.tiempos_semaforo_norte_sur["verde"]
        elif self.estado_actual == "norte_sur_amarillo":
            tiempo_actual = self.tiempos_semaforo_norte_sur["amarillo"]
        elif self.estado_actual == "este_oeste_verde":
            tiempo_actual = self.tiempos_semaforo_este_oeste["verde"]
        else:  # "este_oeste_amarillo"
            tiempo_actual = self.tiempos_semaforo_este_oeste["amarillo"]

        # Verificar si se debe cambiar de estado
        if self.tiempo_estado_actual >= tiempo_actual:
            self.tiempo_estado_actual = 0  # Reiniciar el tiempo en el nuevo estado

            # Cambiar el estado de los semáforos según el ciclo
            if self.estado_actual == "norte_sur_verde":
                self.estado_actual = "norte_sur_amarillo"
            elif self.estado_actual == "norte_sur_amarillo":
                self.estado_actual = "este_oeste_verde"
            elif self.estado_actual == "este_oeste_verde":
                self.estado_actual = "este_oeste_amarillo"
            elif self.estado_actual == "este_oeste_amarillo":
                self.estado_actual = "norte_sur_verde"

        # Ajustar el color de los semáforos en cada intersección según el estado actual
        for interseccion in self.intersecciones:
            if self.estado_actual == "norte_sur_verde":
                interseccion.semaforos["norte"].color_actual = "verde"
                interseccion.semaforos["sur"].color_actual = "verde"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "rojo"
            elif self.estado_actual == "norte_sur_amarillo":
                interseccion.semaforos["norte"].color_actual = "amarillo"
                interseccion.semaforos["sur"].color_actual = "amarillo"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "rojo"
            elif self.estado_actual == "este_oeste_verde":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "verde"
                interseccion.semaforos["oeste"].color_actual = "verde"
            elif self.estado_actual == "este_oeste_amarillo":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "amarillo"
                interseccion.semaforos["oeste"].color_actual = "amarillo"

    def decidir_aparicion_auto(self):
        """
        Decide aleatoriamente si aparece un nuevo auto basado en la frecuencia configurada.
        """
        intervalo_random = random.uniform(0.5 * self.intervalo_entre_autos, 1.5 * self.intervalo_entre_autos)
        return intervalo_random
