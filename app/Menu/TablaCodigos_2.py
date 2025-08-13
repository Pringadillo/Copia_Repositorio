import flet as ft
import datetime
import sqlite3

import sys
import os

import globals
from app.data.funciones_BD import mostrar_cuentas_por_grupo_flet2, insertar_datos_cuenta



#ruta_BDapp = globals.ruta_BD

def menu_TablaDeCodigos():
    """
    Esta función construye y retorna la vista principal de la "Tabla de Códigos".
    Maneja la visibilidad de los botones de configuración y el cambio de contenido
    en el área principal de la tabla.
    """
    ruta_BDapp = globals.ruta_BD

    # 1. Cargar datos iniciales para las 4 columnas
    # (Estos datos son simulados por 'mostrar_cuentas_por_grupo_flet2')
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 1) # Cuentas Financieras
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 2) # Deudas
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 3) # Gastos
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 4) # Ingresos


    # --- Definición del Contenedor Principal de la Tabla de Códigos ---
    # Este es el contenedor que contendrá el contenido dinámico.
    # Se inicializa con las 4 columnas de datos.
    # IMPORTANTE: Se define aquí para que las funciones de acción puedan referenciarlo.
    TablaCodigo_contenido = ft.Container(
        content=ft.Row( # <-- Contenido inicial: las 4 columnas
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),

                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False, expand=True
        ),
        padding=10, expand=True
    )

    # --- Funciones para cambiar el contenido de TablaCodigo_contenido ---
    # Nota: Reciben 'container_to_update' (que es TablaCodigo_contenido) y 'page'

    # Función para volver a cargar los datos por si acaso han cambiado o se han añadido nuevos
    def reset_tabla_codigo_contenido(e, container_to_update, page):
        """Restaura el contenido de TablaCodigo_contenido a la vista de las 4 columnas."""
        # Vuelve a cargar los datos por si acaso han cambiado o se han añadido nuevos
        _controles_cuentas1 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 1)
        _controles_cuentas2 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 2)
        _controles_cuentas3 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 3)
        _controles_cuentas4 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 4)

        container_to_update.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=_controles_cuentas1,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                ft.Container(
                    content=ft.Column(
                        controls=_controles_cuentas2,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),
                ft.Container(
                    content=ft.Column(
                        controls=_controles_cuentas3,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),
                ft.Container(
                    content=ft.Column(
                        controls=_controles_cuentas4,
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, expand=True,
                    ),
                    expand=True, bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10), border_radius=ft.border_radius.all(10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False, expand=True
        )
        page.update()

    # fUNCIONES de las acciones de los botones
    def crear_subcuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Crear Subcuenta".
        Reemplaza el contenido de un contenedor objetivo con un formulario para
        crear una nueva subcuenta.
        """

        instrucciones = ft.Text(
            spans=[
                ft.TextSpan(
                    "Instrucciones\n",  # La línea 1 con el encabezado y un salto de línea
                    ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
                ),
                ft.TextSpan(
                    "Vas a crear una SUBCUENTA, revisa previamente que no exista.\n" # La línea 2 con las instrucciones
                ),
                ft.TextSpan(
                    "Utiliza un concepto corto y descriptivo, que englobe a las cuentas que representará \n" # La línea 3
                ),
            ],
            size=16, # Puedes establecer el tamaño base para el resto del texto
            text_align=ft.TextAlign.LEFT # Alinear el texto a la izquierda
        )




        
        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        dynamic_dropdown_selectors = globals.ventana_hasta_subgrupo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("Crear nuevo SUBGRUPO", size=20, weight=ft.FontWeight.BOLD),
                dynamic_dropdown_selectors,
                instrucciones,
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Nombre SUBGRUPO",
                            hint_text="Ej: Gastos Extra",
                            width=500
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True
        )

        # Actualiza el contenido del contenedor y la página.
        container_to_update.content = new_content_column
        container_to_update.update()
        page.update()
        
    def crear_cuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Crear Código".
        Reemplaza el contenido de un contenedor objetivo con un formulario para
        crear un nuevo código. Este formulario incluye desplegables en cascada
        para Grupo, Subgrupo y Cuentas, y un botón para volver a la vista anterior.

        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """

        # Llama a 'ventana_codigo' desde el módulo 'globals' para obtener un control Row
        # que contiene los tres desplegables en cascada (Grupo, Subgrupo, Cuentas).
        dynamic_dropdown_selectors = globals.ventana_codigo(ruta_BDapp)
        cancelar = lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page)
        guardar = lambda ev: insertar_datos_cuenta()
        botones_final_ventana = globals.ventana_botones_finales(on_click_cancelar=cancelar, mostrar_btn_guardar=guardar)
        


        # Crea un nuevo control Column para agrupar todos los elementos del formulario
        new_content_column = ft.Column(
            controls=[
                ft.Text("Crear Nuevo Código", size=20, weight=ft.FontWeight.BOLD),
                dynamic_dropdown_selectors,
                ft.Row(
                    controls =[ft.TextField(label="Nombre del Código", 
                                            hint_text="Ej: Alquiler", 
                                            width=500),
                                            
                    ],
                    alignment=ft.MainAxisAlignment.START,
                 ),
                botones_final_ventana,
                ft.FilledButton(text="Guardar Código", icon=ft.Icons.SAVE),
                ft.FilledButton(text="Volver", on_click=cancelar, icon=ft.Icons.ARROW_BACK),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True
        )

        # Actualiza el contenido del contenedor objetivo para mostrar el nuevo formulario.
        container_to_update.content = new_content_column
        container_to_update.update() # Update the specific container itself
        page.update() # Then update the whole page to propagate changes
   
    def editar_subcuenta(e, container_to_update, page):
        """Muestra un formulario para editar un código existente."""
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("FORMULARIO: Editar Código Existente", size=20, weight=ft.FontWeight.BOLD),
                ft.Dropdown(
                    label="Seleccionar Código a Editar",
                    options=[
                        ft.dropdown.Option("Gasto: Comida"),
                        ft.dropdown.Option("Ingreso: Salario"),
                        ft.dropdown.Option("Deuda: Tarjeta de Crédito"),
                    ],
                    hint_text="Elige el código a modificar"
                ),
                ft.TextField(label="Nuevo Nombre del Código", hint_text="Ej: Comida del Mes"),
                ft.FilledButton(text="Actualizar Código", icon=ft.Icons.UPDATE),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True # ¡CORRECCIÓN CLAVE!
        )
        page.update()

    def editar_cuenta(e, container_to_update, page):
        """Muestra un formulario para editar un código existente."""
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("FORMULARIO: Editar Código Existente", size=20, weight=ft.FontWeight.BOLD),
                ft.Dropdown(
                    label="Seleccionar Código a Editar",
                    options=[
                        ft.dropdown.Option("Gasto: Comida"),
                        ft.dropdown.Option("Ingreso: Salario"),
                        ft.dropdown.Option("Deuda: Tarjeta de Crédito"),
                    ],
                    hint_text="Elige el código a modificar"
                ),
                ft.TextField(label="Nuevo Nombre del Código", hint_text="Ej: Comida del Mes"),
                ft.FilledButton(text="Actualizar Código", icon=ft.Icons.UPDATE),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True # ¡CORRECCIÓN CLAVE!
        )
        page.update()

    def eliminar_subcuenta(e, container_to_update, page):
        """Muestra una confirmación para eliminar un código."""
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("¿CONFIRMAR ELIMINACIÓN DE CÓDIGO?", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ft.Dropdown(
                    label="Seleccionar Código a Eliminar",
                    options=[
                        ft.dropdown.Option("Gasto: Transporte"),
                        ft.dropdown.Option("Deuda: Préstamo Automóvil"),
                    ],
                    hint_text="Elige el código a eliminar"
                ),
                ft.FilledButton(text="Eliminar Código Permanentemente", icon=ft.Icons.WARNING, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_ACCENT_700)),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True # ¡CORRECCIÓN CLAVE!
        )
        page.update()

    def eliminar_cuenta(e, container_to_update, page):
        """Muestra una confirmación para eliminar un código."""
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("¿CONFIRMAR ELIMINACIÓN DE CÓDIGO?", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ft.Dropdown(
                    label="Seleccionar Código a Eliminar",
                    options=[
                        ft.dropdown.Option("Gasto: Transporte"),
                        ft.dropdown.Option("Deuda: Préstamo Automóvil"),
                    ],
                    hint_text="Elige el código a eliminar"
                ),
                ft.FilledButton(text="Eliminar Código Permanentemente", icon=ft.Icons.WARNING, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_ACCENT_700)),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True # ¡CORRECCIÓN CLAVE!
        )
        page.update()



    # --- Título de la Tabla Códigos ---
    TablaCodigo_titulo = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=20),
                            ft.Text("Configurar Tabla Códigos", size=16)
                        ],
                        spacing=5,
                    ),
                    # Llama a la función para alternar la visibilidad del subtítulo
                    on_click=lambda e: toggle_subtitulo_visibility(e),
                    tooltip="Mostrar/Ocultar opciones de configuración",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=150,
        ),
    )

    # --- Subtítulo de la tabla Códigos (contiene los botones de acción) ---
    # Inicialmente invisible. Su visibilidad se controla con el botón de configuración.
    # IMPORTANTE: Se define aquí para que toggle_subtitulo_visibility pueda referenciarlo.
    TablaCodigo_subtitulo = ft.Container(
        content=ft.Row(
            controls=[
                ft.FilledButton(
                    text="Crear Subgrupo",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: crear_subcuenta(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Crear Cuenta",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: crear_cuenta(e, TablaCodigo_contenido, e.page)
                ),                
                ft.FilledButton(
                    text="Editar Subgrupo",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: editar_subcuenta(e, TablaCodigo_contenido, e.page)
                ),
                 ft.FilledButton(
                    text="Editar Cuenta",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: editar_cuenta(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Eliminar Subgrupo",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e: eliminar_subcuenta(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Eliminar Cuenta",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e: eliminar_cuenta(e, TablaCodigo_contenido, e.page)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False, # ¡Inicialmente invisible!
        padding=ft.padding.only(top=10, bottom=10),
    )

    # --- Función para alternar la visibilidad del subtítulo ---
    # Esta función se define después de que TablaCodigo_subtitulo ya exista.
    def toggle_subtitulo_visibility(e):
        TablaCodigo_subtitulo.visible = not TablaCodigo_subtitulo.visible
        e.page.update() # Actualiza la UI para mostrar/ocultar el subtítulo

    
    # ---------------------- Estructura principal de la vista -----------------
    # Agrupa todos los elementos definidos anteriormente en un Column
    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                TablaCodigo_titulo,
                TablaCodigo_subtitulo,
                TablaCodigo_contenido, # Este es el contenedor que cambia de contenido
                
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor=ft.Colors.WHITE,
        expand=True # Permite que el contenedor principal ocupe el espacio disponible
    )

    # Retorna el contenido para ser añadido a la página principal de Flet
    return globals.contenido_central_container.content



