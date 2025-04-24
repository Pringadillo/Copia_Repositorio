import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from data.funciones_BD import  ruta_BD, obtener_opciones_nivel1_desde_bd


'''
En este archivo debe ir el código para crear la tabla de códigos
y el CRUD correspondiente.
'''



# Aquí puedes importar la función que crea el desplegable de nivel 1
#from ui_elements import crear_desplegable_nivel1
#desplegable_nivel1 = crear_desplegable_nivel1()





def ver_TablaCodigos(e):
    opciones_nivel1 = obtener_opciones_nivel1_desde_bd()

    desplegable_nivel1 = ft.Dropdown(
            label="Selecciona Grupo",
            options=opciones_nivel1,
            on_change=lambda ev: print(f"Nivel 1 seleccionado: {ev.control.value}"),
            width=300,
        )

        # Aquí puedes importar la función que crea el desplegable de nivel 1
        #from ui_elements import crear_desplegable_nivel1
        #desplegable_nivel1 = crear_desplegable_nivel1()
    
    
    submenu_verTablaCodigo = ft.Container(
            content=desplegable_nivel1,
            alignment=ft.alignment.top_left,  # Ejemplo de nueva alineación
        )
    e.page.update()
    return submenu_verTablaCodigo
  



