import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib
import json
import tempfile

import appbar
import cuerpo
import barra_lateral  # Importamos el contenido de la barra lateral

'''
# Variables Globales
ruta_imagenes = "./imagenes/"
empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
usuario = "Usuario"  # Nombre del usuario
'''


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

    # Crear la columna central (contenido dinámico)
    contenido_actual = ft.Text("Contenido inicial")  # Contenido inicial
    contenido_central = ft.Column(
        controls=[
            cuerpo.crear_cuerpo(page, contenido_actual)  # Pasar los argumentos requeridos
        ],
        expand=True
    )

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