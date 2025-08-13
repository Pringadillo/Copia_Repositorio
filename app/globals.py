import flet as ft

from app.data.funciones_BD import *
import app.data.funciones_BD as funciones_BD

# Variables Globales
ruta_imagenes = "./imagenes/"
empresa = "Mi_Empresa_23"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"
usuario = "Usuario_1"  # Nombre del usuario


contenido_central_container = None
cuerpo_principal_diario = None

def crear_dropdown_grupo():
    return ft.Dropdown(
        label="Grupo",
        width=250,
        text_size=16,
        options=[],
        hint_text="Elige Grupo",
        border_radius=ft.border_radius.all(8)
    )

def crear_dropdown_subgrupo():
    return ft.Dropdown(
        label="Subgrupo",
        width=260,
        text_size=16,
        options=[],
        hint_text="Elige Subgrupo",
        border_radius=ft.border_radius.all(8)
    )

def crear_dropdown_cuentas():
    return ft.Dropdown(
        label="Cuentas",
        width=250,
        text_size=16,
        options=[],
        hint_text="Elige Cuenta",
        border_radius=ft.border_radius.all(8)
    )

def ventana_codigo(ruta_BD):
    dd_grupo = crear_dropdown_grupo()
    dd_subgrupo = crear_dropdown_subgrupo()
    dd_cuenta = crear_dropdown_cuentas()

    dd_subgrupo.disabled = True
    dd_cuenta.disabled = True
    #dd_subgrupo.visible = False
    #dd_cuenta.visible = False

    def cambia_Grupo(event: ft.ControlEvent):
        grupo_id_str = event.control.value
        
        dd_subgrupo.options.clear()
        dd_subgrupo.value = None
        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_subgrupo.disabled = True
        dd_cuenta.disabled = True
        dd_subgrupo.options.append(ft.dropdown.Option(key=None, text="Elige subgrupo"))
        dd_cuenta.options.append(ft.dropdown.Option(key=None, text="Elige cuenta"))

        if grupo_id_str:
            try:
                grupo_id = int(grupo_id_str)
                dd_grupo.data = grupo_id

                seleccion_subgrupo = funciones_BD.obtener_datos_subgrupo(ruta_BD, grupo_id=grupo_id)
                subgrupo_options = []
                for row_dict in seleccion_subgrupo:
                    # **Subgrupo Display Format: 'grupo_id.cod_2 - desc_subgrupo'**
                    # We need the 'grupo_id' from the currently selected group, which is stored in dd_grupo.data
                    # The 'cod_2' and 'desc_subgrupo' come from the current row_dict.
                    display_text = f"{grupo_id}.{row_dict['cod_2']} - {row_dict['desc_subgrupo']}"
                    opcion = ft.dropdown.Option(
                        key=str(row_dict['subgrupo_id']), # Key is still just the subgrupo_id
                        text=display_text
                    )
                    subgrupo_options.append(opcion)
                dd_subgrupo.options.extend(subgrupo_options)
                dd_subgrupo.disabled = False
            except ValueError:
                dd_grupo.data = None
                print(f"Error: ID de grupo no válido: {grupo_id_str}")
            except KeyError as e:
                # Added specific error handling for debugging if column names are wrong
                print(f"Error de KeyError al procesar datos de subgrupos: {e}. "
                      f"Asegúrate que la tabla SUBGRUPO tiene las columnas 'subgrupo_id', 'cod_2' y 'desc_subgrupo'.")
        
        event.page.update()

    def cambia_Subgrupo(event: ft.ControlEvent):
        subgrupo_id_str = event.control.value
        grupo_id = dd_grupo.data

        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_cuenta.disabled = True
        dd_cuenta.options.append(ft.dropdown.Option(key=None, text="Elige cuenta"))

        if subgrupo_id_str and grupo_id is not None:
            try:
                subgrupo_id = int(subgrupo_id_str)
                seleccion_cuentas = funciones_BD.obtener_datos_cuentas(ruta_BD, grupo_id=grupo_id, subgrupo_id=subgrupo_id)
                cuenta_options = []
                for row_dict in seleccion_cuentas:
                    codigo = row_dict['cod_3']
                    descripcion = row_dict['descripcion_n3']
                    # **Cuentas Display Format: 'cod_3 - descripcion_n3' (already correct)**
                    visible_text = f"{codigo} - {descripcion}"
                    flet_options = ft.dropdown.Option(key=str(codigo), text=visible_text)
                    cuenta_options.append(flet_options)
                dd_cuenta.options.extend(cuenta_options)
                dd_cuenta.disabled = False
            except ValueError:
                print(f"Error: ID de subgrupo o grupo no válido. Grupo: {grupo_id}, Subgrupo: {subgrupo_id_str}")
            except KeyError as e:
                print(f"Error de KeyError al procesar datos de cuentas: {e}. "
                      f"Asegúrate que la tabla CUENTAS tiene las columnas 'cod_3' y 'descripcion_n3'.")
        
        event.page.update()

    dd_grupo.on_change = cambia_Grupo
    dd_subgrupo.on_change = cambia_Subgrupo

    grupos_iniciales = funciones_BD.obtener_datos_grupo(ruta_BD)
    dd_grupo.options.append(ft.dropdown.Option(key=None, text="Elige Grupo"))
    for row_dict in grupos_iniciales:
        id_val = row_dict['grupo_id']
        # **Grupo Display Format: 'grupo_id - desc_grupo'**
        display_text = f"{id_val} - {row_dict['desc_grupo']}"
        dd_grupo.options.append(ft.dropdown.Option(key=str(id_val), text=display_text))

    return ft.Row(
        controls=[
            dd_grupo,
            dd_subgrupo,
            dd_cuenta,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )


def ventana_grupo(ruta_BD):
    dd_grupo = crear_dropdown_grupo()

    grupos_iniciales = funciones_BD.obtener_datos_grupo(ruta_BD)
    dd_grupo.options.append(ft.dropdown.Option(key=None, text="Elige Grupo"))
    for row_dict in grupos_iniciales:
        id_val = row_dict['grupo_id']
        # **Grupo Display Format: 'grupo_id - desc_grupo'**
        display_text = f"{id_val} - {row_dict['desc_grupo']}"
        dd_grupo.options.append(ft.dropdown.Option(key=str(id_val), text=display_text))

    return ft.Row(
        controls=[
            dd_grupo,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )

def ventana_hasta_subgrupo(ruta_BD):
    dd_grupo = crear_dropdown_grupo()
    dd_subgrupo = crear_dropdown_subgrupo()


    dd_subgrupo.disabled = True
    #dd_subgrupo.visible = False


    def cambia_Grupo(event: ft.ControlEvent):
        grupo_id_str = event.control.value
        
        dd_subgrupo.options.clear()
        dd_subgrupo.value = None

        dd_subgrupo.disabled = True

        dd_subgrupo.options.append(ft.dropdown.Option(key=None, text="Elige subgrupo"))


        if grupo_id_str:
            try:
                grupo_id = int(grupo_id_str)
                dd_grupo.data = grupo_id

                seleccion_subgrupo = funciones_BD.obtener_datos_subgrupo(ruta_BD, grupo_id=grupo_id)
                subgrupo_options = []
                for row_dict in seleccion_subgrupo:
                    # **Subgrupo Display Format: 'grupo_id.cod_2 - desc_subgrupo'**
                    # We need the 'grupo_id' from the currently selected group, which is stored in dd_grupo.data
                    # The 'cod_2' and 'desc_subgrupo' come from the current row_dict.
                    display_text = f"{grupo_id}.{row_dict['cod_2']} - {row_dict['desc_subgrupo']}"
                    opcion = ft.dropdown.Option(
                        key=str(row_dict['subgrupo_id']), # Key is still just the subgrupo_id
                        text=display_text
                    )
                    subgrupo_options.append(opcion)
                dd_subgrupo.options.extend(subgrupo_options)
                dd_subgrupo.disabled = False
            except ValueError:
                dd_grupo.data = None
                print(f"Error: ID de grupo no válido: {grupo_id_str}")
            except KeyError as e:
                # Added specific error handling for debugging if column names are wrong
                print(f"Error de KeyError al procesar datos de subgrupos: {e}. "
                      f"Asegúrate que la tabla SUBGRUPO tiene las columnas 'subgrupo_id', 'cod_2' y 'desc_subgrupo'.")
        
        event.page.update()


    dd_grupo.on_change = cambia_Grupo


    grupos_iniciales = funciones_BD.obtener_datos_grupo(ruta_BD)
    dd_grupo.options.append(ft.dropdown.Option(key=None, text="Elige Grupo"))
    for row_dict in grupos_iniciales:
        id_val = row_dict['grupo_id']
        # **Grupo Display Format: 'grupo_id - desc_grupo'**
        display_text = f"{id_val} - {row_dict['desc_grupo']}"
        dd_grupo.options.append(ft.dropdown.Option(key=str(id_val), text=display_text))

    return ft.Row(
        controls=[
            dd_grupo,
            dd_subgrupo,

        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )


'''
def ventana_botones_finales(
    on_click_guardar = None,
    on_click_cancelar = None,
    mostrar_btn_guardar: bool = True,
    mostrar_btn_cancelar: bool = True,
    ):
    """
    Crea una fila horizontal con botones "Grabar" y "Cancelar",
    cuya visibilidad puede ser controlada por parámetros.
    """
    controles_botones = []
 
    # Crear el botón "Grabar" si mostrar_btn_guardar es True
    if mostrar_btn_guardar:
        btn_guardar = ft.ElevatedButton(
            "Grabar",
            icon=ft.Icons.SAVE,
            on_click=on_click_guardar,
            # Puedes añadir tu lógica de guardado aquí
        )
        controles_botones.append(btn_guardar)

    # Crear el botón "Cancelar" si mostrar_btn_cancelar es True
    if mostrar_btn_cancelar:
        btn_cancelar = ft.OutlinedButton( # Usamos OutlinedButton para distinguirlo
            "Cancelar",
            icon=ft.Icons.CANCEL,
            on_click=on_click_cancelar,
            # Puedes añadir tu lógica de cancelación aquí
        )
        controles_botones.append(btn_cancelar)

    # Devolvemos una Row que contiene solo los botones que se han añadido
    return ft.Row(
        controls=controles_botones,
        spacing=10, # Espacio entre los botones
        alignment=ft.MainAxisAlignment.CENTER # Alineación de los botones en la fila
    )

'''