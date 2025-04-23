import flet as ft
import datetime

import appbar


contenido_por_defecto = ft.Text("Contenido inicial por defecto")  # Contenido a mostrar por defecto


def crear_cuerpo(page, contenido_a_mostrar):
    # Devuelve un contenedor con el contenido dinámico
    return ft.Container(
        content=contenido_a_mostrar,
        bgcolor=ft.colors.LIGHT_BLUE_50,
        padding=10,
        expand=True
    )


