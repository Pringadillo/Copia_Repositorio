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
import barra_lateral  # Importamos el contenido de la barra lateral

from data import funciones_BD




# Variables Globales
empresa = "TEST_100"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"


#crear la Base de Datos
funciones_BD.Crear_Tablas()
funciones_BD.Insertar_Datos_Iniciales()
funciones_BD.mostrar_datos_cuentas()



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




