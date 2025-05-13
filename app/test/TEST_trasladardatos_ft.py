import flet as ft
import sqlite3
import app.globals as globals  # Importa las variables globales


ruta_BDapp= globals.ruta_BD  # Ruta a la base de datos

def obtener_datos_grupo(ruta_BDapp):
    """
    Obtiene todos los datos de la tabla GRUPO como una lista de listas.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.

    Returns:
        list[list]: Una lista donde cada sublista representa una fila de la tabla GRUPO.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GRUPO")
            registros = cursor.fetchall()
        return registros
    except sqlite3.Error as e:
        print(f"Error al obtener datos de GRUPO: {e}")
        return []

def main(page: ft.Page):
    page.title = "Mostrar Datos de GRUPO en Tabla"

    ruta_bd = "mi_app.db"  # Reemplaza con tu ruta de base de datos
    datos_grupo = obtener_datos_grupo(ruta_bd)

    # Define las columnas de la tabla (ajusta según tu estructura)
    columnas = [
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Nivel")),
        ft.DataColumn(ft.Text("Descripción")),
        # Añade más columnas según tu tabla GRUPO
    ]

    filas = []
    for registro in datos_grupo:
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(registro[0]))),  # ID
                    ft.DataCell(ft.Text(str(registro[1]))),  # Nivel
                    ft.DataCell(ft.Text(registro[2])),      # Descripción
                    # Añade más DataCell según tu tabla GRUPO
                ]
            )
        )

    data_table = ft.DataTable(
        columns=columnas,
        rows=filas,
    )

    page.add(data_table)

if __name__ == "__main__":
    ft.app(target=main)