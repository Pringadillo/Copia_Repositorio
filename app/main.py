import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib
import json
import tempfile

import appbar
import cuerpo

'''
# Variables Globales¿?¿?
 ruta_imagenes= "./imagenes/"
 empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
 usuario = "Usuario"  # Nombre del usuario

'''



def main(page: ft.Page):
    page.title = "Cuentas de Casa"
    #page.icon = "/imagenes/"
    page.appbar = appbar.crear_appbar(page)
    page.add(cuerpo.crear_cuerpo())


ft.app(target=main)