import flet as ft

from app.data.funciones_BD import *


# Variables Globales
ruta_imagenes = "./imagenes/"
empresa = "Mi_Empresa_22"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
usuario = "Usuario_1"  # Nombre del usuario


contenido_central_container = None
cuerpo_principal_diario = None

def crear_dropdown_grupo():
    return ft.Dropdown(
        label="Grupo",
        width=200,
        text_size=16,
        options=[],
        hint_text="Elige Grupo",
        border_radius=ft.border_radius.all(8)
    )

def crear_dropdown_subgrupo():
    return ft.Dropdown(
        label="Subgrupo",
        width=200,
        text_size=16,
        options=[],
        hint_text="Elige Subgrupo",
        border_radius=ft.border_radius.all(8)
    )

def crear_dropdown_cuentas():
    return ft.Dropdown(
        label="Cuentas",
        width=200,
        text_size=16,
        options=[],
        hint_text="Elige Cuenta",
        border_radius=ft.border_radius.all(8)
    )
 
def ventana_codigo():
    dd_grupo = crear_dropdown_grupo()
    dd_subgrupo = crear_dropdown_subgrupo()
    dd_cuenta = crear_dropdown_cuentas()

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
                seleccion_subgrupo = funciones_BD.obtener_datos_subgrupo(ruta_BD, grupo_id=int(grupo_id))
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
                seleccion_cuentas = funciones_BD.obtener_datos_cuentas(ruta_BD, grupo_id=int(grupo_id), subgrupo_id=int(subgrupo_id))
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

    grupos_iniciales = funciones_BD.obtener_datos_grupo(ruta_BD)
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
    container_to_update.content = ft.Text("Contenido simulado: aquí va el contenido dinamico")
    page.update()


