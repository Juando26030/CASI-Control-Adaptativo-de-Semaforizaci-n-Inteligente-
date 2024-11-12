import pygame
from time import time
from src.interseccion import Interseccion
from src.auto import Auto
from src.controlador_casi import ControladorCASI
from src.renderer import Renderer
import random

class Simulacion:
    def __init__(self, ancho, alto, controlador):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

        # Centro de la intersección
        self.centro_x, self.centro_y = ancho // 2, alto // 2

        # Configuración de tiempos de semáforos desde el JSON de ControladorCASI
        config_semaforo = controlador.config["semaforo_timing"]

        # Inicialización de intersecciones y lista de autos
        self.intersecciones = [Interseccion((self.centro_x, self.centro_y), config_semaforo)]
        self.autos = []
        self.ultimo_tiempo_auto = time()

        # Instancia de controlador CASI y renderer
        self.controlador = controlador
        self.renderer = Renderer(self.pantalla)

        # Reloj de actualización
        self.tiempo_actualizacion = pygame.time.Clock()

        # Definir el intervalo para generar autos en base a car_frequency para todos los carriles
        self.intervalo_generacion = 60 / controlador.car_frequency  # En segundos

    def generar_autos(self):
        desplazamiento = 60
        margen_fuera_pantalla = 100
        espacio_minimo = 80

        # Definición de los autos en todos los carriles, incluyendo los carriles en línea recta
        posiciones_iniciales = [
            ([self.centro_x - desplazamiento * 1.5, -margen_fuera_pantalla], 90, 1, random.choice([12, 16]), True),
            ([self.centro_x - desplazamiento * 0.5, -margen_fuera_pantalla], 90, 2, 11, False),
            ([self.ancho + margen_fuera_pantalla, self.centro_y - desplazamiento * 1.5], 180, 5, 12, False),
            ([self.ancho + margen_fuera_pantalla, self.centro_y - desplazamiento * 0.5], 180, 6, 11, True),
            ([self.centro_x + desplazamiento * 1.5, self.alto + margen_fuera_pantalla], 270, 9, random.choice([4, 8]), True),
            ([self.centro_x + desplazamiento * 0.5, self.alto + margen_fuera_pantalla], 270, 10, 3, False),
            ([-margen_fuera_pantalla, self.centro_y + desplazamiento * 1.5], 0, 13, 8, False),
            ([-margen_fuera_pantalla, self.centro_y + desplazamiento * 0.5], 0, 14, 7, True),
            # Autos en línea recta de los carriles 6 → 15 y 14 → 7
            ([self.ancho + margen_fuera_pantalla, self.centro_y - desplazamiento * 0.5], 180, 6, 15, False),
            ([-margen_fuera_pantalla, self.centro_y + desplazamiento * 0.5], 0, 14, 7, False),
        ]

        nuevos_autos = []
        for pos_inicial, direccion, carril_origen, carril_destino, puede_girar in posiciones_iniciales:
            # Comprobación para asegurar el espacio mínimo entre autos en el mismo carril y dirección
            if all(
                abs(auto.posicion[1] - pos_inicial[1]) > espacio_minimo
                if auto.carril_origen == carril_origen and direccion in [90, 270]
                else True
                and abs(auto.posicion[0] - pos_inicial[0]) > espacio_minimo
                if auto.carril_origen == carril_origen and direccion in [0, 180]
                else True
                for auto in self.autos
            ):
                nuevos_autos.append(
                    Auto(
                        posicion=pos_inicial,
                        velocidad=self.controlador.car_speed,
                        direccion=direccion,
                        carril_origen=carril_origen,
                        carril_destino=carril_destino,
                        puede_girar=puede_girar
                    )
                )

        self.autos.extend(nuevos_autos)

    def ejecutar_simulacion(self):
        """
        Ejecuta la simulación principal.
        """
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.VIDEORESIZE:
                    self.ancho, self.alto = evento.size
                    self.pantalla = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

            # Consultar intervalo para la aparición de autos
            intervalo = self.controlador.decidir_aparicion_auto()
            if time() - self.ultimo_tiempo_auto > self.intervalo_generacion:
                self.generar_autos()
                self.ultimo_tiempo_auto = time()

            # Actualizar estados de semáforos y autos
            self.controlador.recopilar_datos()
            self.controlador.optimizar_semaforos()

            # Mover autos si el semáforo correspondiente está en verde
            for auto in self.autos:
                semaforo = self.obtener_semaforo_para_auto(auto)
                if semaforo.color_actual == "verde":
                    auto.mover()

            # Actualizar y renderizar semáforos
            for interseccion in self.intersecciones:
                for semaforo in interseccion.semaforos.values():
                    semaforo.actualizar_estado()

            # Renderizar usando Renderer
            self.pantalla.fill((255, 255, 255))  # Fondo blanco
            self.renderer.renderizar(self.intersecciones, self.autos)
            pygame.display.flip()
            self.tiempo_actualizacion.tick(60)

    def obtener_semaforo_para_auto(self, auto):
        """
        Retorna el semáforo que controla el carril de origen del auto.
        """
        if auto.carril_origen in [1, 2]:  # Carriles del norte
            return self.intersecciones[0].semaforos["norte"]
        elif auto.carril_origen in [5, 6]:  # Carriles del este
            return self.intersecciones[0].semaforos["este"]
        elif auto.carril_origen in [9, 10]:  # Carriles del sur
            return self.intersecciones[0].semaforos["sur"]
        elif auto.carril_origen in [13, 14]:  # Carriles del oeste
            return self.intersecciones[0].semaforos["oeste"]
