import pandas as pd
import json
import random

class AjusteTiempoSemaforo:
    def __init__(self, traffic_data_path="data/traffic_data.json", config_path="config/settings.json"):
        self.traffic_data_path = traffic_data_path
        self.config_path = config_path
        self.tiempos_semaforo = {
            "NS": {"verde": 0, "amarillo": 5, "rojo": 0},
            "WE": {"verde": 0, "amarillo": 5, "rojo": 0},
            "SN": {"verde": 0, "amarillo": 5, "rojo": 0},
            "EW": {"verde": 0, "amarillo": 5, "rojo": 0}
        }

    def cargar_datos_trafico(self):
        # Cargar el archivo JSON completo
        with open(self.traffic_data_path, 'r') as file:
            data = json.load(file)
        # Acceder a la lista de datos de tráfico dentro de "vol-data"
        traffic_data = data["vol-data"]
        return traffic_data

    def calcular_flujo_vehicular(self, traffic_data):
        flujo_por_sentido = {"NS": 0, "WE": 0, "SN": 0, "EW": 0}
        pesos_vehiculos = {
            "C2": 1, "BI": 1, "C3": 2, ">=C4": 3, "M": 1, "L": 2, "B": 3, "AT": 1, "INT": 2
        }

        for entrada in traffic_data:
            sentido = entrada["SENTIDO"]
            flujo_ponderado = sum(entrada[vehiculo] * pesos_vehiculos[vehiculo] for vehiculo in pesos_vehiculos)
            flujo_por_sentido[sentido] += flujo_ponderado

        return flujo_por_sentido

    def ajustar_tiempos_semaforo(self, flujo_por_sentido):
        flujo_total = sum(flujo_por_sentido.values())
        tiempo_ciclo = 120

        for sentido, flujo in flujo_por_sentido.items():
            tiempo_verde = int((flujo / flujo_total) * tiempo_ciclo)
            self.tiempos_semaforo[sentido]["verde"] = max(10, tiempo_verde)

        for sentido in self.tiempos_semaforo:
            tiempo_verde_total = sum(self.tiempos_semaforo[s]["verde"] for s in self.tiempos_semaforo if s != sentido)
            self.tiempos_semaforo[sentido]["rojo"] = tiempo_ciclo - self.tiempos_semaforo[sentido]["verde"] - tiempo_verde_total

    def guardar_configuracion(self):
        with open(self.config_path, 'r+') as file:
            config = json.load(file)
            config["semaforo_timing"] = self.tiempos_semaforo
            file.seek(0)
            json.dump(config, file, indent=4)
            file.truncate()

    def ejecutar_ajuste(self):
        # Cargar y procesar los datos de tráfico
        traffic_data = self.cargar_datos_trafico()
        flujo_por_sentido = self.calcular_flujo_vehicular(traffic_data)
        self.ajustar_tiempos_semaforo(flujo_por_sentido)
        self.guardar_configuracion()
