import flet as ft

import datetime

def TablaCodigos():
    # Submenu CRUD de la tabla código
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Ver Tabla Códigos",
                    icon=ft.icons.TABLE_CHART,  # Ícono para "Ver Tabla"
                    on_click=ver_TablaCodigos,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Crear Código",
                    icon=ft.icons.ADD,  # Ícono para "Crear"
                    on_click=crear_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),

                ft.TextButton(
                    text="Actualizar Código",
                    icon=ft.icons.EDIT,  # Ícono para "Actualizar"
                    on_click=actualizar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Eliminar Código",
                    icon=ft.icons.DELETE,  # Ícono para "Eliminar"
                    on_click=eliminar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,  # Centrar los botones horizontalmente
            spacing=20,  # Espaciado entre los botones
        ),
        bgcolor=ft.colors.LIGHT_BLUE_50,  # Fondo suave para el submenú
        padding=10,  # Espaciado interno del contenedor
        border_radius=ft.border_radius.all(10),  # Bordes redondeados
            )
    
    # Contenido de la tabla de códigos
    contenido_cuerpo = ft.Container(
        # poner la tabla Códigos aquí------------------------------------
        content=ft.Column(
            controls=[
                ft.Text("Contenido de Tabla Códigos", size=20),
            ],
            expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )

    # Fila que contiene el submenú y el coColumnnido
    cuerpo = ft.Column(
        controls=[
            submenu,  # Submenú a la izquierda
            contenido_cuerpo,  # Contenido a la derecha
        ],
        expand=True,
    )
    return cuerpo






# -----------------------  FUNCIONES SUBMENU TABLA CODIGOS -----------------------
def ver_TablaCodigos(e):
    print("Ver Tabla Códigos")

    contenido_cuerpo = ft.Container(
        # poner la tabla Códigos aquí------------------------------------
        content=ft.Column(
            controls=[
                ft.Text("Tabla Códigos", size=20),

            ],
            expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )




def crear_codigo(e):
    """Crea el entorno para insertar un nuevo código en la tabla."""
    # Obtener la fecha actual
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    # Lista de opciones para nivel1 (puedes reemplazar estas opciones con datos dinámicos de la base de datos)
    opciones_nivel1 = [
        ft.dropdown.Option("1", "Cuentas Financieras"),
        ft.dropdown.Option("2", "Deudas"),
        ft.dropdown.Option("3", "Gastos"),
        ft.dropdown.Option("4", "Ingresos"),
    ]

    # Crear los campos de entrada
    nivel1_input = ft.Dropdown(
        label="Nivel 1",
        hint_text="Seleccione el Nivel 1",
        options=opciones_nivel1,
    )
    nivel2_input = ft.TextField(label="Nivel 2", hint_text="Ingrese el ID del Nivel 2")
    descripcion_input = ft.TextField(label="Descripción", hint_text="Ingrese la descripción del código")
    importe_input = ft.TextField(
        label="Importe",
        hint_text="Ingrese el importe",
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0",  # Valor por defecto
    )
    fecha_inicio_input = ft.TextField(
        label="Fecha Inicio",
        hint_text="YYYY-MM-DD",
        keyboard_type=ft.KeyboardType.DATETIME,
        value=fecha_actual,  # Valor por defecto
    )

    # Botón para confirmar la creación del código
    confirmar_boton = ft.ElevatedButton(
        text="Crear Código",
        icon=ft.icons.ADD,
        on_click=lambda _: print(
            f"Nuevo Código: Nivel1={nivel1_input.value}, Nivel2={nivel2_input.value}, "
            f"Descripción={descripcion_input.value}, Importe={importe_input.value}, Fecha Inicio={fecha_inicio_input.value}"
        ),
    )

    # Botón para cancelar la acción
    cancelar_boton = ft.ElevatedButton(
        text="Cancelar",
        icon=ft.icons.CANCEL,
        on_click=lambda _: print("Acción cancelada"),
    )

    # Contenedor para el formulario
    formulario = ft.Column(
        controls=[
            ft.Text("Crear Nuevo Código", size=20, weight=ft.FontWeight.BOLD),
            nivel1_input,
            nivel2_input,
            descripcion_input,
            importe_input,
            fecha_inicio_input,
            ft.Row(
                controls=[confirmar_boton, cancelar_boton],
                alignment=ft.MainAxisAlignment.END,  # Alinear los botones a la derecha
                spacing=10,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    # Mostrar el formulario en la ventana
    e.page.controls[0].controls[1].content = formulario
    e.page.update()



def leer_codigo(e):
    print("Ver Tabla") 
    contenido_cuerpo = ft.Container(
    # poner la tabla Códigos aquí------------------------------------
    content=ft.Column(
        controls=[
            ft.Text("Leer Códigos", size=20),
        ],
        expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )   

def actualizar_codigo(e):
    print("Modificar Código")
    contenido_cuerpo = ft.Container(
    # poner la tabla Códigos aquí------------------------------------
    content=ft.Column(
        controls=[
            ft.Text("Modificar Códigos", size=20),
        ],
        expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )      

def eliminar_codigo(e):  
    print("Eliminar Código")
    contenido_cuerpo = ft.Container(
    # poner la tabla Códigos aquí------------------------------------
    content=ft.Column(
        controls=[
            ft.Text("Eliminar Código", size=20),
        ],
        expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )  
