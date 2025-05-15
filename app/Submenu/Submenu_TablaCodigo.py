import flet as ft
import datetime
import sqlite3

import sys
import os

from app import globals
from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo

#ruta_BDapp = globals.ruta_BD

def submenu_Grupos(e):
    ruta_BDapp = globals.ruta_BD
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
    datos_nivel1 = obtener_datos_grupo(ruta_BDapp)
    # Extrae solo el segundo elemento (el texto) de cada tupla
    textos_nivel1 = [f"{item[0]}   {item[1]}" for item in datos_nivel1]

    # Convierte los datos en un solo texto para mostrar en texto2
    texto2 = ft.Row(
        [
            ft.Text(
                "\n".join(textos_nivel1),  # Une la lista de textos
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
        ruta_BDapp = globals.ruta_BD
        # Llama a obtener_datos_grupo para obtener los datos (lista de tuplas)
        opciones_nivel1_tuplas = obtener_datos_grupo(ruta_BDapp)

        # Transforma la lista de tuplas en una lista de objetos ft.dropdown.Option
        opciones_nivel1 = [
            ft.dropdown.Option(key=str(grupo_id), text=f"{grupo_id}  {nombre_grupo}")
            for grupo_id, nombre_grupo in opciones_nivel1_tuplas
        ]

        desplegable_nivel1 = ft.Dropdown(
            label="Grupo",
            options=opciones_nivel1,
            on_change=lambda ev: mostrar_subgrupos(ev.control.value, columna_subgrupos),
            width=200,  # Ajusta el ancho según necesites
        )

        columna_subgrupos = ft.Column(
            controls=[
                ft.Text("Subgrupos:", weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona un grupo"),  # Texto inicial
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        columna_botones = ft.Column(
            controls=[
                ft.ElevatedButton("Crear"),
                ft.ElevatedButton("Editar"),
                ft.ElevatedButton("Eliminar"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        submenu_crear_codigo_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(controls=[ft.Text("Selecciona Grupo:", weight=ft.FontWeight.BOLD), desplegable_nivel1], horizontal_alignment=ft.CrossAxisAlignment.START, width=200),
                    ft.Container(content=columna_subgrupos, width=300, padding=10), # Contenedor para dar espacio
                    ft.Column(controls=[ft.Text("Acciones:", weight=ft.FontWeight.BOLD), columna_botones], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=150),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND, # Distribuye las columnas
            ),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.top_left,
            padding=20, # Añade un poco de espacio alrededor del contenido
        )
        return submenu_crear_codigo_container

        def mostrar_subgrupos(grupo_id, columna_subgrupos: ft.Column):
            ruta_BDapp = globals.ruta_BD
            # Aquí deberías tener una función que obtenga los subgrupos basados en el grupo_id
            subgrupos = obtener_subgrupos_por_grupo(ruta_BDapp, grupo_id)
            columna_subgrupos.controls = [ft.Text("Subgrupos:", weight=ft.FontWeight.BOLD)] + [ft.Text(subgrupo) for subgrupo in subgrupos]
            columna_subgrupos.update()

        # Placeholder para la función que obtendría los subgrupos de la base de datos
        def obtener_subgrupos_por_grupo(ruta_bd, grupo_id):
            # Aquí iría tu lógica para consultar la base de datos y obtener los subgrupos
            # relacionados con el grupo_id.
            # Por ahora, devolvemos una lista de ejemplo.
            return [f"Subgrupo A del Grupo {grupo_id}", f"Subgrupo B del Grupo {grupo_id}", f"Subgrupo C del Grupo {grupo_id}"]

def submenu_Cuentas(e):
    ruta_BDapp = globals.ruta_BD

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
    ruta_BDapp = globals.ruta_BD

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
