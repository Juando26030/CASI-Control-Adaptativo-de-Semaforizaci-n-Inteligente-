import pygame
from src.interseccion import Interseccion
from src.auto import Auto
from src.controlador_casi import ControladorCASI
import json


class Simulacion:
    def __init__(self, ancho, alto):
        pygame.init()
        self.ancho = ancho
        self.alto = alto
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.intersecciones = [Interseccion((100, 200)), Interseccion((300, 400))]
        self.autos = [Auto([50, 50], 1, 0)]
        self.controlador = ControladorCASI(self.intersecciones)
        self.tiempo_actualizacion = pygame.time.Clock()

    def ejecutar_simulacion(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Actualizar estados
            self.controlador.recopilar_datos()
            self.controlador.optimizar_semaforos()
            for auto in self.autos:
                auto.mover()
            for interseccion in self.intersecciones:
                interseccion.semaforo.actualizar()

            # Renderizar
            self.pantalla.fill((255, 255, 255))
            self.mostrar()
            pygame.display.flip()
            self.tiempo_actualizacion.tick(60)

    def mostrar(self):
        # Dibuja intersecciones y semáforos
        for interseccion in self.intersecciones:
            color = {"verde": pygame.Color("green"), "amarillo": pygame.Color("yellow"), "rojo": pygame.Color("red")}
            pygame.draw.circle(self.pantalla, color[interseccion.semaforo.color_actual], interseccion.posicion, 20)

        # Dibuja autos
        for auto in self.autos:
            pygame.draw.circle(self.pantalla, pygame.Color("blue"), (int(auto.posicion[0]), int(auto.posicion[1])), 10)
