import flet as ft
import datetime
import sqlite3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from .data.funciones_BD import crear_tabla, insertar_datos, eliminar_datos, actualizar_datos

'''
empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"


'''
print ("Ruta de la base de datos:", ruta_BD)




def TablaCodigos():
    # Contenedor dinámico para el contenido_cuerpo
    contenido_cuerpo_container = ft.Container(
        content=ft.Text("Seleccione una opción del submenú", size=20),
        expand=True,
    )

    # Funciones para actualizar el contenido dinámico
    def ver_TablaCodigos(e):
        contenido_cuerpo_container.content = ft.Text("Tabla Códigos", size=20)
        e.page.update()

    def crear_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Crear Código", size=20)
        e.page.update()

    def actualizar_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Actualizar Código", size=20)
        e.page.update()

    def eliminar_codigo(e):
        contenido_cuerpo_container.content = ft.Text("Formulario para Eliminar Código", size=20)
        e.page.update()

    # Submenú CRUD de la tabla código
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Ver Tabla Códigos",
                    icon=ft.icons.TABLE_CHART,
                    on_click=ver_TablaCodigos,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Crear Código",
                    icon=ft.icons.ADD,
                    on_click=crear_codigo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Actualizar Código",
                    icon=ft.icons.EDIT,
                    on_click=actualizar_codigo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Eliminar Código",
                    icon=ft.icons.DELETE,
                    on_click=eliminar_codigo,
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

    # Estructura principal que incluye el submenú y el contenido dinámico
    cuerpo = ft.Column(
        controls=[
            submenu,  # Submenú siempre visible
            contenido_cuerpo_container,  # Contenido dinámico que cambia
        ],
        expand=True,
    )
    return cuerpo




'''

def obtener_datos_nivel1():
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nombre FROM nivel1")  # Ajusta 'nombre' al nombre de tu columna
    datos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return datos

def obtener_datos_nivel2(nivel1_seleccionado):
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nombre FROM nivel2 WHERE nivel1_id = (SELECT id FROM nivel1 WHERE nombre = ?)", (nivel1_seleccionado,)) # Ajusta 'nombre' y 'nivel1_id'
    datos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return datos

def obtener_datos_nivel3(nivel2_seleccionado):
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nombre FROM nivel3 WHERE nivel2_id = (SELECT id FROM nivel2 WHERE nombre = ?)", (nivel2_seleccionado,)) # Ajusta 'nombre' y 'nivel2_id'
    datos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return datos

def main(page: ft.Page):
    page.title = "Formulario Dinámico con BD"

    nivel1_data = obtener_datos_nivel1()

    nivel1_dropdown = ft.Dropdown(
        label="Nivel 1",
        options=[ft.dropdown.Option(text) for text in nivel1_data],
        on_change=lambda e: update_nivel2(e.control.value),
        value=nivel1_data[0] if nivel1_data else None,
        disabled=not nivel1_data
    )

    nivel2_dropdown = ft.Dropdown(
        label="Nivel 2",
        options=[],
        on_change=lambda e: update_nivel3(e.control.value),
        disabled=True,
    )

    nivel3_dropdown = ft.Dropdown(
        label="Nivel 3",
        options=[],
        disabled=True,
    )

    saldo_inicial_input = ft.TextField(label="Saldo Inicial", keyboard_type=ft.KeyboardType.NUMBER)
    fecha_inicio_input = ft.TextField(label="Fecha Inicio")

    def update_nivel2(nivel1_value):
        nivel2_data = obtener_datos_nivel2(nivel1_value)
        nivel2_dropdown.options = [ft.dropdown.Option(text) for text in nivel2_data]
        nivel2_dropdown.disabled = not nivel2_data
        nivel2_dropdown.value = nivel2_data[0] if nivel2_data else None
        nivel3_dropdown.options = []
        nivel3_dropdown.disabled = True
        nivel3_dropdown.value = None
        page.update()

    def update_nivel3(nivel2_value):
        nivel3_data = obtener_datos_nivel3(nivel2_value)
        nivel3_dropdown.options = [ft.dropdown.Option(text) for text in nivel3_data]
        nivel3_dropdown.disabled = not nivel3_data
        nivel3_dropdown.value = nivel3_data[0] if nivel3_data else None
        page.update()

    def limpiar_formulario(e):
        nivel1_dropdown.value = nivel1_data[0] if nivel1_data else None
        update_nivel2(nivel1_dropdown.value)
        saldo_inicial_input.value = ""
        fecha_inicio_input.value = ""
        page.update()

    def crear_elemento(e):
        # Aquí iría la lógica para insertar los datos en tu base de datos
        print("Crear elemento:",
              nivel1_dropdown.value,
              nivel2_dropdown.value,
              nivel3_dropdown.value,
              saldo_inicial_input.value,
              fecha_inicio_input.value)
        # Ejemplo de inserción (tendrás que adaptarlo a tu esquema de base de datos)
        # conn = sqlite3.connect(ruta_BD)
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO tu_tabla (nivel1, nivel2, nivel3, saldo, fecha) VALUES (?, ?, ?, ?, ?)",
        #                (nivel1_dropdown.value, nivel2_dropdown.value, nivel3_dropdown.value, saldo_inicial_input.value, fecha_inicio_input.value))
        # conn.commit()
        # conn.close()

    def cancelar_creacion(e):
        print("Creación cancelada")

    formulario = ft.Column(
        controls=[
            nivel1_dropdown,
            nivel2_dropdown,
            nivel3_dropdown,
            saldo_inicial_input,
            fecha_inicio_input,
            ft.Row(
                controls=[
                    ft.ElevatedButton("Limpiar", on_click=limpiar_formulario),
                    ft.ElevatedButton("Crear", on_click=crear_elemento, bgcolor=ft.colors.GREEN_ACCENT_700),
                    ft.ElevatedButton("Cancelar", on_click=cancelar_creacion, bgcolor=ft.colors.RED_ACCENT_700),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    contenedor_formulario = ft.Container(
        content=formulario,
        padding=20,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
    )

    page.add(contenedor_formulario)

if __name__ == "__main__":
    # Asegurarse de que la carpeta 'data' existe
    if not os.path.exists("./data"):
        os.makedirs("./data")
        # Aquí podrías añadir la lógica para crear la base de datos y las tablas si no existen

    ft.app(target=main)'''