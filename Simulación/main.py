import json
import pygame
from src.interseccion import Interseccion
from src.controlador_casi import ControladorCASI
from src.simulacion import Simulacion

if __name__ == "__main__":
    # Cargar la configuración desde el archivo JSON
    with open("config/settings.json") as f:
        config = json.load(f)

    # Crear la instancia del controlador CASI con la configuración
    controlador = ControladorCASI(intersecciones=[], config_path="config/settings.json")

    # Definir el centro de la intersección en el tamaño de la pantalla
    ancho, alto = 800, 600
    centro_interseccion = (ancho // 2, alto // 2)

    # Crear las intersecciones con la configuración correcta para cada semáforo
    intersecciones = [
        Interseccion(centro_interseccion, config_semaforo=config["semaforo_timing"])
    ]

    # Asignar intersecciones al controlador CASI
    controlador.intersecciones = intersecciones

    # Iniciar la simulación
    simulacion = Simulacion(ancho, alto, controlador)
    simulacion.ejecutar_simulacion()
