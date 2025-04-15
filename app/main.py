import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib
import json
import tempfile

import appbar2
import cuerpo2

'''
# Variables Globales¿?¿?
 ruta_imagenes= "./imagenes/"
 empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
 usuario = "Usuario"  # Nombre del usuario
contenido_actual = None
'''



# Variable global para el contenido dinámico
contenido_actual = None

def actualizar_cuerpo(page: ft.Page, nuevo_contenido):
    """Actualiza el contenido del cuerpo dinámicamente."""
    global contenido_actual
    contenido_actual = nuevo_contenido
    page.controls.clear()  # Limpia el contenido actual
    page.add(cuerpo2.crear_cuerpo(page, contenido_actual))  # Agrega el nuevo contenido
    page.update()

def main(page: ft.Page):
    page.title = "Cuentas de Casa"
    #page.icon = "/imagenes/"
    
    page.appbar = appbar2.crear_appbar(page, actualizar_cuerpo)  # Pasar la función de actualización
    page.add(cuerpo2.crear_cuerpo(page, contenido_actual))  # Inicializa el cuerpo vacío
    page.update()


ft.app(target=main)