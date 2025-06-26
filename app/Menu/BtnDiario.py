import flet as ft
import datetime
import sqlite3

import sys
import os


from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo, obtener_datos_subgrupo, mostrar_cuentas_por_grupo_flet
import globals

'''

def boton_diario():
    """
    Función que se ejecuta al hacer clic en el botón "Diario".
    """

    def Tabla_Diario(e):
        #contenido_cuerpo_container.content = ft.Text("menu MOSTRAR TABLA CÓDIGO", size=20)
        cuerpo_diario = ft.Container(
            content=ft.Text("Tabla Diario", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=ft.border_radius.all(10)
        )

        e.page.update()
        return cuerpo_diario

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
                    text="Tabla Diario",
                    #on_click=ver_4columnas,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Asiento Simple",
                    #on_click=ver_4columnas,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Traspaso entre cuentas",
                    #on_click=crear_Grupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Modificar Asiento ",
                    #on_click=crear_Subgrupo,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Importar datos Excel",
                    #on_click=crear_Cuenta,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # ----------------------  Estructura principal -----------------
    globals.contenido_central_container.content = ft.Column(
        controls=[
            submenu,  # Submenú siempre visible
            cuerpo_diario # Contenido principal del diario
        ],
        expand=True,
        spacing=10,  # separacion entre el submenú y el contenido

    )
    return globals.contenido_central_container.content

'''


'''    
cuerpo_principal_diario = ft.Container(
    content=ft.Text("Haz clic en una opción del submenú 'Diario'.", size=20, weight=ft.FontWeight.NORMAL),
    alignment=ft.alignment.center,
    padding=20,
    bgcolor=ft.Colors.GREY_100,
    border_radius=ft.border_radius.all(10),
    expand=True # Permite que ocupe el espacio disponible
    )
'''
# --- Funciones de la UI ---

def boton_diario2():
    """
    Función que configura la sección "Diario" de la aplicación,
    incluyendo su submenú y el área de contenido principal que se actualiza.
    """
    cuerpo_principal_diario=ft.Container()


    # --- Funciones para actualizar el contenido principal ---
    # Estas funciones serán los 'on_click' de los botones del submenú.
    # Ahora modifican el 'content' de 'cuerpo_principal_diario' directamente.

    def mostrar_Tabla_Diario(e: ft.ControlEvent):
        # Actualiza el contenido del contenedor principal del diario
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Tabla Diario cargada con datos...", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update() # Es crucial actualizar la página para que se vean los cambios

    def mostrar_Asiento_Simple(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Formulario para Asiento Simple.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Traspaso_Cuentas(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Interfaz para Traspaso entre Cuentas.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Modificar_Asiento(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Herramienta para Modificar Asiento.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Importar_Excel(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Sección para Importar datos Excel.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.YELLOW_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()


    # ----------------------------------------- SUBMENÚ -----------------------------------------
    # Definición de los botones del submenú con sus handlers
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Tabla Diario",
                    on_click=mostrar_Tabla_Diario, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Asiento Simple",
                    on_click=mostrar_Asiento_Simple, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Traspaso entre cuentas", # Texto en varias líneas
                    on_click=mostrar_Traspaso_Cuentas, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Modificar Asiento", # Texto en varias líneas
                    on_click=mostrar_Modificar_Asiento, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Importar datos Excel", # Texto en varias líneas
                    on_click=mostrar_Importar_Excel, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20, # Espacio entre los botones
        ),
        bgcolor=ft.Colors.WHITE,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # ---------------------- Estructura principal del "Diario" -----------------
    # Se establece el contenido de 'contenido_central_container'
    globals.contenido_central_container.content = ft.Column(
        controls=[
            submenu, # El submenú siempre está en la parte superior
            cuerpo_principal_diario # Esta área se actualizará dinámicamente
        ],
        expand=True, # La columna se expande para ocupar el espacio disponible
        spacing=10, # Separación entre el submenú y el contenido principal
    )
    
    # Retorna el contenido del contenedor central.
    # Cuando esta función es llamada (por ejemplo, desde un botón principal "Diario"),
    # establecerá el contenido de contenido_central_container.
    return globals.contenido_central_container.content



def boton_diario3():
    """
    Función que configura la sección "Diario" de la aplicación,
    incluyendo su submenú y el área de contenido principal que se actualiza.
    """
    cuerpo_principal_diario=ft.Container()


    # --- Funciones para actualizar el contenido principal ---
    # Estas funciones serán los 'on_click' de los botones del submenú.
    # Ahora modifican el 'content' de 'cuerpo_principal_diario' directamente.

    def mostrar_Tabla_Diario(e: ft.ControlEvent):
        # Actualiza el contenido del contenedor principal del diario

        datos_tabla_diario = ""
        ver_la_tabla_diario= ""

        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Tabla Diario cargada con datos...", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update() # Es crucial actualizar la página para que se vean los cambios

    def mostrar_Asiento_Simple(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Formulario para Asiento Simple.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Traspaso_Cuentas(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Interfaz para Traspaso entre Cuentas.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Modificar_Asiento(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Herramienta para Modificar Asiento.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def mostrar_Importar_Excel(e: ft.ControlEvent):
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("Contenido: Sección para Importar datos Excel.", size=20, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.YELLOW_50,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()


    # ----------------------------------------- SUBMENÚ -----------------------------------------
    # Definición de los botones del submenú con sus handlers
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Tabla Diario",
                    on_click=mostrar_Tabla_Diario, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Asiento Simple",
                    on_click=mostrar_Asiento_Simple, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Traspaso entre cuentas", # Texto en varias líneas
                    on_click=mostrar_Traspaso_Cuentas, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Modificar Asiento", # Texto en varias líneas
                    on_click=mostrar_Modificar_Asiento, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Importar datos Excel", # Texto en varias líneas
                    on_click=mostrar_Importar_Excel, # Asignado a la función para actualizar
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20, # Espacio entre los botones
        ),
        bgcolor=ft.Colors.WHITE,
        padding=10,
        border_radius=ft.border_radius.all(10),
    )

    # ---------------------- Estructura principal del "Diario" -----------------
    # Se establece el contenido de 'contenido_central_container'
    globals.contenido_central_container.content = ft.Column(
        controls=[
            submenu, # El submenú siempre está en la parte superior
            cuerpo_principal_diario # Esta área se actualizará dinámicamente
        ],
        expand=True, # La columna se expande para ocupar el espacio disponible
        spacing=10, # Separación entre el submenú y el contenido principal
    )
    
    # Retorna el contenido del contenedor central.
    # Cuando esta función es llamada (por ejemplo, desde un botón principal "Diario"),
    # establecerá el contenido de contenido_central_container.
    return globals.contenido_central_container.content



