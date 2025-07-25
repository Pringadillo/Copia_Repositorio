import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"


#ruta_BDapp = globals.ruta_BDapp


# --- Mocks para demostración ---
# En tu aplicación real, estas clases y la ruta_BDapp vendrían de tus archivos `globals.py` y `funciones_BD.py`

class Globals:
    def __init__(self):
        self.ruta_BD = ruta_BDapp
        self.contenido_central_container = ft.Container()

globals = Globals()

class FuncionesBD:
    def obtener_datos_grupo(self, ruta_bd):
        return [(1, "1 - Activo"), (2, "2 - Pasivo"), (3, "3 - Patrimonio Neto")]
    
    def obtener_datos_subgrupo(self, ruta_bd, grupo_id):
        if grupo_id == 1:
            return [(11, "1.1 - Activo Corriente"), (12, "1.2 - Activo No Corriente")]
        elif grupo_id == 2:
            return [(21, "2.1 - Pasivo Corriente"), (22, "2.2 - Pasivo No Corriente")]
        elif grupo_id == 3:
            return [(31, "3.1 - Capital"), (32, "3.2 - Reservas")]
        return []

    def obtener_datos_cuentas(self, ruta_bd, grupo_id, subgrupo_id):
        if grupo_id == 1 and subgrupo_id == 11:
            return [("1.1.001", "Caja"), ("1.1.002", "Bancos")]
        elif grupo_id == 1 and subgrupo_id == 12:
            return [("1.2.001", "Terrenos"), ("1.2.002", "Edificios")]
        elif grupo_id == 2 and subgrupo_id == 21:
            return [("2.1.001", "Proveedores"), ("2.1.002", "Deudas a Corto Plazo")]
        elif grupo_id == 2 and subgrupo_id == 22:
            return [("2.2.001", "Deudas a Largo Plazo")]
        elif grupo_id == 3 and subgrupo_id == 31:
            return [("3.1.001", "Capital Social")]
        return []

funciones_BD = FuncionesBD()

# Asume que ventana_codigo existe y es como la hemos corregido previamente
def ventana_codigo():
    dd_grupo = ft.Dropdown(
        label="Grupo",
        width=200,
        text_size=16,
        options=[],
        hint_text="Elige Grupo",
        border_radius=ft.border_radius.all(8)
    )

    dd_subgrupo = ft.Dropdown(
        label="Subgrupo",
        width=250,
        text_size=16,
        options=[],
        disabled=True,
        hint_text="Elige Subgrupo",
        border_radius=ft.border_radius.all(8)
    )

    dd_cuenta = ft.Dropdown(
        label="Cuenta",
        width=300,
        text_size=16,
        options=[],
        disabled=True,
        hint_text="Elige Cuenta",
        border_radius=ft.border_radius.all(8)
    )

    def cambia_Grupo(event: ft.ControlEvent):
        grupo_id = event.control.value
        dd_subgrupo.options.clear()
        dd_subgrupo.value = None
        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_subgrupo.disabled = True
        dd_cuenta.disabled = True
        dd_subgrupo.options.append(ft.dropdown.Option(key=None, text="Elige subgrupo"))
        dd_cuenta.options.append(ft.dropdown.Option(key=None, text="Elige cuenta"))

        if grupo_id:
            try:
                dd_grupo.data = int(grupo_id)
                seleccion_subgrupo = funciones_BD.obtener_datos_subgrupo(globals.ruta_BD, grupo_id=int(grupo_id))
                subgrupo_options = []
                for id_val, nombre_completo in seleccion_subgrupo:
                    opcion = ft.dropdown.Option(key=str(id_val), text=nombre_completo)
                    subgrupo_options.append(opcion)
                dd_subgrupo.options.extend(subgrupo_options)
                dd_subgrupo.disabled = False
            except ValueError:
                dd_grupo.data = None
                print(f"Error: ID de grupo no válido: {grupo_id}")
        event.page.update()

    def cambia_Subgrupo(event: ft.ControlEvent):
        subgrupo_id = event.control.value
        grupo_id = dd_grupo.data
        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_cuenta.disabled = True
        dd_cuenta.options.append(ft.dropdown.Option(key=None, text="Elige cuenta"))

        if subgrupo_id and grupo_id is not None:
            try:
                seleccion_cuentas = funciones_BD.obtener_datos_cuentas(globals.ruta_BD, grupo_id=int(grupo_id), subgrupo_id=int(subgrupo_id))
                cuenta_options = []
                for codigo, descripcion in seleccion_cuentas:
                    visible_text = f"{codigo} - {descripcion}"
                    flet_options = ft.dropdown.Option(key=codigo, text=visible_text)
                    cuenta_options.append(flet_options)
                dd_cuenta.options.extend(cuenta_options)
                dd_cuenta.disabled = False
            except ValueError:
                print(f"Error: ID de subgrupo o grupo no válido. Grupo: {grupo_id}, Subgrupo: {subgrupo_id}")
        event.page.update()

    dd_grupo.on_change = cambia_Grupo
    dd_subgrupo.on_change = cambia_Subgrupo

    grupos_iniciales = funciones_BD.obtener_datos_grupo(globals.ruta_BD)
    dd_grupo.options.append(ft.dropdown.Option(key=None, text="Elige Grupo"))
    for id_val, nombre_completo in grupos_iniciales:
        dd_grupo.options.append(ft.dropdown.Option(key=str(id_val), text=nombre_completo))

    return ft.Row(
        controls=[
            dd_grupo,
            dd_subgrupo,
            dd_cuenta,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )


def crear_codigo_accion(e, container_to_update, page):
    """Muestra un formulario para crear un nuevo código."""

    # La función ventana_codigo() devuelve un ft.Row con los dropdowns
    dropdowns_grupos_cuentas = ventana_codigo()

    container_to_update.content = ft.Column(
        controls=[
            ft.Text("Crear Nuevo Código", size=20, weight=ft.FontWeight.BOLD),
            # Integrar la fila de dropdowns aquí
            # Ya no necesitas ft.Text("GRUPO:") porque los dropdowns tienen etiquetas
            dropdowns_grupos_cuentas, # Se inserta la fila de dropdowns directamente aquí
            ft.TextField(label="Nombre del Código", hint_text="Ej: Alquiler"),
            ft.Dropdown(
                label="Tipo de Código",
                options=[
                    ft.dropdown.Option("Financiero"),
                    ft.dropdown.Option("Deuda"),
                    ft.dropdown.Option("Gasto"),
                    ft.dropdown.Option("Ingreso"),
                ],
                hint_text="Selecciona el tipo de cuenta"
            ),
            ft.FilledButton(text="Guardar Código", icon=ft.Icons.SAVE),
            ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        expand=True
    )
    page.update()

# Mock de la función reset_tabla_codigo_contenido para que el ejemplo sea ejecutable
def reset_tabla_codigo_contenido(e, container_to_update, page):
    container_to_update.content = ft.Text("Contenido de la tabla de códigos (simulado)")
    page.update()

# --- Función principal para demostración ---
def main(page: ft.Page):
    page.title = "Demostración de Creación de Código"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 600

    # Contenedor que será actualizado
    main_container = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=20,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=10
    )

    # Botón para activar el formulario
    open_form_button = ft.ElevatedButton(
        text="Crear Código de Acción",
        on_click=lambda e: crear_codigo_accion(e, main_container, page)
    )

    page.add(
        ft.Column(
            [
                open_form_button,
                main_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    # Contenido inicial
    main_container.content = ft.Text("Haz clic en el botón para crear un nuevo código.")
    page.update()

if __name__ == "__main__":
    ft.app(target=main)