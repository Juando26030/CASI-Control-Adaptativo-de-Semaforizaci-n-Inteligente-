import json
import pandas as pd

def cargar_configuracion(filepath):
    with open(filepath, 'r') as file:
        config = json.load(file)
    return config

def cargar_datos_csv(filepath):
    return pd.read_csv(filepath)
