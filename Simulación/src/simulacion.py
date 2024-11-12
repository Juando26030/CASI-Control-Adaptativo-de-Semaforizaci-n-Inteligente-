import pygame
from src.interseccion import Interseccion
from src.auto import Auto
from src.controlador_casi import ControladorCASI
from src.renderer import Renderer

class Simulacion:
    def __init__(self, ancho, alto):
        pygame.init()
        # Configura la ventana ajustable y centrada
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)

        # Centro de la pantalla para la disposición en cruz
        self.intersecciones = [Interseccion((ancho // 2, alto // 2))]

        # Generar 16 autos, 4 en cada dirección, uno por subcarril
        desplazamiento = 60  # Para centrar cada auto en su subcarril
        centro_x, centro_y = ancho // 2, alto // 2
        self.autos = [
            # Autos de izquierda a derecha
            Auto([centro_x - 200, centro_y - desplazamiento * 1.5], 1, 0),
            Auto([centro_x - 200, centro_y - desplazamiento * 0.5], 1, 0),
            Auto([centro_x - 200, centro_y + desplazamiento * 0.5], 1, 0),
            Auto([centro_x - 200, centro_y + desplazamiento * 1.5], 1, 0),

            # Autos de derecha a izquierda
            Auto([centro_x + 200, centro_y - desplazamiento * 1.5], 1, 180),
            Auto([centro_x + 200, centro_y - desplazamiento * 0.5], 1, 180),
            Auto([centro_x + 200, centro_y + desplazamiento * 0.5], 1, 180),
            Auto([centro_x + 200, centro_y + desplazamiento * 1.5], 1, 180),

            # Autos de arriba a abajo
            Auto([centro_x - desplazamiento * 1.5, centro_y - 200], 1, 90),
            Auto([centro_x - desplazamiento * 0.5, centro_y - 200], 1, 90),
            Auto([centro_x + desplazamiento * 0.5, centro_y - 200], 1, 90),
            Auto([centro_x + desplazamiento * 1.5, centro_y - 200], 1, 90),

            # Autos de abajo a arriba
            Auto([centro_x - desplazamiento * 1.5, centro_y + 200], 1, 270),
            Auto([centro_x - desplazamiento * 0.5, centro_y + 200], 1, 270),
            Auto([centro_x + desplazamiento * 0.5, centro_y + 200], 1, 270),
            Auto([centro_x + desplazamiento * 1.5, centro_y + 200], 1, 270)
        ]

        # Instancia del controlador CASI y el renderer
        self.controlador = ControladorCASI(self.intersecciones)
        self.renderer = Renderer(self.pantalla)

        # Reloj de actualización
        self.tiempo_actualizacion = pygame.time.Clock()

    def ejecutar_simulacion(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.VIDEORESIZE:
                    self.ancho, self.alto = evento.size
                    self.pantalla = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

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
