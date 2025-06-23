import flet as ft
import re
from datetime import datetime

# Asume que esta función está en un archivo separado como 'simple_date_input_field.py'
# y que estás importándola correctamente en tu 'main.py' (o TEST_fechas.py)
def create_simple_date_input_field():
    """
    Crea y devuelve un TextField configurado para la entrada de fechas en formato DD-MM-AA,
    junto con un control de texto para mensajes de validación.

    Returns:
        tuple: Una tupla que contiene:
               - ft.TextField: El campo de entrada de fecha.
               - ft.Text: Un control de texto para mensajes de validación/error.
    """

    validation_message = ft.Text("", color=ft.Colors.RED_500, size=12)

    date_input = ft.TextField(
        label="Fecha (DD-MM-AA)",
        hint_text="Ej: 25-12-24",
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9-]", replacement_string=""),
        max_length=8,
        expand=True
    )

    def _validate_date_on_change(e):
        date_string = e.control.value
        pattern = r"^\d{2}-\d{2}-\d{2}$"

        if re.match(pattern, date_string):
            try:
                day, month, year = map(int, date_string.split('-'))
                full_year = 2000 + year if year < 100 else year
                datetime(full_year, month, day)

                validation_message.value = "Formato de fecha válido."
                validation_message.color = ft.Colors.GREEN_500
            except ValueError:
                validation_message.value = "Fecha inválida (ej: 31-02-24 no existe)."
                validation_message.color = ft.Colors.RED_500
        else:
            if date_string:
                validation_message.value = "Formato incorrecto. Usa DD-MM-AA."
                validation_message.color = ft.Colors.RED_500
            else:
                validation_message.value = ""
        e.page.update()

    date_input.on_change = _validate_date_on_change

    return date_input, validation_message


# No incluyo los imports aquí de nuevo para no alargar el código,
# pero asegúrate de que estén en tu archivo.
# from simple_date_input_field import create_simple_date_input_field

def main(page: ft.Page):
    page.title = "Entrada de Fecha Sencilla"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    my_date_field, my_validation_message = create_simple_date_input_field()

    # --- NUEVA SECCIÓN ---
    # Un control para mostrar la fecha obtenida
    retrieved_date_display = ft.Text("Fecha obtenida: N/A")

    def get_date_button_clicked(e):
        # Acceder al valor del campo de texto
        entered_date_string = my_date_field.value

        # Aquí puedes usar el valor de `entered_date_string`
        # Es buena práctica verificar la validación antes de usarla
        if "válido" in my_validation_message.value:
            retrieved_date_display.value = f"Fecha obtenida: {entered_date_string}"
            # Opcional: convertir a un objeto datetime si necesitas manipular la fecha
            try:
                day, month, year_short = map(int, entered_date_string.split('-'))
                full_year = 2000 + year_short if year_short < 100 else year_short
                date_object = datetime(full_year, month, day).date()
                print(f"Fecha como objeto datetime.date: {date_object}")
            except ValueError:
                print("La fecha obtenida no es válida lógicamente, a pesar del formato.")
        else:
            retrieved_date_display.value = "Fecha no válida o campo vacío."

        page.update() # Actualiza la UI para mostrar el mensaje de fecha obtenida
    # --- FIN NUEVA SECCIÓN ---

    page.add(
        ft.Column(
            [
                my_date_field,
                my_validation_message,
                # --- NUEVOS CONTROLES ---
                ft.ElevatedButton("Obtener Fecha", on_click=get_date_button_clicked),
                retrieved_date_display,
                # --- FIN NUEVOS CONTROLES ---
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)