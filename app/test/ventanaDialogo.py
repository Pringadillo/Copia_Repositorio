import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de AlertDialog"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. Definir una función para cerrar el diálogo
    # Esta función se llamará cuando se haga clic en los botones de acción del diálogo.
    def close_dlg(e):
        # Establece la propiedad 'open' del diálogo de la página a False para ocultarlo
        page.dialog.open = False
        # Actualiza la página para que los cambios se reflejen en la UI
        page.update()
        # Opcional: Puedes hacer algo diferente dependiendo del botón que se hizo clic
        if e.control.text == "Aceptar":
            page.snack_bar = ft.SnackBar(
                ft.Text("¡Has aceptado!"),
                open=True, # Abrir SnackBar inmediatamente
                action="OK",
                on_action_click=lambda ev: print("OK clicked")
            )
        else: # Si es "Cancelar"
            page.snack_bar = ft.SnackBar(
                ft.Text("Has cancelado."),
                open=True
            )
        page.update() # Actualiza la página para mostrar el SnackBar


    # 2. Crear la instancia de ft.AlertDialog
    # Este es el objeto de diálogo que queremos mostrar.
    mi_alert_dialog = ft.AlertDialog(
        # 'modal=True' significa que el diálogo bloquea la interacción con el resto de la página
        # hasta que el usuario interactúa con el diálogo.
        modal=True,
        # Título del diálogo
        title=ft.Text("Confirmación Importante"),
        # Contenido principal del diálogo. Puede ser cualquier control de Flet.
        content=ft.Text("¿Estás seguro de que deseas proceder con esta acción irreversible?"),
        # Lista de acciones (botones) en la parte inferior del diálogo
        actions=[
            ft.TextButton("Aceptar", on_click=close_dlg), # Botón "Aceptar"
            ft.TextButton("Cancelar", on_click=close_dlg), # Botón "Cancelar"
        ],
        # Alineación de los botones de acción
        actions_alignment=ft.MainAxisAlignment.END, # Alinea los botones a la derecha
        # Opcional: Puedes agregar un botón para cerrar el diálogo si haces clic fuera de él.
        # on_dismiss=lambda e: print("Diálogo descartado al hacer clic fuera"),
    )

    # 3. Función para mostrar el diálogo
    # Esta función se llamará cuando se haga clic en el botón principal de la aplicación.
    def show_alert_dialog(e):
        # Asigna la instancia de AlertDialog a la propiedad 'dialog' de la página
        page.dialog = mi_alert_dialog
        # Establece la propiedad 'open' del diálogo a True para que se muestre
        page.dialog.open = True
        # Actualiza la página para que los cambios se reflejen en la UI
        page.update()

    # 4. Añadir un botón a la página para activar el diálogo
    page.add(
        ft.ElevatedButton("Mostrar Diálogo", on_click=show_alert_dialog)
    )

# Ejecutar la aplicación Flet
if __name__ == "__main__":
    ft.app(target=main)