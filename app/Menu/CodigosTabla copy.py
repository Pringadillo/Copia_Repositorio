import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from data.funciones_BD import  ruta_BD, obtener_opciones_nivel1_desde_bd

from ..Submenu import FuncionesTablaCodigo



def menu_TablaCodigos():
    # Contenedor dinámico para el contenido_cuerpo
    contenido_cuerpo_container = ft.Row(
            [
                ft.Container(
                    content=ft.Text("Contenido Dinámico", size=20),
                    bgcolor=ft.colors.RED_200, expand=1),  # 1/5 del espacio
                ft.Container(
                    content=ft.Text("Seleccione una opción del submenú", size=30,),
                    bgcolor=ft.colors.BLUE_200, expand=12), # 3/5 del espacio
                    #height=200  # Una altura mayor para este contenedor

                    
                ft.Container(
                    content=ft.Text("Contenido Dinámico", size=20),
                    bgcolor=ft.colors.GREEN_200, expand=1), # 1/5 del espacio
            ],
            expand=True,  # Haz que la fila se expanda para llenar el contenedor padre
        )
    
    def ver_TablaCodigos(e):
        
        ver_la_TablaCodigos= FuncionesTablaCodigo.submenu_ver_codigo(e)
        contenido_cuerpo_container.content = ver_la_TablaCodigos
        e.page.update()

    def crear_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Crear Código", size=20)
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
            ft.Container(
                content=contenido_cuerpo_container,
                alignment=ft.alignment.center, # Centra contenido_cuerpo_container
               
            ),
        ],
        expand=True,
        spacing=10, #separacion entre el submenú y el contenido
        
        )
    return cuerpo

