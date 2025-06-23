import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"



def main(page: ft.Page):
    page.title = "Asiento Simple"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False


    def create_simple_date_input_field():

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


    
    # Campo de fecha (usando tu función)
    campoFecha_field, campoFecha_validation_msg = create_simple_date_input_field()

    '''
    # Otros campos de ejemplo (deberías definirlos como instancias de ft.TextField o el control que corresponda)
    campoGrupo = ft.TextField(label="Grupo", hint_text="Ej: Gastos Varios")
    campoSubgrupo = ft.TextField(label="Subgrupo", hint_text="Ej: Comida")
    campoCuenta = ft.TextField(label="Cuenta", hint_text="Ej: Efectivo")
    campoDescripcion = ft.TextField(label="Descripción", width=300, multiline=True, expand=True)
    campoImporte = ft.TextField(label="Importe", keyboard_type=ft.KeyboardType.NUMBER, hint_text="Ej: 50.25")
    campoPyG = ft.TextField(label="P&G", hint_text="Ej: Sí/No") # Podría ser un ft.Dropdown
    campoCategoria = ft.TextField(label="Categoría", hint_text="Ej: Alimentación")
    campoSubcategoria = ft.TextField(label="Subcategoría", hint_text="Ej: Restaurantes")
    campoconciliar = ft.Checkbox(label="Conciliar", value=False) # Un Checkbox
    campoverificar = ft.Checkbox(label="Verificar", value=False) # Otro Checkbox
    campofechaintroduccion = ft.TextField(
        label="Fecha de Introducción", 
        value=date.today().strftime("%d-%m-%y"), # Formato DD-MM-AA para consistencia
        width=200, 
        read_only=True
    )
    '''


    page.add(
    )

if __name__ == "__main__":
    ft.app(target=main)


''' 
Este código es un ejemplo de cómo crear un formulario básico en Flet para probar un botón relacionado con el Diario. 
continuando con mi programa de cuentas de casa, quiero empezar a trabajar sobre el Diario. Como siempre lo haré con python y la libreria flet, sqlite3

Creo que voy a empezar a pedirte ha realizar una labla en sqlite3 del diario, ha de contener los siguientes campos, con las siguientes condiciones:

id: unico, no nulo, primary key

fecha: no nulo dd/mm/aa

Grupo: no nulo, ha de coincidir con descripcion_grupo de la tabla GRUPO

subgrupo: no nulo, ha de coincidir con descripcion_subgrupo de la tabla SUBGRUPO

Cuenta: no nulo, ha de coincidir con descripcion_n3 de la tabla CUENTAS

importe: no nulo, con 2 decimales y el guion de negativo si es necesario

PyG: 
'''