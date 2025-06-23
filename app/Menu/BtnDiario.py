import flet as ft
import datetime
import sqlite3

import sys
import os


from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo, obtener_datos_subgrupo, mostrar_cuentas_por_grupo_flet
#from app.Menu.BtnDiario import boton__diario


ruta_BDapp = globals.ruta_BD


def boton__diarioSimple(e):
    """
    Función que se ejecuta al hacer clic en el botón "Diario".
    """
    #ruta_BDapp = globals.ruta_BD
    
    '''
    def ver_4columnas(e):
        #contenido_cuerpo_container.content = ft.Text("menu MOSTRAR TABLA CÓDIGO", size=20)
        #e.page.update()
        contenido_verTablasCodigos = submenu_4_columnas(e.page)
        globals.contenido_central_container.content = contenido_verTablasCodigos
        e.page.update()



    def crear_Grupo(e):
        contenido_grupo = submenu_Grupos(e.page)
        globals.contenido_central_container.content = contenido_grupo
        e.page.update()

    def crear_Subgrupo(e):
        #contenido_cuerpo_container.content = ft.Text("menu MOSTRAR SUBGRUPOS", size=20)
        contenido_subgrupos = submenu_Subgrupos(e.page)
        globals.contenido_central_container.content = contenido_subgrupos
        e.page.update()

    def crear_Cuenta(e):
        globals.contenido_central_container.content = ft.Text("desde menu CUENTAS", size=20)
        #contenido_cuentas = submenu_Cuentas(e.page)
        #contenido_cuerpo_container.content = contenido_cuentas
        e.page.update()
        '''

    # -----------------------------------------  SUBMENU  -----------------------------------------
    # Definición de los botones del submenú    
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Asiento Simple",
                    #on_click=ver_4columnas,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Asiento Múltiple",
                    #on_click=crear_Grupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Importar datos Excel",
                    #on_click=crear_Subgrupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Modificar Asiento",
                    #on_click=crear_Cuenta,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        ),
        bgcolor=ft.Colors.LIGHT_BLUE_50,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # ----------------------  Estructura principal -----------------
    globals.contenido_central_container.content = ft.Column(
        controls=[
            submenu,  # Submenú siempre visible
            
        ],
        expand=True,
        spacing=10,  # separacion entre el submenú y el contenido

    )
    return globals.contenido_central_container.content

    


def proves3():
        
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 4)

    botonesDiario = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        #bgcolor=ft.Colors.BLUE_GREY_200,
        margin=ft.margin.only(top=20) 
    )
    
    contenidoDiario = ft.Container(
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
                botonesDiario,
                contenidoDiario,

            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
    











