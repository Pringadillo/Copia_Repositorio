import flet as ft
import datetime
import sqlite3
from datetime import datetime
import sys
import os


from app.data.funciones_BD import *
import app.data.funciones_BD as funciones_BD

import globals

ruta_BDapp = globals.ruta_BD
lista_Grupos=[]
lista_Subgrupos = []
lista_Cuentas =[]

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
        asientos = funciones_BD.mostrar_datos_Diario(ruta_BDapp)
        
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
 
    def mostrar_Tabla_Diario(e: ft.ControlEvent): 
        ruta_BDapp= globals.ruta_BD
        asientos = funciones_BD.mostrar_datos_Diario(ruta_BDapp)
        
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

        crearAsientoSimple_1 = ft.Column(        # container
            controls=[ ft.TextField(
                            label="Fecha de la operación", 
                            hint_text="dd/mm/aa",  # formato
                            #value=default_date_str,   # Establece el valor por defecto a la fecha de hoy
                            width=200, # Ancho del campo de fecha
                            keyboard_type=ft.KeyboardType.DATETIME, # Sugiere un teclado de fecha en móviles
                            #on_change=lambda e: print(f"Fecha ingresada: {e.control.value}") #imprime en consola la fecha 
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
                                    label="Subgrupo",  # This acts like the "Grupo" text
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
                spacing=10, #separación entre los controles                  
                expand=True,  # Permite que la columna ocupe todo el espacio disponible


        )
        
        crearAsientoSimple = ft.Container(
            content=crearAsientoSimple_1,  # Aquí se usa el container definido arriba
            margin=ft.margin.only(left=50, top=20),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=ft.border_radius.all(10),
            expand=True  # Permite que el contenedor ocupe todo el espacio disponible
        )


        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(  # 'content' debe ser un solo control, en este caso, un ft.Column
                [
                    ft.Text("Crear Asiento Simple", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    crearAsientoSimple, # Asumiendo que 'crearAsientoSimple' es un control de Flet válido (ej. un ft.Container, ft.Column, ft.Row, etc.)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            margin=ft.margin.only(left=10), # margen izquierdo de TODO el contenedor
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



def boton_CrearCodigo():
    """
    Función que configura la sección "Diario" de la aplicación,
    incluyendo su submenú y el área de contenido principal que se actualiza.
    """
    cuerpo_principal_diario=ft.Container()

    # Definimos los Dropdowns para poder manipularlos
    dd_grupo = ft.Dropdown(
        label="Grupo",
        width=200,
        text_size=16,
        options=[], # Inicialmente vacío, se llenará al seleccionar un grupo
        hint_text="Elige Grupo",        
    )

    dd_subgrupo = ft.Dropdown(
        label="Subgrupo",
        width=250,
        text_size=16,
        options=[], # Inicialmente vacío, se llenará al seleccionar un grupo
        disabled=True, # Inicialmente deshabilitado hasta que se seleccione un grupo
        hint_text="Elige Subgrupo",
    )

    dd_cuenta = ft.Dropdown(
        label="Cuenta",
        width=300,
        text_size=16,
        options=[], # Inicialmente vacío, se llenará al seleccionar un grupo
        disabled=True, # Inicialmente deshabilitado hasta que se seleccione un grupo
        hint_text="Elige Cuenta",
    )

    def mostrar_Tabla_Diario(e: ft.ControlEvent): 
        
        asientos = funciones_BD.mostrar_datos_Diario(ruta_BDapp)
        
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
        ruta_BDapp = globals.ruta_BD

        def cambia_Grupo(event: ft.ControlEvent):
            seleccion_completa_grupo = event.control.value # Ej. "1 - Activo"
            grupo_id = None

            dd_subgrupo.options.clear()
            dd_subgrupo.value = None
            dd_cuenta.options.clear()
            dd_cuenta.value = None
            dd_subgrupo.disabled = True # Deshabilita subgrupo hasta que se seleccione un grupo válido
            dd_cuenta.disabled = True   # Deshabilita cuenta hasta que se seleccione un subgrupo válido
            
            #print(f"Grupo seleccionado: {seleccion_completa_grupo}")
            
            if seleccion_completa_grupo and seleccion_completa_grupo != "Elige Grupo":
                try:
                    # Extraer el ID de la cadena. Esto asume el formato "ID - Nombre"
                    grupo_id = int(seleccion_completa_grupo.split(' - ')[0]) 
                    #print(f"Grupo ID: {grupo_id}")
                    # Guarda el grupo_id seleccionado directamente en la propiedad 'data' del control
                    event.control.data = grupo_id
                    # Obtener subgrupos basados en el grupo_id
                    seleccion_subgrupo = obtener_datos_subgrupo(ruta_BDapp, grupo_id=grupo_id)
                    #print(seleccion_completa_subgrupo)

                    # Llenar el Dropdown de subgrupos
                    subgrupo_id = []

                    for id_val, nombre_completo in seleccion_subgrupo:
                        nombre_corto = nombre_completo.split(' - ')[-1] if ' - ' in nombre_completo else nombre_completo
                        texto_visible = f"{id_val} {nombre_corto}"
                        opcion = ft.dropdown.Option(
                                text=texto_visible,
                                data=id_val # Guardamos solo el ID como valor
                            )
                        subgrupo_id.append(opcion)

                    dd_subgrupo.options.extend(subgrupo_id) # ¡Añade las opciones al dropdown de subgrupos!
                    dd_subgrupo.disabled = False # Habilita el dropdown de subgrupos

                except ValueError:
                    grupo_id = None # Si no se puede parsear, no es un ID válido
                    event.control.data = None # Limpia el dato si es inválido

           
            e.page.update()  # Actualiza la página una vez después de todos los cambios

        def cambia_Subgrupo(event: ft.ControlEvent):
            #buscamos el valor del boton subgrupo
            seleccion_completa_subgrupo = event.control.value # Ej. "2 - Caja"
            #transformar el valor a un ID numérico
            valor_extraido = (seleccion_completa_subgrupo.split('.')[-1].strip())
            subgrupo_id = int(valor_extraido.split(' ')[0].strip())          
            grupo_id = dd_grupo.data  

            # para controlar las variables
            #print(f"seleccion_completa_subgrupo: {seleccion_completa_subgrupo}")
            #print(f"grupo_id: {grupo_id}")
            #print(f"subgrupo_id: {subgrupo_id}")

            #limpiar los datos del dropdown de cuenta
            dd_cuenta.options.clear()
            dd_cuenta.value = None
            dd_cuenta.disabled = True # Deshabilita cuenta hasta que se seleccione un subgrupo válido

            # Llenar el Dropdown de Cuenta
            cuentas_id =[]
            seleccion_cuentas = obtener_datos_cuentas(ruta_BDapp, grupo_id=grupo_id, subgrupo_id=subgrupo_id)
            #print(f"seleccion_cuentas: {seleccion_cuentas}")
            for la_cuenta in seleccion_cuentas:
                codigo_completo = la_cuenta[0]
                #print(f"El código completo es: {codigo_completo}")
                descripcion_cuenta = la_cuenta[1].split(' - ')[-1]
                #print(f"La descripción de la cuenta es: {descripcion_cuenta}")
                cuentas_id.append((codigo_completo, descripcion_cuenta))
                #print(f"Cuenta añadida: {cuentas_id}")
                

            # obtener las cuentas basadas en el subgrupo_id
            if cuentas_id is not None and cuentas_id != "Elige Cuenta":
                #print(f"pasa el criterio Elige subgrupo: {cuentas_id}")
                dd_cuenta.options.clear() 

                flet_options = []
                for codigo, descripcion in cuentas_id:
                    visible_text = f"{codigo} {descripcion}" 
                    flet_options.append(ft.dropdown.Option(key=codigo, text=visible_text)) 
                    
                dd_cuenta.options.extend(flet_options) 
                dd_cuenta.disabled = False

            else: 
                print("Falla algo")
                # Asegurarse de que la cuenta esté deshabilitada y vacía si el subgrupo no es válido
                dd_cuenta.value = None
                dd_cuenta.disabled = True
                
            event.page.update() # Actualiza la página una vez después de todos los cambios

        def guardar_asiento(e: ft.ControlEvent):
            # Aquí puedes implementar la lógica para guardar el asiento
            # Por ejemplo, podrías recoger los valores de los campos y guardarlos en la base de datos
            fecha = e.control.parent.controls[0].value
            grupo = dd_grupo.value
            subgrupo = dd_subgrupo.value
            cuenta = dd_cuenta.value
            descripcion = e.control.parent.controls[3].value
            importe = e.control.parent.controls[4].value 
            traspaso = e.control.parent.controls[5].value 
            numero_traspaso = e.control.parent.controls[6].value
            fecha_creacion = e.control.parent.controls[7].value        

        def cancelar_asiento(e: ft.ControlEvent):
            pass
        
        grupos_iniciales = obtener_datos_grupo(ruta_BDapp)
        dd_grupo.options.clear()
        dd_grupo.options.append(ft.dropdown.Option("Elige Grupo", data=None)) # Opción por defecto
        dd_subgrupo.options.append(ft.dropdown.Option("Elige subgrupo", data=None)) # Opción por defecto
        dd_cuenta.options.append(ft.dropdown.Option("Elige cuenta", data=None)) # Opción por defecto

        for id, nombre in grupos_iniciales:
            dd_grupo.options.append(ft.dropdown.Option(f"{id} - {nombre}", data=id)) # Guarda el ID en 'data'

        # Asignar controladores de eventos
        dd_grupo.on_change = cambia_Grupo
        dd_subgrupo.on_change = cambia_Subgrupo

        # Asegura que los dropdowns de subgrupo y cuenta estén deshabilitados al inicio
        dd_subgrupo.disabled = True
        dd_cuenta.disabled = True

        # Dispocición de las ventanas de datos
        crearAsientoSimple_1 = ft.Column(        
            controls=[ ft.TextField(
                            label="Fecha de la operación", 
                            hint_text="dd/mm/aa",  # formato
                            #value=default_date_str,   # Establece el valor por defecto a la fecha de hoy
                            width=200, # Ancho del campo de fecha
                            keyboard_type=ft.KeyboardType.DATETIME, # Sugiere un teclado de fecha en móviles
                            #on_change=lambda e: print(f"Fecha ingresada: {e.control.value}") #imprime en consola la fecha 
                        ),
                        ft.Row(
                            controls=[
                                # ¡IMPORTANTE! Usamos las instancias de Dropdown definidas al principio
                                dd_grupo,
                                dd_subgrupo,
                                dd_cuenta,
                            ],
                            spacing=20,
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
                                    disabled=True, # Deshabilitado hasta que se seleccione un traspaso
                                    ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.Dropdown(
                                    label="Grupo",  # This acts like the "Grupo" text
                                    options = lista_Grupos, # Lista de opciones obtenida de la base de datos
                                    width=200,  # You can adjust the width as needed
                                    #height=50,
                                    text_size=16, # Adjust text size for the dropdown
                                ),
                                ft.Dropdown(
                                    label="Subgrupo",  # This acts like the "Grupo" text
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
                                    width=200,
                                    disabled=True, # Deshabilitado para evitar edición
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Guardar",
                                    on_click=guardar_asiento # Asigna la función a on_click
                                ),
                                ft.ElevatedButton(
                                    text="Cancelar",
                                    on_click=cancelar_asiento # Asigna la función a on_click
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER, # Alinea los checkboxes al centro
                        ),
                ],
                spacing=10, #separación entre los controles                  
                expand=True,  # Permite que la columna ocupe todo el espacio disponible
        )
        
        # traspasar el contenido al container
        crearAsientoSimple = ft.Container(
            content=crearAsientoSimple_1,  # Aquí se usa el container definido arriba
            margin=ft.margin.only(left=50, top=20),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=ft.border_radius.all(10),
            expand=True  # Permite que el contenedor ocupe todo el espacio disponible
        )

        # diseño de la página dinámica de la app, con crearAsientSimple
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Column(  # 'content' debe ser un solo control, en este caso, un ft.Column
                [
                    ft.Text("Crear Asiento Simple", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    crearAsientoSimple, # Asumiendo que 'crearAsientoSimple' es un control de Flet válido (ej. un ft.Container, ft.Column, ft.Row, etc.)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True  # La columna interior también debe expandirse
            ),
            alignment=ft.alignment.center,
            padding=20,
            margin=ft.margin.only(left=10), # margen izquierdo de TODO el contenedor
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
                    text="Diario",
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


