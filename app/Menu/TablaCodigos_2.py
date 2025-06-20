import flet as ft
import datetime
import sqlite3

import sys
import os

import globals
from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo, obtener_datos_subgrupo, mostrar_cuentas_por_grupo_flet

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
                            ft.Text(textos_nivel1[0], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER),
                            ft.Container(
                                content=ft.Text(textos_nivel1),
                                #ft.Text("• Cuenta Corriente\n• Cuenta de Ahorro\n• Inversiones"),
                            )
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
                            ft.Text(textos_nivel1[1], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
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
                            ft.Text(textos_nivel1[2], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
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
                            ft.Text(textos_nivel1[3], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
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

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 4)

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
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
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
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
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
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
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
    






