import pygame


class Renderer:
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def dibujar_interseccion(self, interseccion):
        # Colores del semáforo
        color_map = {
            "verde": pygame.Color("green"),
            "amarillo": pygame.Color("yellow"),
            "rojo": pygame.Color("red")
        }
        color_semaforo = color_map[interseccion.semaforo.color_actual]

        # Dibuja la intersección como un rectángulo gris con un círculo representando el semáforo
        pygame.draw.rect(self.pantalla, (200, 200, 200),
                         (interseccion.posicion[0] - 25, interseccion.posicion[1] - 25, 50, 50))
        pygame.draw.circle(self.pantalla, color_semaforo, interseccion.posicion, 20)

    def dibujar_auto(self, auto):
        # Dibuja los autos en azul
        pygame.draw.circle(self.pantalla, pygame.Color("blue"), (int(auto.posicion[0]), int(auto.posicion[1])), 10)

    def renderizar(self, intersecciones, autos):
        # Dibuja intersecciones
        for interseccion in intersecciones:
            self.dibujar_interseccion(interseccion)

        # Dibuja autos
        for auto in autos:
            self.dibujar_auto(auto)
