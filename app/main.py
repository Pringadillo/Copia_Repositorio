import flet as ft
import pandas as pd
import sqlite3
import os
import pathlib



#rutas del programa
ruta_imagenes = "./imagenes/"
ruta_datos = "./data/"
ruta_funciones = "./app/"

# base_datos = "./data/{nombre_BD}"



# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()




def main(page: ft.Page):

    #parametros entorno



    texto = ft.Text(value="¡Hola, Flet!")
    boton = ft.ElevatedButton(text="Haz clic")

    def boton_clic(e):
        texto.value = "¡Botón clicado!"
        page.update()

    boton.on_click = boton_clic

    page.add(texto, boton)



ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
