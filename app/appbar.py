import flet as ft

def crear_appbar(page):
    def boton_click(e):
        if e.control.text == "Diario":
            page.controls[0].controls[1].content = ft.Text("Contenido del Diario")
        elif e.control.text == "Mayor":
            page.controls[0].controls[1].content = ft.Text("Contenido del Mayor")
        elif e.control.text == "Balance":
            page.controls[0].controls[1].content = ft.Text("Contenido del Balance")
        elif e.control.text == "Saldos":
            page.controls[0].controls[1].content = ft.Text("Contenido de Saldos")
        elif e.control.text == "Configuración":
            page.controls[0].controls[1].content = ft.Text("Contenido de Configuración")

        page.update()

    appbar = ft.AppBar(
        title=ft.Row(
            [
                ft.TextButton(text="Diario", on_click=boton_click),
                ft.TextButton(text="Mayor", on_click=boton_click),
                ft.TextButton(text="Balance", on_click=boton_click),
                ft.TextButton(text="Saldos", on_click=boton_click),
                ft.TextButton(text="Configuración", on_click=boton_click),
            ]
        )
    )
    return appbar