import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

#from data.funciones_BD import *
from data.funciones_BD import ver_tabla_nivel1, obtener_opciones_nivel1_desde_bd

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
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.top_left,  # Alineación del contenedor en la parte superior izquierda
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
                "SUBGRUPOS DE CUENTAS",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.BLUE_900,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        height=100,
    )

    texto2 = ft.Row(
        [
            ft.Text(
                "Selecciona un grupo para ver sus subgrupos",
                size=20,
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Subgrupo de códigos a partir de la opción escogida en el desplegable
    texto3 = ft.Row(
        [
            ft.Text(
                "Selecciona un Subgrupo para ver sus cuentas",
                size=20,
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    texto4 = ft.Row(
        [
            ft.Text(
                "Selecciona una cuenta para ver su detalle",
                size=20,
                weight=ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    submenu_crear_codigo_container = ft.Container(  # Renombrado para claridad
        content=ft.Column(
            controls=[
                texto1,
                texto2,
                desplegable_nivel1,
                texto3,
                #desplegable_nivel2,
                texto4,
                #desplegable_nivel3,
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
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

def submenu_4_columnas(e):
    # Obtén los datos de los subgrupos y cuentas desde la base de datos
    grupos = obtener_opciones_nivel1_desde_bd()  # Supongamos que esta función devuelve los grupos
    columnas = []

    # Genera las columnas dinámicamente
    for grupo in grupos:
        # Obtén los subgrupos y cuentas para cada grupo
        subgrupos_y_cuentas = ver_tabla_nivel1()  # Reemplaza con la función adecuada para obtener los datos

        # Crea una columna con los datos del grupo
        columna = ft.Column(
            controls=[
                ft.Text(
                    f"Grupo: {grupo}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_900,
                ),
                ft.Text(
                    "\n".join(subgrupos_y_cuentas),  # Une los subgrupos y cuentas con saltos de línea
                    size=16,
                    weight=ft.FontWeight.NORMAL,
                    color=ft.colors.BLACK,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=1,  # Expande la columna uniformemente
        )
        columnas.append(columna)

    # Crea un contenedor con las 4 columnas distribuidas uniformemente
    contenido_cuerpo_container = ft.Container(
        content=ft.Row(
            controls=columnas,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # Distribuye uniformemente las columnas
        ),
        bgcolor=ft.colors.WHITE,
        expand=1,
    )

    # Actualiza la página con el nuevo contenido
    e.page.controls.clear()
    e.page.controls.append(contenido_cuerpo_container)
    e.page.update()