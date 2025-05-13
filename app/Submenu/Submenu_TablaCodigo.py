import flet as ft
import datetime
import sqlite3

import sys
import os

import globals
from app.data.funciones_BD import mostrar_datos_grupo



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
    datos_nivel1 = mostrar_datos_grupo()

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
    # Llama a ver_tabla_nivel1 para obtener los datos    
    opciones_nivel1 = mostrar_datos_grupo()

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
    texto1 = ft.Row(
        [
            ft.Text(
                "TABLA DE CÓDIGOS",
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
    alignment=ft.MainAxisAlignment.SPACE_AROUND,
    controls=[
        ft.Container(
            expand=True,  # Hace que la columna ocupe espacio igualitario
            content=ft.Column(
                [
                    ft.Text("CUENTAS FINANCIERAS", weight=ft.FontWeight.BOLD),
                    # Aquí irían los códigos de nivel 2 y 3 relacionados con Activo
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.GREEN_100,
            padding=10,
            border_radius=ft.border_radius.all(5),
        ),
        ft.VerticalDivider(),
        ft.Container(
            expand=True,  # Hace que la columna ocupe espacio igualitario
            content=ft.Column(
                [
                    ft.Text("DEUDAS", weight=ft.FontWeight.BOLD),
                    # Aquí irían los códigos de nivel 2 y 3 relacionados con Pasivo
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.RED_100,
            padding=10,
            border_radius=ft.border_radius.all(5),
        ),
        ft.VerticalDivider(),
        ft.Container(
            expand=True,  # Hace que la columna ocupe espacio igualitario
            content=ft.Column(
                [
                    ft.Text("GASTOS", weight=ft.FontWeight.BOLD),
                    # Aquí irían los códigos de nivel 2 y 3 relacionados con Gastos
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.ORANGE_100,
            padding=10,
            border_radius=ft.border_radius.all(5),
        ),
        ft.VerticalDivider(),
        ft.Container(
            expand=True,  # Hace que la columna ocupe espacio igualitario
            content=ft.Column(
                [
                    ft.Text("INGRESOS", weight=ft.FontWeight.BOLD),
                    # Aquí irían los códigos de nivel 2 y 3 relacionados con Ingresos
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.BLUE_100,
            padding=10,
            border_radius=ft.border_radius.all(5),
        ),
    ],
    )

    
    submenu_crear_codigo_container = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.colors.WHITE,
        alignment=ft.alignment.top_left,  # Alineación del contenedor en la parte superior izquierda
    )
    return submenu_crear_codigo_container    
