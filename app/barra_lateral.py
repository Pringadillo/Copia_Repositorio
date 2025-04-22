import flet as ft

def crear_barra_lateral(page):
    return ft.Column(
        controls=[
            ft.Text("Menú", style="headlineSmall"),
            ft.ElevatedButton(
                text="Opción 1",
                on_click=lambda e: page.snack_bar.open("Opción 1 seleccionada")
            ),
            ft.ElevatedButton(
                text="Opción 2",
                on_click=lambda e: page.snack_bar.open("Opción 2 seleccionada")
            ),
            ft.ElevatedButton(
                text="Opción 3",
                on_click=lambda e: page.snack_bar.open("Opción 3 seleccionada")
            ),
        ],
        spacing=10,
        expand=True
    )