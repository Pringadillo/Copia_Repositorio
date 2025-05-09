import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib
import json
import tempfile
import sys




# Archivos estructura del codigo
import appbar
import cuerpo
import barra_lateral  # Importamos el contenido de la barra lateral

import globals
from data import funciones_BD



# Crear la Base de Datos si no existe
funciones_BD.Crear_Tablas(globals.ruta_BD)


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

    # Crear la Base de Datos si no existe
    funciones_BD.Crear_Tablas(globals.ruta_BD)
    



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