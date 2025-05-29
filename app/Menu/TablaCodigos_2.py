import flet as ft
import datetime
import sqlite3

import sys
import os

import globals
from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo, obtener_datos_subgrupo

def proves2():
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    datos_nivel1 = obtener_datos_grupo(ruta_BDapp)
    # Extrae solo el segundo elemento (el texto) de cada tupla
    textos_nivel1 = [f"{item[0]}   {item[1]}" for item in datos_nivel1]


    texto1 = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        #bgcolor=ft.Colors.BLUE_GREY_200,
        margin=ft.margin.only(top=20) 
    )

    texto2 = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("CUENTAS FINANCIERAS", weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER),
                            ft.Text("• Cuenta Corriente\n• Cuenta de Ahorro\n• Inversiones"),
                            
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("DEUDAS", weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Tarjeta de Crédito\n• Préstamo Hipotecario\n• Préstamo Personal"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("GASTOS", weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Alquiler/Hipoteca\n• Alimentación\n• Transporte\n• Servicios"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("INGRESOS", weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Salario\n• Freelance\n• Intereses/Dividendos"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True
        ),
        padding=10,
        expand=True
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






