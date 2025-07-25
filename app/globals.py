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

# se ha de mejorar, no funciona
# # habria que ponerlo en un archivo a parte
def ventana_codigo():
    """
    Crea y devuelve un ft.Row que contiene tres ft.Dropdowns (Grupo, Subgrupo, Cuenta)
    con lógica de dependencia para actualizar las opciones.

    Retorna:
        ft.Row: Un control Row que contiene los tres desplegables.
    """
    # 1. Definir los desplegables
    # Es crucial que sean variables para poder modificar sus opciones y valores.
    dd_grupo = ft.Dropdown(
        label="Grupo",
        width=200,
        text_size=16,
        options=[], # Se poblará más abajo
        hint_text="Elige Grupo",
        border_radius=ft.border_radius.all(8) # Añadido para consistencia visual
    )

    dd_subgrupo = ft.Dropdown(
        label="Subgrupo",
        width=250,
        text_size=16,
        options=[],
        disabled=True, # Inicialmente deshabilitado hasta que se seleccione un grupo
        hint_text="Elige Subgrupo",
        border_radius=ft.border_radius.all(8) # Añadido para consistencia visual
    )

    dd_cuenta = ft.Dropdown(
        label="Cuenta",
        width=300,
        text_size=16,
        options=[],
        disabled=True, # Inicialmente deshabilitado hasta que se seleccione un subgrupo
        hint_text="Elige Cuenta",
        border_radius=ft.border_radius.all(8) # Añadido para consistencia visual
    )

    # 2. Definir las funciones de manejo de cambios (on_change)
    def cambia_Grupo(event: ft.ControlEvent):
        """
        Maneja el cambio en el Dropdown de Grupo.
        Carga las opciones del Subgrupo y deshabilita/habilita los desplegables.
        """
        # El 'value' de un Dropdown.Option es su 'key' si se especifica,
        # o su 'text' si solo se da un string. Aquí esperamos el 'key' (el ID).
        grupo_id = event.control.value

        # Limpiar y resetear los desplegables dependientes
        dd_subgrupo.options.clear()
        dd_subgrupo.value = None
        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_subgrupo.disabled = True
        dd_cuenta.disabled = True

        if grupo_id: # Asegurarse de que se ha seleccionado un grupo válido (no None o 'Elige Grupo')
            try:
                # Almacenar el ID del grupo seleccionado en la propiedad 'data' del dd_grupo
                # Esto es útil si necesitas acceder al ID del grupo desde dd_subgrupo o dd_cuenta
                dd_grupo.data = int(grupo_id)

                # Obtener subgrupos basados en el grupo_id
                seleccion_subgrupo = obtener_datos_subgrupo(globals.ruta_BDapp, grupo_id=int(grupo_id))

                # Llenar el Dropdown de subgrupos
                subgrupo_options = []
                # Añadir la opción por defecto "Elige subgrupo"
                subgrupo_options.append(ft.dropdown.Option(key=None, text="Elige subgrupo"))

                for id_val, nombre_completo in seleccion_subgrupo:
                    # Usamos el id_val como key y el nombre_completo como text
                    opcion = ft.dropdown.Option(key=str(id_val), text=nombre_completo)
                    subgrupo_options.append(opcion)

                dd_subgrupo.options.extend(subgrupo_options)
                dd_subgrupo.disabled = False # Habilita el dropdown de subgrupos

            except ValueError:
                # Manejar el caso si el ID no es un número (ej. si 'Elige Grupo' tuviera un ID numérico)
                dd_grupo.data = None
                print(f"Error: ID de grupo no válido: {grupo_id}")
        
        # Siempre actualizar la página al final de la función de cambio
        event.page.update()

    def cambia_Subgrupo(event: ft.ControlEvent):
        """
        Maneja el cambio en el Dropdown de Subgrupo.
        Carga las opciones de Cuenta y deshabilita/habilita el desplegable de Cuenta.
        """
        subgrupo_id = event.control.value # Esperamos que el 'value' sea el ID del subgrupo
        grupo_id = dd_grupo.data # Recuperamos el ID del grupo almacenado en dd_grupo.data

        # Limpiar y resetear el desplegable de Cuenta
        dd_cuenta.options.clear()
        dd_cuenta.value = None
        dd_cuenta.disabled = True

        if subgrupo_id and grupo_id is not None: # Asegurarse de que se ha seleccionado un subgrupo y un grupo válidos
            try:
                # Obtener cuentas basadas en el grupo_id y subgrupo_id
                seleccion_cuentas = obtener_datos_cuentas(globals.ruta_BDapp, grupo_id=int(grupo_id), subgrupo_id=int(subgrupo_id))

                cuenta_options = []
                # Añadir la opción por defecto "Elige cuenta"
                cuenta_options.append(ft.dropdown.Option(key=None, text="Elige cuenta"))

                for codigo, descripcion in seleccion_cuentas:
                    # Usamos el código completo como key y la descripción como text
                    visible_text = f"{codigo} {descripcion}"
                    flet_options = ft.dropdown.Option(key=codigo, text=visible_text)
                    cuenta_options.append(flet_options)

                dd_cuenta.options.extend(cuenta_options)
                dd_cuenta.disabled = False # Habilita el dropdown de cuentas

            except ValueError:
                print(f"Error: ID de subgrupo o grupo no válido. Grupo: {grupo_id}, Subgrupo: {subgrupo_id}")
        
        # Siempre actualizar la página al final
        event.page.update()

    # 3. Asignar las funciones de manejo de cambios a los desplegables
    dd_grupo.on_change = cambia_Grupo
    dd_subgrupo.on_change = cambia_Subgrupo

    # 4. Poblar el Dropdown de Grupo con los datos iniciales
    # Esto debe hacerse DESPUÉS de definir dd_grupo y sus on_change,
    # pero ANTES de devolver el Row.
    grupos_iniciales = obtener_datos_grupo(globals.ruta_BDapp)
    dd_grupo.options.append(ft.dropdown.Option(key=None, text="Elige Grupo")) # Opción por defecto
    for id_val, nombre_completo in grupos_iniciales:
        # Usamos el id_val como key y el nombre_completo como text
        dd_grupo.options.append(ft.dropdown.Option(key=str(id_val), text=nombre_completo))

    # 5. Devolver el ft.Row que contiene los tres desplegables
    return ft.Row(
        controls=[
            dd_grupo,
            dd_subgrupo,
            dd_cuenta,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )




 


