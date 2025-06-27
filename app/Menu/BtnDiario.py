import flet as ft
import datetime
import sqlite3
from datetime import datetime
import sys
import os


from app.data.funciones_BD import *
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

    def mostrar_Tabla_Diario(e: ft.ControlEvent): # Asumo que esta es la función a la que te referías
        ruta_BDapp= globals.ruta_BD
        asientos = obtener_asientos_diario(ruta_BDapp)
        
        if not asientos:
            # Si no hay datos, se actualiza el contenido del contenedor principal
            cuerpo_principal_diario.content = ft.Container(
                content=ft.Text("No hay datos en el diario para mostrar.", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                #padding=20,
                expand=True
            )
            e.page.update()
            return

        # Obtenemos los nombres de las columnas de la primera fila (diccionario)
        column_names = list(asientos[0].keys())

        # Creamos las DataColumnas
        columns = []
        for col_name in column_names:
            columns.append(
                ft.DataColumn(
                    ft.Text(col_name, weight=ft.FontWeight.BOLD),
                    on_sort=lambda e: print(f"Ordenando por {e.column}"), # Puedes implementar lógica de ordenamiento aquí
                )
            )

        # Creamos las DataFilas
        rows = []
        for asiento in asientos:
            cells = []
            for col_name in column_names:
                cells.append(ft.DataCell(ft.Text(str(asiento[col_name]))))
            rows.append(ft.DataRow(cells=cells))


        # Creamos el contenedor que envolverá la tabla
        tabla_container = ft.DataTable(
                columns=columns,
                rows=rows,
                sort_column_index=0,  # Columna por defecto para ordenar (ej. la primera)
                sort_ascending=True,  # Orden ascendente por defecto
                heading_row_color=ft.Colors.BLUE_GREY_100,
                data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
                border=ft.border.all(1, ft.Colors.GREY_300),
                column_spacing=20,
                horizontal_margin=10,
                divider_thickness=1,
        )
        

        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Libro Diario", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    tabla_container, # Esta 'tabla_container' está definida justo arriba
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def insertar_Asiento_Simple(e: ft.ControlEvent):

        crearAsientoSimple = ft.Column(
            controls=[ ft.TextField(
                            label="Fecha de la operación", 
                            hint_text="dd/mm/aa",  # formato
                            #value=default_date_str,   # Establece el valor por defecto a la fecha de hoy
                            width=200, # Ancho del campo de fecha
                            keyboard_type=ft.KeyboardType.DATETIME, # Sugiere un teclado de fecha en móviles
                            #on_change=lambda e: print(f"Fecha ingresada: {e.control.value}") #imprime en consola la fecha ingresada
                        ),
                        ft.Row(
                            controls=[
                                ft.Dropdown(
                                    label="Grupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                ft.Dropdown(
                                    label="Subrupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                                                ft.Dropdown(
                                    label="Cuenta",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                            ],
                            spacing=20, # Espacio entre los desplegables
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.TextField(
                            label="Descripción",
                            hint_text="Introduce la descripción del asiento",
                            multiline=True, # Permite múltiples líneas
                            min_lines=1,    # Altura mínima de 2 líneas
                            max_lines=1,    # Altura máxima de 5 líneas
                            width=400,      # Ancho del campo
                            border_radius=ft.border_radius.all(8) # Borde redondeado
                        ),
                        ft.Row(
                            controls=[
                                ft.TextField(
                                    label="Importe",
                                    width=200,
                                    keyboard_type=ft.KeyboardType.NUMBER, # Permite números y el signo menos
                                    value="0.00", # Valor inicial
                                    text_align=ft.TextAlign.RIGHT, # Alinea el texto a la derecha
                                ),
                                ft.Checkbox(label="Traspaso"),
                                ft.TextField(
                                    label="Número Traspaso",
                                    #hint_text="Ej: 123, -45",
                                    keyboard_type=ft.KeyboardType.NUMBER, # Sugiere un teclado numérico
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string=""), # Permite solo números y el signo menos
                                    max_length=10, # Limita la longitud máxima si lo deseas
                                    width=250,
                                    text_align=ft.TextAlign.RIGHT,
                                    ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.Dropdown(
                                    label="Grupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                ft.Dropdown(
                                    label="Subrupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                                                ft.Dropdown(
                                    label="Cuenta",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                            ],
                            spacing=20, # Espacio entre los desplegables
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                

                                ft.TextField(
                                    label="Fecha Creación",
                                    read_only=True,
                                    value=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    width=200
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.Checkbox(label="Guardar"),
                                ft.Checkbox(label="Cancelar"),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                ],
                #spacing=10, #separación entre los controles   
        )
        
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Crear Asiento Simple", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    crearAsientoSimple, # Esta 'tabla_container' está definida justo arriba
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.WHITE,
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
                    on_click=insertar_Asiento_Simple, # Asignado a la función para actualizar
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



def boton_diario4():
    """
    Función que configura la sección "Diario" de la aplicación,
    incluyendo su submenú y el área de contenido principal que se actualiza.
    """
    cuerpo_principal_diario=ft.Container()

    def mostrar_Tabla_Diario(e: ft.ControlEvent): # Asumo que esta es la función a la que te referías
        ruta_BDapp= globals.ruta_BD
        asientos = obtener_asientos_diario(ruta_BDapp)
        
        if not asientos:
            # Si no hay datos, se actualiza el contenido del contenedor principal
            cuerpo_principal_diario.content = ft.Container(
                content=ft.Text("No hay datos en el diario para mostrar.", text_align=ft.TextAlign.CENTER),
                alignment=ft.alignment.center,
                #padding=20,
                expand=True
            )
            e.page.update()
            return

        # Obtenemos los nombres de las columnas de la primera fila (diccionario)
        column_names = list(asientos[0].keys())

        # Creamos las DataColumnas
        columns = []
        for col_name in column_names:
            columns.append(
                ft.DataColumn(
                    ft.Text(col_name, weight=ft.FontWeight.BOLD),
                    on_sort=lambda e: print(f"Ordenando por {e.column}"), # Puedes implementar lógica de ordenamiento aquí
                )
            )

        # Creamos las DataFilas
        rows = []
        for asiento in asientos:
            cells = []
            for col_name in column_names:
                cells.append(ft.DataCell(ft.Text(str(asiento[col_name]))))
            rows.append(ft.DataRow(cells=cells))


        # Creamos el contenedor que envolverá la tabla
        tabla_container = ft.DataTable(
                columns=columns,
                rows=rows,
                sort_column_index=0,  # Columna por defecto para ordenar (ej. la primera)
                sort_ascending=True,  # Orden ascendente por defecto
                heading_row_color=ft.Colors.BLUE_GREY_100,
                data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
                border=ft.border.all(1, ft.Colors.GREY_300),
                column_spacing=20,
                horizontal_margin=10,
                divider_thickness=1,
        )
        

        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Libro Diario", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    tabla_container, # Esta 'tabla_container' está definida justo arriba
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(10),
            expand=True
        )
        e.page.update()

    def insertar_Asiento_Simple(e: ft.ControlEvent):

        crearAsientoSimple = ft.Column(        # container
            controls=[ ft.TextField(
                            label="Fecha de la operación", 
                            hint_text="dd/mm/aa",  # formato
                            #value=default_date_str,   # Establece el valor por defecto a la fecha de hoy
                            width=200, # Ancho del campo de fecha
                            keyboard_type=ft.KeyboardType.DATETIME, # Sugiere un teclado de fecha en móviles
                            #on_change=lambda e: print(f"Fecha ingresada: {e.control.value}") #imprime en consola la fecha ingresada
                        ),

                        
                        ft.Row(
                            controls=[
                                ft.Dropdown(
                                    label="Grupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                ft.Dropdown(
                                    label="Subrupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                                                ft.Dropdown(
                                    label="Cuenta",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                            ],
                            spacing=20, # Espacio entre los desplegables
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.TextField(
                            label="Descripción",
                            hint_text="Introduce la descripción del asiento",
                            multiline=True, # Permite múltiples líneas
                            min_lines=1,    # Altura mínima de 2 líneas
                            max_lines=1,    # Altura máxima de 5 líneas
                            width=400,      # Ancho del campo
                            border_radius=ft.border_radius.all(8) # Borde redondeado
                        ),
                        ft.Row(
                            controls=[
                                ft.TextField(
                                    label="Importe",
                                    width=200,
                                    keyboard_type=ft.KeyboardType.NUMBER, # Permite números y el signo menos
                                    value="0.00", # Valor inicial
                                    text_align=ft.TextAlign.RIGHT, # Alinea el texto a la derecha
                                ),
                                ft.Checkbox(label="Traspaso"),
                                ft.TextField(
                                    label="Número Traspaso",
                                    #hint_text="Ej: 123, -45",
                                    keyboard_type=ft.KeyboardType.NUMBER, # Sugiere un teclado numérico
                                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string=""), # Permite solo números y el signo menos
                                    max_length=10, # Limita la longitud máxima si lo deseas
                                    width=250,
                                    text_align=ft.TextAlign.RIGHT,
                                    ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.Dropdown(
                                    label="Grupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                ft.Dropdown(
                                    label="Subrupo",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                                                ft.Dropdown(
                                    label="Cuenta",  # This acts like the "Grupo" text
                                    options=[ft.dropdown.Option("Opción 1"),
                                            ft.dropdown.Option("Opción 2"),],
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                            ],
                            spacing=20, # Espacio entre los desplegables
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                

                                ft.TextField(
                                    label="Fecha Creación",
                                    read_only=True,
                                    value=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    width=200
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.Checkbox(label="Guardar"),
                                ft.Checkbox(label="Cancelar"),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                ],
                #spacing=10, #separación entre los controles   
        )
        
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Crear Asiento Simple", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    crearAsientoSimple, # Esta 'tabla_container' está definida justo arriba
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            bgcolor=ft.Colors.WHITE,
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
                    on_click=insertar_Asiento_Simple, # Asignado a la función para actualizar
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




