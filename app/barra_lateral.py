import flet as ft

def crear_barra_lateral(page):
    return ft.Column(
        controls=[
            ft.Text("Menú", style="headlineSmall"),
            ft.ElevatedButton(
                text="Opción 1",
                on_click=lambda e: mostrar_snack_bar(page, "Opción 1 seleccionada")
            ),
            ft.ElevatedButton(
                text="Opción 2",
                on_click=lambda e: mostrar_snack_bar(page, "Opción 2 seleccionada")
            ),
            ft.ElevatedButton(
                text="Opción 3",
                on_click=lambda e: mostrar_snack_bar(page, "Opción 3 seleccionada")
            ),
        ],
        spacing=10,
        expand=True
    )

def mostrar_snack_bar(page, mensaje):
    page.snack_bar.content.value = mensaje
    page.snack_bar.open = True
    page.update()