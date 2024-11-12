import pandas as pd
import json
import random

from Simulación.src.ajuste_tiempo_semaforo import AjusteTiempoSemaforo

class ControladorCASI:
    def __init__(self, intersecciones, config_path="config/settings.json"):
        self.intersecciones = intersecciones
        self.datos_trafico = pd.read_csv("data/sensor_data.csv")
        with open(config_path) as f:
            self.config = json.load(f)

        self.car_speed = self.config["car_speed"]
        self.car_frequency = self.config["car_frequency"]
        self.update_frequency = self.config["update_frequency"]
        self.intervalo_entre_autos = 60 / self.car_frequency

        self.ajuste_tiempos_semaforo = AjusteTiempoSemaforo("data/traffic_data.json", config_path)
        self.actualizar_tiempos_semaforo()

        # Inicializar las variables de estado
        self.tiempo_estado_actual = 0  # Tiempo acumulado en el estado actual del semáforo
        self.estado_actual = "norte_sur_verde"  # Estado inicial del semáforo

    def actualizar_tiempos_semaforo(self):
        self.ajuste_tiempos_semaforo.ejecutar_ajuste()
        with open(self.ajuste_tiempos_semaforo.config_path) as f:
            self.config = json.load(f)
        self.tiempos_semaforo_norte_sur = self.config["semaforo_timing"]["NS"]
        self.tiempos_semaforo_este_oeste = self.config["semaforo_timing"]["WE"]
        self.tiempos_semaforo_sur_norte = self.config["semaforo_timing"]["SN"]
        self.tiempos_semaforo_este_oeste_rev = self.config["semaforo_timing"]["EW"]

    def recopilar_datos(self):
        for interseccion in self.intersecciones:
            datos_sensores = interseccion.reportar_datos_sensores()
            print(f"Datos de sensores para intersección {interseccion.id}: {datos_sensores}")

    def optimizar_semaforos(self):
        # Actualizar el tiempo del estado actual
        self.tiempo_estado_actual += self.update_frequency

        # Determinar el tiempo del semáforo según el estado actual
        if self.estado_actual == "norte_sur_verde":
            tiempo_actual = self.tiempos_semaforo_norte_sur["verde"]
        elif self.estado_actual == "norte_sur_amarillo":
            tiempo_actual = self.tiempos_semaforo_norte_sur["amarillo"]
        elif self.estado_actual == "este_oeste_verde":
            tiempo_actual = self.tiempos_semaforo_este_oeste["verde"]
        elif self.estado_actual == "este_oeste_amarillo":
            tiempo_actual = self.tiempos_semaforo_este_oeste["amarillo"]
        elif self.estado_actual == "sur_norte_verde":
            tiempo_actual = self.tiempos_semaforo_sur_norte["verde"]
        elif self.estado_actual == "sur_norte_amarillo":
            tiempo_actual = self.tiempos_semaforo_sur_norte["amarillo"]
        elif self.estado_actual == "este_oeste_rev_verde":
            tiempo_actual = self.tiempos_semaforo_este_oeste_rev["verde"]
        else:
            tiempo_actual = self.tiempos_semaforo_este_oeste_rev["amarillo"]

        # Cambiar el estado de los semáforos cuando el tiempo del estado se haya cumplido
        if self.tiempo_estado_actual >= tiempo_actual:
            self.tiempo_estado_actual = 0

            # Cambiar el estado de los semáforos en orden
            if self.estado_actual == "norte_sur_verde":
                self.estado_actual = "norte_sur_amarillo"
            elif self.estado_actual == "norte_sur_amarillo":
                self.estado_actual = "este_oeste_verde"
            elif self.estado_actual == "este_oeste_verde":
                self.estado_actual = "este_oeste_amarillo"
            elif self.estado_actual == "este_oeste_amarillo":
                self.estado_actual = "norte_sur_verde"
            elif self.estado_actual == "sur_norte_verde":
                self.estado_actual = "sur_norte_amarillo"
            elif self.estado_actual == "sur_norte_amarillo":
                self.estado_actual = "este_oeste_rev_verde"
            elif self.estado_actual == "este_oeste_rev_verde":
                self.estado_actual = "este_oeste_rev_amarillo"
            else:
                self.estado_actual = "sur_norte_verde"

        # Asignar los colores de los semáforos en función del estado
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
            elif self.estado_actual == "sur_norte_verde":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "verde"
            elif self.estado_actual == "sur_norte_amarillo":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "amarillo"
            elif self.estado_actual == "este_oeste_rev_verde":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "verde"
            elif self.estado_actual == "este_oeste_rev_amarillo":
                interseccion.semaforos["norte"].color_actual = "rojo"
                interseccion.semaforos["sur"].color_actual = "rojo"
                interseccion.semaforos["este"].color_actual = "rojo"
                interseccion.semaforos["oeste"].color_actual = "amarillo"

    def decidir_aparicion_auto(self):
        intervalo_aparicion = self.intervalo_entre_autos

        return intervalo_aparicion