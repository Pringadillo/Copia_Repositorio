import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib
import json
import tempfile
import sys


# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Archivos estructura del codigo
import appbar
import cuerpo
import barra_lateral
import globals  # Importamos las variables globales

import data.funciones_BD as funciones_BD
# Arxivos menu
#import app.Menu.CodigosTabla as CodigosTabla


nombre_empresa=globals.empresa
ruta_BDapp =globals.ruta_BD


def existe_base_de_datos(ruta_BDapp):
    """
    Verifica si un archivo de base de datos SQLite existe en la ruta especificada.

    Args:
        ruta_db (str): La ruta completa al archivo de la base de datos.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    return os.path.exists(ruta_BDapp)


if existe_base_de_datos(ruta_BDapp):
        print(f"La base de datos '{ruta_BDapp}' existe.")
        try:
            conn = sqlite3.connect(ruta_BDapp)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
else:
        print(f"La base de datos '{ruta_BDapp}' NO EXISTE.")
        funciones_BD.crear_base_datos(ruta_BDapp)
        funciones_BD.crear_tabla_GRUPOS(ruta_BDapp)
        funciones_BD.crear_tabla_SUBGRUPOS(ruta_BDapp)
        funciones_BD.crear_tabla_CUENTAS(ruta_BDapp)
        # insertar datos iniciales
        funciones_BD.insertar_datos_iniciales(ruta_BDapp)

    

    





def main(page: ft.Page):
    page.title = "Cuentas de Casa"
    
    # Crear e inicializar el SnackBar
    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        action="Cerrar"
    )

    # Crear la AppBar
    page.appbar = appbar.crear_appbar(page)  # Contenido definido en appbar.py

    # Crear la barra lateral izquierda
    barra_lateral_contenido = barra_lateral.crear_barra_lateral(page)

    # Crear el contenido central
    contenido = cuerpo.contenido_por_defecto  # Contenido a mostrar por defecto
    contenido_central = cuerpo.crear_cuerpo(page, contenido)



    # Estructura principal de la página
    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=barra_lateral_contenido,
                    width=250,  # Ancho de la barra lateral
                    bgcolor=ft.Colors.BLUE_GREY_50,
                ),
                ft.Container(
                    content=contenido_central,
                    expand=True,  # La columna central ocupa el espacio restante
                    bgcolor=ft.Colors.WHITE,
                ),
            ],
            expand=True,
        )
    )

    page.update()


ft.app(target=main)