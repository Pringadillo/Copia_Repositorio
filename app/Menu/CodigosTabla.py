import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from data.funciones_BD import ruta_BD, obtener_opciones_nivel1_desde_bd
#from ..Submenu import FuncionesTablaCodigo
from ..Submenu.FuncionesTablaCodigo import submenu_ver_codigo, submenu_crear_codigo 

def menu_TablaCodigos():
    # Contenedor dinámico para el contenido_cuerpo
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Seleccione una opción del submenú", size=30, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        expand=True,  # Haz que el contenedor se expanda dentro de la Column
    )

    def ver_TablaCodigos(e):
        contenido_cuerpo_container.content = ft.Text("MOSTRAR TABLA CÓDIGO", size=20)
        e.page.update()

    def crear_codigo(e):
        nuevo_contenido = submenu_crear_codigo(e.page)
        contenido_cuerpo_container.content = nuevo_contenido
        e.page.update()

    def actualizar_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Actualizar Código", size=20)
        e.page.update()

    def eliminar_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Eliminar Código", size=20)
        e.page.update()

    # Submenú CRUD de la tabla código
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Ver Tabla Códigos",
                    icon=ft.icons.TABLE_CHART,
                    on_click=ver_TablaCodigos,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Crear Código",
                    icon=ft.icons.ADD,
                    on_click=crear_codigo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Actualizar Código",
                    icon=ft.icons.EDIT,
                    on_click=actualizar_codigo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Eliminar Código",
                    icon=ft.icons.DELETE,
                    on_click=eliminar_codigo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        ),
        bgcolor=ft.colors.LIGHT_BLUE_50,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # Estructura principal que incluye el submenú y el contenido dinámico
    cuerpo = ft.Column(
        controls=[
            submenu,  # Submenú siempre visible
            contenido_cuerpo_container,
        ],
        expand=True,
        spacing=10,  # separacion entre el submenú y el contenido

    )
    return cuerpo



