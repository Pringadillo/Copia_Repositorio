import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from data.funciones_BD import  ruta_BD, obtener_opciones_nivel1_desde_bd

def submenu_crear_codigo(page: ft.Page):
    opciones_nivel1 = obtener_opciones_nivel1_desde_bd()

    desplegable_nivel1 = ft.Dropdown(
        label="Grupo",
        options=opciones_nivel1,
        on_change=lambda ev: print(f"Nivel 1 seleccionado: {ev.control.value}"),
        width=300,
    )

    texto1 = ft.Row(
        [
            ft.Text(  # Corrección: El texto va como primer argumento posicional
                "Crear nuevo Código",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=200,
    )

    texto2 = ft.Row(
        [
            desplegable_nivel1,
            ft.TextButton(
                text="Grupo",
                on_click=lambda e: submenu_ver_codigo(page),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    texto3 = ft.Row(
        [
            ft.Text(  # Corrección: El texto va como primer argumento posicional
                "Modificar",
                size=20,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    submenu_crear_codigo_container = ft.Container(  # Renombrado para claridad
        content=ft.Column(
            controls=[
                texto1,
                texto2,
                texto3,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.top_left,
    )
    return submenu_crear_codigo_container
    
  

def submenu_ver_codigo(e):
    # Aquí puedes importar la función que crea el desplegable de nivel 1
    #from ui_elements import crear_desplegable_nivel1
    #desplegable_nivel1 = crear_desplegable_nivel1()
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Contenido Dinámico", size=20),
        bgcolor=ft.colors.RED_200, expand=1)  # 1/5 del espacio

    e.page.update()

def submenu_modificar_codigo(e):
    # Aquí puedes importar la función que crea el desplegable de nivel 1
    #from ui_elements import crear_desplegable_nivel1
    #desplegable_nivel1 = crear_desplegable_nivel1()
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Contenido Dinámico", size=20),
        bgcolor=ft.colors.RED_200, expand=1)  # 1/5 del espacio

    e.page.update()

def submenu_eliminar_codigo(e):
    # Aquí puedes importar la función que crea el desplegable de nivel 1
    #from ui_elements import crear_desplegable_nivel1
    #desplegable_nivel1 = crear_desplegable_nivel1()
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Contenido Dinámico", size=20),
        bgcolor=ft.colors.RED_200, expand=1)  # 1/5 del espacio

    e.page.update()