
import os
import sys


# Agregar el directorio raíz al PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

# Otras variables globales
empresa = "TEST_100"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
usuario = "Nombre KKKK & K"

