import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from data.funciones_BD import *
from data.funciones_BD import ver_tabla_nivel1

def submenu_Grupos(e):
    texto1 = ft.Row(
        [
            ft.Text(
                "No se pueden modificar los GRUPOS",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLUE_900,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=100,
    )

    # Llama a ver_tabla_nivel1 para obtener los datos
    datos_nivel1 = ver_tabla_nivel1()

    # Convierte los datos en un solo texto para mostrar en texto2
    texto2 = ft.Row(
        [
            ft.Text(
                "\n".join(datos_nivel1),  # Une las líneas con saltos de línea
                size=20,
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.LEFT,
                color=ft.colors.BLACK,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=200,
    )

    texto3 = ft.Row(
        [
            ft.Text(
                "GRUPOS DE CUENTAS",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLUE_900,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=100,
    )

    submenu_crear_codigo_container = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto3,
                texto2,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.top_left,
    )
    return submenu_crear_codigo_container
    
def submenu_Subgrupos(e):
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
                "TEXTO PARA SUBGRUPOS",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLUE_900,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=100,
    )

    submenu_crear_codigo_container = ft.Container(  # Renombrado para claridad
        content=ft.Column(
            controls=[
                texto1,
                desplegable_nivel1,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.top_left,
    )
    return submenu_crear_codigo_container

def submenu_Cuentas(e):
    texto1 = ft.Row(
        [
            ft.Text(  # Corrección: El texto va como primer argumento posicional
                "TEXTO PARA CUENTAS",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLUE_900,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=100,
    )


    submenu_crear_codigo_container = ft.Container(  # Renombrado para claridad
        content=ft.Column(
            controls=[
                texto1,
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

