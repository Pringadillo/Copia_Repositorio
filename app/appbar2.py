import flet as ft

def crear_appbar(page: ft.Page, actualizar_cuerpo):
    """Crea la barra de navegación superior."""
    return ft.AppBar(
        title=ft.Text("Cuentas de Casa"),
        actions=[
            ft.IconButton(
                icon=ft.icons.ADD,
                tooltip="Crear Código",
                on_click=lambda _: actualizar_cuerpo(page, "crear_codigo")  # Cambia el contenido del cuerpo
            ),
        ],
    )