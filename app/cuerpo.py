import flet as ft
import datetime

import appbar


def crear_cuerpo(page, contenido_actual):
    # Devuelve un contenedor con el contenido dinámico
    return ft.Container(
        content=contenido_actual,
        bgcolor=ft.colors.LIGHT_BLUE_50,
        padding=10,
        expand=True
    )

def crear_codigo(page: ft.Page):
    """Crea el entorno para insertar un nuevo código en la tabla."""
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    nivel1_input = ft.Dropdown(
        label="Nivel 1",
        hint_text="Seleccione el Nivel 1",
        options=[
            ft.dropdown.Option("1", "Cuentas Financieras"),
            ft.dropdown.Option("2", "Deudas"),
            ft.dropdown.Option("3", "Gastos"),
            ft.dropdown.Option("4", "Ingresos"),
        ],
    )
    nivel2_input = ft.TextField(label="Nivel 2", hint_text="Ingrese el ID del Nivel 2")
    descripcion_input = ft.TextField(label="Descripción", hint_text="Ingrese la descripción del código")
    importe_input = ft.TextField(
        label="Importe",
        hint_text="Ingrese el importe",
        keyboard_type=ft.KeyboardType.NUMBER,
        value="0",
    )
    fecha_inicio_input = ft.TextField(
        label="Fecha Inicio",
        hint_text="YYYY-MM-DD",
        keyboard_type=ft.KeyboardType.DATETIME,
        value=fecha_actual,
    )

    confirmar_boton = ft.ElevatedButton(
        text="Crear Código",
        icon=ft.icons.ADD,
        on_click=lambda _: print(
            f"Nuevo Código: Nivel1={nivel1_input.value}, Nivel2={nivel2_input.value}, "
            f"Descripción={descripcion_input.value}, Importe={importe_input.value}, Fecha Inicio={fecha_inicio_input.value}"
        ),
    )

    cancelar_boton = ft.ElevatedButton(
        text="Cancelar",
        icon=ft.icons.CANCEL,
        on_click=lambda _: page.go("/"),  # Regresa al contenido inicial
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Crear Nuevo Código", size=20, weight=ft.FontWeight.BOLD),
                nivel1_input,
                nivel2_input,
                descripcion_input,
                importe_input,
                fecha_inicio_input,
                ft.Row(
                    controls=[confirmar_boton, cancelar_boton],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=10,
        ),
        expand=True,
    )