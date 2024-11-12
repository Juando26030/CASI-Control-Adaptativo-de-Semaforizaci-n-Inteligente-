import json
import os

import pandas as pd
import pygame


class Utils:
    def cargar_configuracion(filepath):
        with open(filepath, 'r') as file:
            config = json.load(file)
        return config

    def cargar_datos_csv(filepath):
        return pd.read_csv(filepath)

    def cargar_imagen(nombre_imagen):
        # Cargar la imagen desde la carpeta 'assets/images'
        ruta = os.path.join("assets", "images", nombre_imagen)
        return pygame.image.load(ruta).convert_alpha()

