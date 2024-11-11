import pygame
from src.interseccion import Interseccion
from src.auto import Auto
from src.controlador_casi import ControladorCASI
from src.renderer import Renderer


class Simulacion:
    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((ancho, alto))

        # Define una disposición en cuadrícula para las intersecciones
        self.intersecciones = [
            Interseccion((100, 100)),
            Interseccion((300, 100)),
            Interseccion((500, 100)),
            Interseccion((100, 300)),
            Interseccion((300, 300))
        ]

        # Agrega varios autos en movimiento
        self.autos = [
            Auto([50, 50], 1, 0),
            Auto([150, 150], 1, 90),
            Auto([450, 250], 1, 180),
            Auto([250, 450], 1, 270)
        ]

        # Instancia del controlador CASI
        self.controlador = ControladorCASI(self.intersecciones)

        # Instancia de Renderer para manejar la visualización
        self.renderer = Renderer(self.pantalla)

        # Reloj de actualización
        self.tiempo_actualizacion = pygame.time.Clock()

    def ejecutar_simulacion(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

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
