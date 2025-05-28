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



    texto1 = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center, # <--- Centra el contenido (texto1_content) dentro del Container
        #expand=True, # <--- Hace que el Container se expanda para ocupar el ancho disponible
        # Puedes añadir un color de fondo temporal para ver los límites del contenedor
        bgcolor=ft.Colors.BLUE_GREY_200
    )




    texto2 = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Título Columna 1", weight=ft.FontWeight.BOLD),
                            ft.Text("Contenido de la columna 1. Puedes poner varios elementos aquí."),
                        ],
                        alignment=ft.MainAxisAlignment.START, # Align content within this column vertically
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Center content horizontally within this column
                        expand=True # Make this column expand to take available width
                    ),
                    ft.VerticalDivider(), # Optional: Add a visual separator between columns
                    ft.Column(
                        controls=[
                            ft.Text("Título Columna 2", weight=ft.FontWeight.BOLD),
                            ft.Text("Contenido de la columna 2."),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),
                    ft.VerticalDivider(),
                    ft.Column(
                        controls=[
                            ft.Text("Título Columna 3", weight=ft.FontWeight.BOLD),
                            ft.Text("Contenido de la columna 3."),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),
                    ft.VerticalDivider(),
                    ft.Column(
                        controls=[
                            ft.Text("Título Columna 4", weight=ft.FontWeight.BOLD),
                            ft.Text("Contenido de la columna 4."),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND, # Distribute space evenly around columns
                vertical_alignment=ft.CrossAxisAlignment.START, # Align columns at the top
                wrap=False, # Prevent columns from wrapping to the next line if space is limited
                expand=True # Make the Row itself expand within the Container
            ),
            alignment=ft.alignment.center, # Center the Row within the Container
            bgcolor=ft.Colors.BLUE_GREY_200,
            padding=10, # Add some padding around the content
            expand=True # Make the container itself expand
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






