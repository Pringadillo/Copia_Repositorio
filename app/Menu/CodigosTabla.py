import flet as ft
import datetime
import sqlite3

import sys
import os

import globals


from app.Submenu.Submenu_TablaCodigo import submenu_Grupos, submenu_Subgrupos, submenu_Cuentas, submenu_4_columnas



def menu_TablaCodigos():


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

    # -----------------------------------------  SUBMENU  -----------------------------------------
    # Definición de los botones del submenú    
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Tabla de Códigos",
                    on_click=ver_4columnas,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Grupos",
                    on_click=crear_Grupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Subgrupos",
                    on_click=crear_Subgrupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Cuentas",
                    on_click=crear_Cuenta,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        ),
        bgcolor=ft.colors.LIGHT_BLUE_50,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # ----------------------  Estructura principal -----------------
    cuerpo = ft.Column(
        controls=[
            submenu,  # Submenú siempre visible
            globals.contenido_central_container,
        ],
        expand=True,
        spacing=10,  # separacion entre el submenú y el contenido

    )
    return cuerpo


