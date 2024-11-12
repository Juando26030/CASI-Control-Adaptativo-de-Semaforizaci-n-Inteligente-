import pygame
from src.utils import Utils

class Renderer:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        # Cargar imágenes de autos y semáforos usando Utils
        self.auto_imagen = Utils.cargar_imagen("car.png")
        self.semaforo_imagenes = {
            "verde": Utils.cargar_imagen("traffic_light_green.png"),
            "amarillo": Utils.cargar_imagen("traffic_light_yellow.png"),
            "rojo": Utils.cargar_imagen("traffic_light_red.png")
        }
        self.ancho_calle = 240  # Ancho total de la calle (para ambos sentidos)
        self.ancho_carril = 60   # Ancho de cada subcarril
        self.largo_segmento_blanco = 60  # Longitud de cada segmento blanco
        self.espacio_blanco = 25         # Espacio entre segmentos blancos

    def dibujar_calles(self):
        # Colores para la calle y líneas
        color_calle = (180, 180, 180)
        color_linea_divisoria = (0, 0, 0)  # Línea divisoria central entre los dos sentidos (negra)
        color_linea_carril = (255, 255, 255)  # Línea divisoria entre subcarriles (blanca)

        centro_x, centro_y = self.pantalla.get_width() // 2, self.pantalla.get_height() // 2

        # Dibujar calles en cruz
        # Calle vertical
        pygame.draw.rect(self.pantalla, color_calle,
                         (centro_x - self.ancho_calle // 2, 0, self.ancho_calle, self.pantalla.get_height()))
        # Calle horizontal
        pygame.draw.rect(self.pantalla, color_calle,
                         (0, centro_y - self.ancho_calle // 2, self.pantalla.get_width(), self.ancho_calle))

        # Área de exclusión (cuadrado central donde no habrá líneas)
        area_exclusion = pygame.Rect(
            centro_x - self.ancho_calle // 2,
            centro_y - self.ancho_calle // 2,
            self.ancho_calle,
            self.ancho_calle
        )

        # Dibujar las líneas negras divisorias centrales (hasta el borde del cuadrado)
        # Línea negra vertical en el centro de la calle
        pygame.draw.line(self.pantalla, color_linea_divisoria,
                         (centro_x, 0), (centro_x, centro_y - self.ancho_calle // 2), 3)
        pygame.draw.line(self.pantalla, color_linea_divisoria,
                         (centro_x, centro_y + self.ancho_calle // 2), (centro_x, self.pantalla.get_height()), 3)

        # Línea negra horizontal en el centro de la calle
        pygame.draw.line(self.pantalla, color_linea_divisoria,
                         (0, centro_y), (centro_x - self.ancho_calle // 2, centro_y), 3)
        pygame.draw.line(self.pantalla, color_linea_divisoria,
                         (centro_x + self.ancho_calle // 2, centro_y), (self.pantalla.get_width(), centro_y), 3)

        # Offset para la línea blanca de cada lado (debe estar en el centro de cada sentido)
        mitad_sentido = self.ancho_calle // 4

        # Dibujar líneas intermitentes en la mitad izquierda y derecha (verticales)
        for offset_x in [-mitad_sentido, mitad_sentido]:
            y = centro_y + self.ancho_calle // 2  # Comienza desde el borde inferior del cuadrado central y va hacia afuera
            while y < self.pantalla.get_height():
                # Dibuja un segmento de línea blanca
                pygame.draw.line(self.pantalla, color_linea_carril,
                                 (centro_x + offset_x, y),
                                 (centro_x + offset_x, y + self.largo_segmento_blanco), 2)
                # Avanza al siguiente segmento después del espacio
                y += self.largo_segmento_blanco + self.espacio_blanco

            # Repetir hacia arriba desde el borde superior del cuadrado central
            y = centro_y - self.ancho_calle // 2 - self.largo_segmento_blanco
            while y > 0:
                pygame.draw.line(self.pantalla, color_linea_carril,
                                 (centro_x + offset_x, y),
                                 (centro_x + offset_x, y - self.largo_segmento_blanco), 2)
                y -= self.largo_segmento_blanco + self.espacio_blanco

        # Dibujar líneas intermitentes en la mitad superior e inferior (horizontales)
        for offset_y in [-mitad_sentido, mitad_sentido]:
            x = centro_x + self.ancho_calle // 2  # Comienza desde el borde derecho del cuadrado central y va hacia afuera
            while x < self.pantalla.get_width():
                pygame.draw.line(self.pantalla, color_linea_carril,
                                 (x, centro_y + offset_y),
                                 (x + self.largo_segmento_blanco, centro_y + offset_y), 2)
                x += self.largo_segmento_blanco + self.espacio_blanco

            # Repetir hacia la izquierda desde el borde izquierdo del cuadrado central
            x = centro_x - self.ancho_calle // 2 - self.largo_segmento_blanco
            while x > 0:
                pygame.draw.line(self.pantalla, color_linea_carril,
                                 (x, centro_y + offset_y),
                                 (x - self.largo_segmento_blanco, centro_y + offset_y), 2)
                x -= self.largo_segmento_blanco + self.espacio_blanco

    def dibujar_flechas(self):
        # Función para dibujar flechas en cada dirección de la intersección
        color_flecha = (255, 255, 0)
        centro_x, centro_y = self.pantalla.get_width() // 2, self.pantalla.get_height() // 2
        offset_flecha = 60  # Distancia de la flecha respecto al centro

        # Flechas de dirección permitida en vertical
        for dy in [-offset_flecha, offset_flecha]:
            pygame.draw.polygon(self.pantalla, color_flecha, [
                (centro_x, centro_y + dy),
                (centro_x - 10, centro_y + dy - 20),
                (centro_x + 10, centro_y + dy - 20)
            ])

        # Flechas de dirección permitida en horizontal
        for dx in [-offset_flecha, offset_flecha]:
            pygame.draw.polygon(self.pantalla, color_flecha, [
                (centro_x + dx, centro_y),
                (centro_x + dx - 20, centro_y - 10),
                (centro_x + dx - 20, centro_y + 10)
            ])

    def dibujar_interseccion(self, interseccion):
        # Obtener la imagen del semáforo según el color actual
        imagen_semaforo = self.semaforo_imagenes[interseccion.semaforo.color_actual]
        # Posicionar la imagen del semáforo en el centro de la intersección
        rect = imagen_semaforo.get_rect(center=interseccion.posicion)
        self.pantalla.blit(imagen_semaforo, rect)

    def dibujar_auto(self, auto):
        # Rotar la imagen del auto según la dirección del movimiento
        imagen_auto_rotada = pygame.transform.rotate(self.auto_imagen, -auto.direccion)
        rect = imagen_auto_rotada.get_rect(center=(int(auto.posicion[0]), int(auto.posicion[1])))
        # Dibujar el auto en la posición actual
        self.pantalla.blit(imagen_auto_rotada, rect)

    def dibujar_semaforos(self, interseccion):
        """
        Dibuja los semáforos de una intersección en sus posiciones correspondientes.
        """
        for semaforo in interseccion.semaforos.values():
            imagen_semaforo = self.semaforo_imagenes[semaforo.color_actual]
            rect = imagen_semaforo.get_rect(center=semaforo.posicion)
            self.pantalla.blit(imagen_semaforo, rect)

    def renderizar(self, intersecciones, autos):
        # Dibujar calles y flechas de dirección
        self.dibujar_calles()
        self.dibujar_flechas()

        # Dibujar intersecciones
        for interseccion in intersecciones:
            self.dibujar_semaforos(interseccion)

        # Dibujar autos
        for auto in autos:
            self.dibujar_auto(auto)