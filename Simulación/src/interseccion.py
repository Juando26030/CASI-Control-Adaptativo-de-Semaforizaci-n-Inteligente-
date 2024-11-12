from src.semaforo import Semaforo


class Interseccion:
    def __init__(self, posicion):
        self.posicion = posicion  # Centro de la intersección
        self.semaforos = self.crear_semaforos()
        self.autos_en_espera = []

    def crear_semaforos(self):
        """
        Crea los semáforos en las posiciones correctas para controlar los carriles.
        """
        desplazamiento = 60
        centro_x, centro_y = self.posicion

        # Definimos los semáforos para cada grupo de carriles
        semaforos = {
            "norte": Semaforo((centro_x - desplazamiento, centro_y - 120)),  # Carriles 1-2
            "este": Semaforo((centro_x + 120, centro_y - desplazamiento)),  # Carriles 5-6
            "sur": Semaforo((centro_x + desplazamiento, centro_y + 120)),  # Carriles 9-10
            "oeste": Semaforo((centro_x - 120, centro_y + desplazamiento))  # Carriles 13-14
        }
        return semaforos

    def actualizar_flujo_trafico(self):
        """
        Actualiza los datos de tráfico para cada semáforo.
        """
        for semaforo in self.semaforos.values():
            semaforo.datos_sensores = len(self.autos_en_espera)

    def reportar_datos_sensores(self):
        """
        Devuelve los datos de tráfico de todos los semáforos.
        """
        return {ubicacion: semaforo.datos_sensores for ubicacion, semaforo in self.semaforos.items()}
