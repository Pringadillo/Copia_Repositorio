import flet as ft
import datetime

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
