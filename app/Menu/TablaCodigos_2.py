import flet as ft
import datetime
import sqlite3

import sys
import os

import globals



def proves2():
    ruta_BDapp = globals.ruta_BD

    Columna1 = ft.Column(
        
    )
    Columna2 = ft.Column()
    Columna3 = ft.Column()
    Columna4 = ft.Column()


    
    
    aaa = ft.Text("TABLA DE CÓDIGOS", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    texto1 = ft.Container(
        content=aaa,
        alignment=ft.alignment.center, # <--- Centra el contenido (texto1_content) dentro del Container
        #expand=True, # <--- Hace que el Container se expanda para ocupar el ancho disponible
        # Puedes añadir un color de fondo temporal para ver los límites del contenedor
        bgcolor=ft.Colors.BLUE_GREY_200
    )
    texto2 = ft.Container(
        content=aaa,
        alignment=ft.alignment.center, # <--- Centra el contenido (texto1_content) dentro del Container
        #expand=True, # <--- Hace que el Container se expanda para ocupar el ancho disponible
        # Puedes añadir un color de fondo temporal para ver los límites del contenedor
        bgcolor=ft.Colors.BLUE_GREY_200
    )


    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            #alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content



def proves3():
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






    
    # ----------------------  Estructura principal -----------------
    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content






