import pygame
from src.interseccion import Interseccion
from src.auto import Auto
from src.controlador_casi import ControladorCASI
from src.renderer import Renderer
import time
import random


class Simulacion:
    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

        # Centro de la intersección
        self.centro_x, self.centro_y = ancho // 2, alto // 2

        # Intersecciones y autos
        self.intersecciones = [Interseccion((self.centro_x, self.centro_y))]
        self.autos = []
        self.ultimo_tiempo_auto = time.time()

        # Instancia del controlador CASI y el renderer
        self.controlador = ControladorCASI(self.intersecciones)
        self.renderer = Renderer(self.pantalla)

        # Reloj de actualización
        self.tiempo_actualizacion = pygame.time.Clock()

    def generar_autos(self):
        """
        Genera autos en los carriles según la lógica corregida.
        """
        desplazamiento = 60

        # Carriles rotados correctamente en sentido contrario al reloj
        nuevos_autos = [
            # Carril 1: Del norte, puede seguir recto al carril 12 o girar al carril 16.
            Auto(
                posicion=[self.centro_x - desplazamiento * 1.5, self.centro_y - 200],
                velocidad=1,
                direccion=90,  # Va hacia el sur
                carril_origen=1,
                carril_destino=random.choice([12, 16]),
                puede_girar=True
            ),

            # Carril 2: Del norte, va al carril 11.
            Auto(
                posicion=[self.centro_x - desplazamiento * 0.5, self.centro_y - 200],
                velocidad=1,
                direccion=90,  # Va hacia el sur
                carril_origen=2,
                carril_destino=11
            ),

            # Carril 5: Del este, va al carril 12.
            Auto(
                posicion=[self.centro_x + 200, self.centro_y - desplazamiento * 1.5],
                velocidad=1,
                direccion=180,  # Va hacia el oeste
                carril_origen=5,
                carril_destino=12
            ),

            # Carril 6: Del este, va al carril 11.
            Auto(
                posicion=[self.centro_x + 200, self.centro_y - desplazamiento * 0.5],
                velocidad=1,
                direccion=180,  # Va hacia el oeste
                carril_origen=6,
                carril_destino=11
            ),

            # Carril 9: Del sur, puede seguir recto al carril 4 o girar al carril 8.
            Auto(
                posicion=[self.centro_x + desplazamiento * 1.5, self.centro_y + 200],
                velocidad=1,
                direccion=270,  # Va hacia el norte
                carril_origen=9,
                carril_destino=random.choice([4, 8]),
                puede_girar=True
            ),

            # Carril 10: Del sur, va al carril 3.
            Auto(
                posicion=[self.centro_x + desplazamiento * 0.5, self.centro_y + 200],
                velocidad=1,
                direccion=270,  # Va hacia el norte
                carril_origen=10,
                carril_destino=3
            ),

            # Carril 13: Del oeste, va al carril 8.
            Auto(
                posicion=[self.centro_x - 200, self.centro_y + desplazamiento * 1.5],
                velocidad=1,
                direccion=0,  # Va hacia el este
                carril_origen=13,
                carril_destino=8
            ),

            # Carril 14: Del oeste, va al carril 7.
            Auto(
                posicion=[self.centro_x - 200, self.centro_y + desplazamiento * 0.5],
                velocidad=1,
                direccion=0,  # Va hacia el este
                carril_origen=14,
                carril_destino=7
            ),
        ]

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

            # Generar autos cada 3 segundos
            if time.time() - self.ultimo_tiempo_auto > 3:
                self.generar_autos()
                self.ultimo_tiempo_auto = time.time()

            # Actualizar estados de semáforos y autos
            self.controlador.recopilar_datos()
            self.controlador.optimizar_semaforos()
            for auto in self.autos:
                auto.mover()
            for interseccion in self.intersecciones:
                interseccion.semaforo.actualizar()

            # Renderizar usando Renderer
            self.pantalla.fill((255, 255, 255))  # Fondo blanco
            self.renderer.renderizar(self.intersecciones, self.autos)
            pygame.display.flip()
            self.tiempo_actualizacion.tick(60)
