import math

class Auto:
    def __init__(self, posicion, velocidad, direccion, carril_origen, carril_destino, puede_girar=False):
        self.posicion = posicion
        self.velocidad = velocidad
        self.direccion = direccion
        self.carril_origen = carril_origen
        self.carril_destino = carril_destino
        self.puede_girar = puede_girar
        self.ya_giro_una_vez = False

    def mover(self):
        rad = math.radians(self.direccion)
        self.posicion[0] += self.velocidad * math.cos(rad)
        self.posicion[1] += self.velocidad * math.sin(rad)

        centro_interseccion = (400, 300)
        margen_giro = 90
        margen_centro = 10

        # Girar en los bordes de la intersección
        if self.puede_girar and not self.ya_giro_una_vez:
            if abs(self.posicion[0] - centro_interseccion[0]) < margen_giro or abs(self.posicion[1] - centro_interseccion[1]) < margen_giro:
                self.direccion = (self.direccion + 90) % 360
                self.ya_giro_una_vez = True

        # Ajustar dirección en el centro
        if abs(self.posicion[0] - centro_interseccion[0]) < margen_centro and abs(self.posicion[1] - centro_interseccion[1]) < margen_centro:
            self.direccion = {12: 90, 16: 180, 4: 270, 8: 0}.get(self.carril_destino, self.direccion)

    def en_interseccion(self):
        """
        Retorna True si el auto está en el área central de la intersección.
        """
        centro_x, centro_y = 400, 300
        margen = 100  # Tamaño de la intersección
        return (
            centro_x - margen < self.posicion[0] < centro_x + margen and
            centro_y - margen < self.posicion[1] < centro_y + margen
        )
