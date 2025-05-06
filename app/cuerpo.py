import flet as ft
import datetime

import appbar



def crear_cuerpo(page, contenido):
    # Devuelve un contenedor con el contenido dinámico
    return ft.Container(
        content=contenido,
        bgcolor=ft.colors.LIGHT_BLUE_50,
        padding=10,
        expand=True
    )


contenido_por_defecto = ft.Column(
    [
        ft.Text("Bienvenido a la aplicación de Cuentas de Casa", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("Aquí puedes gestionar tus cuentas y gastos de manera eficiente.", size=16),
        ft.Container(
            content=ft.Image(src="https://via.placeholder.com/150", width=150, height=150),
            border=ft.border.all(2, ft.colors.BLACK)
        ),
        ft.Text("Fecha actual: " + str(datetime.datetime.now().date()), size=16)
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
)
