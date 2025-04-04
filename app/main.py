import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib


import appbar
import cuerpo

def main(page: ft.Page):
    page.title = "Mi Aplicación Flet"
    page.appbar = appbar.crear_appbar(page)
    page.add(cuerpo.crear_cuerpo())


ft.app(target=main)