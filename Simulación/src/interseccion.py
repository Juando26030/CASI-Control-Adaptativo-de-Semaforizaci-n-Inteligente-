from src.semaforo import Semaforo

# Clase Interseccion para gestionar una intersección con varios semáforos
class Interseccion:
    def __init__(self, id, config_semaforo):
        """
        Inicializa una intersección con varios semáforos según la configuración JSON.

        :param id: Identificador de la intersección
        :param config_semaforo: Configuración de tiempos para los semáforos
        """
        self.id = id

        # Posiciones de cada semáforo en la intersección
        posiciones = {
            "norte": (self.id[0], self.id[1] - 100),  # 100 píxeles al norte del centro de la intersección
            "sur": (self.id[0], self.id[1] + 100),
            "este": (self.id[0] + 100, self.id[1]),
            "oeste": (self.id[0] - 100, self.id[1])
        }

        # Asignar configuración de tiempos según dirección
        self.semaforos = {}
        for direccion, posicion in posiciones.items():
            if direccion in ["norte", "sur"]:
                tiempos = config_semaforo["norte_sur"]
            else:
                tiempos = config_semaforo["este_oeste"]
            self.semaforos[direccion.lower()] = Semaforo(direccion, tiempos, posicion)

    def actualizar_semaforos(self):
        """
        Actualiza el estado de cada semáforo en la intersección.
        """
        for semaforo in self.semaforos.values():
            semaforo.actualizar_estado()

    def reportar_datos_sensores(self):
        """
        Simula la recopilación de datos de los sensores en la intersección.
        """
        return {"norte": 5, "sur": 3, "este": 7, "oeste": 4}
