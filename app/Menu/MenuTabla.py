import flet as ft
import datetime
import sqlite3
#import globals
import sys
import os




# Obtiene la ruta absoluta del directorio padre de 'app/Menu' (que es la raíz del proyecto)
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ruta_raiz)

from app import globals
#from app.Submenu import SubmenuTablaCodigo 
from app.Submenu.SubmenuTablaCodigo import submenu_4_columnas, submenu_Grupos, submenu_Subgrupos, submenu_Cuentas


'''
para comprobar si existen los modulos'
ruta_bd = globals.ruta_BD  # Importamos la ruta de la base de datos desde globals.py
print(ruta_bd)
print(ruta_raiz)
print(globals.ruta_BD)
'''

ruta_bd = globals.ruta_BD  # Importamos la ruta de la base de datos desde globals.py

def menu_TablaCodigos(ruta_bd): # Añadimos ruta_bd como argumento
    ruta_bd = globals.ruta_BD  # Importamos la ruta de la base de datos desde globals.py

    # Contenedor dinámico para el contenido_cuerpo
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Seleccione una opción del submenú", size=30, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.top_center,
        expand=True,  # Haz que el contenedor se expanda dentro de la Column
    )

    def ver_TablaCodigos(e):
        # Borra el contenido actual del contenedor
        contenido_cuerpo_container.content = None
        e.page.update() 
        contenido_verTablasCodigos = submenu_4_columnas(e.page, ruta_bd) # Pasar ruta_bd
        contenido_cuerpo_container.content = contenido_verTablasCodigos
        e.page.update()

    def crear_Grupo(e):
        contenido_grupo = submenu_Grupos(e.page, ruta_bd) # Pasar ruta_bd
        contenido_cuerpo_container.content = contenido_grupo
        e.page.update()

    def crear_Subgrupo(e):
        contenido_subgrupos = submenu_Subgrupos(e.page, ruta_bd) # Pasar ruta_bd
        contenido_cuerpo_container.content = contenido_subgrupos
        e.page.update()

    def crear_Cuenta(e):
        contenido_cuentas = submenu_Cuentas(e.page, ruta_bd) # Pasar ruta_bd
        contenido_cuerpo_container.content = contenido_cuentas
        e.page.update()

    # -----------------------------------------  SUBMENU  -----------------------------------------
    # Definición de los botones del submenú
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Tabla de Códigos",
                    on_click=ver_TablaCodigos,
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
            contenido_cuerpo_container,
        ],
        expand=True,
        spacing=10,  # separacion entre el submenú y el contenido

    )
    return cuerpo




