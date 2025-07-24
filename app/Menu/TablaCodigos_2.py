import flet as ft
import datetime
import sqlite3

import sys
import os

import globals
from app.data.funciones_BD import mostrar_datos_grupo, obtener_datos_grupo, obtener_datos_subgrupo, mostrar_cuentas_por_grupo_flet, mostrar_cuentas_por_grupo_flet2

def proves2():
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    datos_nivel1 = obtener_datos_grupo(ruta_BDapp)
    # Extrae solo el segundo elemento (el texto) de cada tupla
    textos_nivel1 = [f"{item[0]}   {item[1]}" for item in datos_nivel1]


    texto1 = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        #bgcolor=ft.Colors.BLUE_GREY_200,
        margin=ft.margin.only(top=20) 
    )

    texto2 = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(textos_nivel1[0], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER),
                            ft.Container(
                                content=ft.Text(textos_nivel1),
                                #ft.Text("• Cuenta Corriente\n• Cuenta de Ahorro\n• Inversiones"),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(textos_nivel1[1], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Tarjeta de Crédito\n• Préstamo Hipotecario\n• Préstamo Personal"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(textos_nivel1[2], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Alquiler/Hipoteca\n• Alimentación\n• Transporte\n• Servicios"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(textos_nivel1[3], weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER), # <--- text_align para el título
                            ft.Text("• Salario\n• Freelance\n• Intereses/Dividendos"),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # <--- Centra los elementos horizontalmente en esta columna
                        run_spacing=5
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True
        ),
        padding=10,
        expand=True
    )

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            #alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content

def proves3():
        
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 4)

    texto1 = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        #bgcolor=ft.Colors.BLUE_GREY_200,
        margin=ft.margin.only(top=20) 
    )
    
    texto2 = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True

        ),

        padding=10,
        expand=True
        
    )

    # ----------------------  Estructura principal -----------------

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
    
def proves4():
        
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 4)

    # funciones de la configuracion de la tabla
    def open_rename_dialog(e):
        pass

    def open_create_subgroup_dialog(e):
        pass

    def open_create_group_dialog(e):
        pass

    def open_create_cuenta_dialog(e):
        pass

    def close_dialog(e):
        pass





    texto1 = ft.Container(
        content= ft.Row(  
            controls=[
                ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Renombrar Código",
                            icon=ft.Icons.EDIT,
                            on_click=open_rename_dialog
                        ),
                        ft.PopupMenuItem(
                            text="Crear Grupo",
                            icon=ft.Icons.CREATE_NEW_FOLDER,
                            on_click=open_create_group_dialog
                        ),
                        ft.PopupMenuItem(
                            text="Crear Subgrupo",
                            icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                            on_click=open_create_subgroup_dialog
                        ),
                        ft.PopupMenuItem(
                            text="Crear Cuenta",
                            icon=ft.Icons.ACCOUNT_TREE_OUTLINED,
                            on_click=open_create_cuenta_dialog
                        ),
                    ],
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=20),  # Icono de menú
                            ft.Text("Configuraciones Tabla", size=16)  # Texto del menú
                        ],
                        spacing=5, # Espacio entre el icono y el texto
                        
                    ),
                    tooltip="Configuraciones para la Tabla",
                ),
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            spacing=150,  # Espacio entre el título y el menú
        ),
    )

    
    texto2 = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True

        ),

        padding=10,
        expand=True
        
    )

    # ----------------------  Estructura principal -----------------

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
   
def proves5():
        
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 4)

    # funciones de la configuracion de la tabla
    def crear_codigo(e):
        pass

    def modificar_codigo(e):
        pass

    def bloquear_codigo(e):
        pass

    def close_dialog(page:ft.Page):
        page.dialog.open = False
        page.update()





    # Título de la Tabla Códigos
    TablaCodigo_titulo = ft.Container(
        content= ft.Row(  
            controls=[
                ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.PopupMenuButton(
                            items=[
                                ft.PopupMenuItem(
                                    text="Crear Código",
                                    icon=ft.Icons.ADD,
                                    on_click=crear_codigo
                                ),
                                ft.PopupMenuItem(
                                    text="Modificar Código",
                                    icon=ft.Icons.EDIT,
                                    on_click=modificar_codigo
                                ),
                                ft.PopupMenuItem(
                                    text="Bloquear Código",
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    on_click=bloquear_codigo
                                ),
                            ],
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=20),  # Icono de menú
                                    ft.Text("Configurar Tabla Códigos", size=16)  # Texto del menú
                                ],
                                spacing=5, # Espacio entre el icono y el texto
                                
                            ),
                            tooltip="Configurar los códigos de la Tabla",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  
                    spacing=150,  # Espacio entre el título y el menú
                ),
            )

    # Subtitulo de la tabla Códigos
    TablaCodigo_subtitulo=""
    
    # Cuerpo de Tabla Códigos
    TablaCodigo_contenido = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True

        ),

        padding=10,
        expand=True
        
    )



    # ----------------------  Estructura principal -----------------

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                TablaCodigo_titulo,
                TablaCodigo_subtitulo,
                TablaCodigo_contenido,
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
   
def proves6():

    # --- Funciones de acción para los botones del subtítulo ---
    # Estas funciones se llamarán cuando los botones "Crear", "Editar", "Eliminar" sean presionados.
    # Por ahora, solo actualizan el contenido de TablaCodigo_contenido.
    # ¡Recuerda llamar a e.page.update() para que los cambios se muestren!

    def crear_codigo_accion(e):
        print("Botón 'Crear Código' presionado.")
        # Modificar TablaCodigo_contenido
        # Accede al contenedor principal a través de 'e.page' o 'globals' si lo gestionas así.
        # Necesitamos una referencia a TablaCodigo_contenido que sea accesible aquí.
        # Una forma es que mi_funcion_principal devuelva los componentes o los haga accesibles.
        # Para este ejemplo, simularé el cambio asumiendo que TablaCodigo_contenido es accesible.
        if globals.contenido_central_container.content and \
        isinstance(globals.contenido_central_container.content.content, ft.Column) and \
        len(globals.contenido_central_container.content.content.controls) > 2:
            # Asumiendo que TablaCodigo_contenido es el tercer control en el Column principal
            tabla_contenido_ref = globals.contenido_central_container.content.content.controls[2]
            tabla_contenido_ref.content = ft.Column(
                controls=[
                    ft.Text("Formulario para CREAR un nuevo código.", size=18, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Nombre del Código"),
                    ft.TextField(label="Descripción"),
                    ft.ElevatedButton("Guardar Nuevo Código"),
                ]
            )
            e.page.update()


    def editar_codigo_accion(e):
        print("Botón 'Editar Código' presionado.")
        if globals.contenido_central_container.content and \
        isinstance(globals.contenido_central_container.content.content, ft.Column) and \
        len(globals.contenido_central_container.content.content.controls) > 2:
            tabla_contenido_ref = globals.contenido_central_container.content.content.controls[2]
            tabla_contenido_ref.content = ft.Column(
                controls=[
                    ft.Text("Formulario para EDITAR un código existente.", size=18, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(label="Seleccionar Código", options=[ft.dropdown.Option("COD001"), ft.dropdown.Option("COD002")]),
                    ft.TextField(label="Nuevo Nombre"),
                    ft.ElevatedButton("Guardar Cambios"),
                ]
            )
            e.page.update()


    def eliminar_codigo_accion(e):
        print("Botón 'Eliminar Código' presionado.")
        if globals.contenido_central_container.content and \
        isinstance(globals.contenido_central_container.content.content, ft.Column) and \
        len(globals.contenido_central_container.content.content.controls) > 2:
            tabla_contenido_ref = globals.contenido_central_container.content.content.controls[2]
            tabla_contenido_ref.content = ft.Column(
                controls=[
                    ft.Text("Confirma la ELIMINACIÓN de un código.", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                    ft.Dropdown(label="Código a Eliminar", options=[ft.dropdown.Option("COD001"), ft.dropdown.Option("COD002")]),
                    ft.ElevatedButton("Eliminar Código", style=ft.ButtonStyle(bgcolor=ft.colors.RED_500, color=ft.colors.WHITE)),
                ]
            )
            e.page.update()

    # --- Función principal que construye la interfaz de usuario ---
    def mi_funcion_principal():
        # El subtítulo y sus botones, inicialmente ocultos
        TablaCodigo_subtitulo_content = ft.Row(
            controls=[
                ft.FilledButton(
                    text="Crear Código",
                    icon=ft.Icons.ADD,
                    on_click=crear_codigo_accion # Llama a la función que actualiza TablaCodigo_contenido
                ),
                ft.FilledButton(
                    text="Editar Código",
                    icon=ft.Icons.EDIT,
                    on_click=editar_codigo_accion # Llama a la función que actualiza TablaCodigo_contenido
                ),
                ft.FilledButton(
                    text="Eliminar Código",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=eliminar_codigo_accion # Llama a la función que actualiza TablaCodigo_contenido
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START # Alinea los botones a la izquierda
        )

        # Contenedor para el subtítulo y sus botones, inicialmente invisible
        subtitulo_container = ft.Container(
            content=TablaCodigo_subtitulo_content,
            visible=False,
            padding=ft.padding.only(top=10, bottom=10), # Pequeño padding para separación
        )

        # Botón principal para mostrar/ocultar TablaCodigo_subtitulo
        def toggle_subtitulo_visibility(e):
            subtitulo_container.visible = not subtitulo_container.visible
            e.page.update() # Muy importante para que los cambios se reflejen en la UI

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
                        on_click=toggle_subtitulo_visibility, # Este botón controlará la visibilidad
                        tooltip="Mostrar/Ocultar opciones de configuración",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=150, # Espacio entre el título y el botón
            ),
        )

        # Esta es la sección que tus funciones de acción modificarán.
        TablaCodigo_contenido = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Contenido principal de la tabla de códigos.", size=18),
                    ft.Text("Aquí se mostrará la información relevante según la acción seleccionada.", size=14, color=ft.Colors.GREY_600),
                ],
                spacing=10
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_GREY_50,
            border_radius=10,
            expand=True, # Para que ocupe el espacio disponible
        )

        # ---------------------- Estructura principal -----------------

        globals.contenido_central_container.content = ft.Container(
            content=ft.Column(
                controls=[
                    TablaCodigo_titulo,
                    subtitulo_container, # El contenedor con los 3 botones
                    TablaCodigo_contenido, # El contenido que se modificará
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centra el contenido horizontalmente
                spacing=20, # Espacio entre los controles principales
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20, # Un poco de padding general
            expand=True, # Para que el contenedor principal ocupe todo el espacio
        )

        return globals.contenido_central_container.content

def proves7():
    
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet2(ruta_BDapp, 4)


    # Título de la Tabla Códigos ----------------------------------

    # creamos previamente la funcion de hacer visible TablaCodigo_subtitulo
    def toggle_subtitulo_visibility(e):
        TablaCodigo_subtitulo.visible = not TablaCodigo_subtitulo.visible
        e.page.update() # Actualiza la UI para mostrar/ocultar el subtítulo


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
                    on_click=toggle_subtitulo_visibility, # Este botón controla la visibilidad
                    tooltip="Mostrar/Ocultar opciones de configuración",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=150, # Espacio entre el título y el botón
        ),
    )
    # Subtitulo de la tabla Códigos --------------------------------
    
    def reset_tabla_codigo_contenido(e, container_to_update, page):
        # This function would put back the original 4-column layout
        # For simplicity here, I'll put a placeholder. In your full code,
        # you'd re-create the ft.Row with the four containers.
        container_to_update.content = ft.Text("Contenido original de la tabla de códigos", size=18, color=ft.colors.BLUE_GREY_700)
        page.update()

    #funciones de los botones
    def crear_codigo_accion(e, container_to_update, page):
        # Example content for creating a code
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("Formulario de Creación", size=20),
                ft.TextField(label="Nombre"),
                ft.FilledButton(text="Guardar", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page))
            ]
        )
        page.update()

    def editar_codigo_accion(e, container_to_update, page):
        # Example content for editing a code
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("Formulario de Edición", size=20),
                ft.TextField(label="ID a editar"),
                ft.FilledButton(text="Actualizar", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page))
            ]
        )
        page.update()

    def eliminar_codigo_accion(e, container_to_update, page):
        # Example content for deleting a code
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("Confirmar Eliminación", size=20, color=ft.colors.RED),
                ft.Text("¿Estás seguro?", size=16),
                ft.FilledButton(text="Sí, eliminar", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page))
            ]
        )
        page.update()

    # Contiene los 3 botones, y su visibilidad será controlada.
    # Inicialmente está invisible.
    TablaCodigo_subtitulo = ft.Container(
        content=ft.Row(
            controls=[
                ft.FilledButton(
                    text="Crear Código",
                    icon=ft.Icons.ADD,
                    # Corrected: Removed the duplicate 'on_click='
                    on_click=lambda e: crear_codigo_accion(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Editar Código",
                    icon=ft.Icons.EDIT,
                    # Corrected: Removed the duplicate 'on_click='
                    on_click=lambda e: editar_codigo_accion(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Eliminar Código",
                    icon=ft.Icons.DELETE_OUTLINE,
                    # Corrected: Removed the duplicate 'on_click='
                    on_click=lambda e: eliminar_codigo_accion(e, TablaCodigo_contenido, e.page)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False, # ¡Inicialmente invisible!
        padding=ft.padding.only(top=10, bottom=10),
     )
   
    # Cuerpo de Tabla Códigos ---------------------------------------
    TablaCodigo_contenido = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True

        ),

        padding=10,
        expand=True
        
    )

    # ----------------------  Estructura principal -----------------

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                TablaCodigo_titulo,
                TablaCodigo_subtitulo,
                TablaCodigo_contenido,
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
   
def proves8():
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


    def crear_codigo_accion(e, container_to_update, page):
        """Muestra un formulario para crear un nuevo código."""
        container_to_update.content = ft.Column(
            controls=[
                ft.Text("FORMULARIO: Crear Nuevo Código", size=20, weight=ft.FontWeight.BOLD),
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
            expand=True # ¡CORRECCIÓN CLAVE! Asegura que el Column ocupe el espacio disponible.
        )
        page.update() # ¡Importante! Actualiza la UI para mostrar el nuevo contenido.

    def editar_codigo_accion(e, container_to_update, page):
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

    def eliminar_codigo_accion(e, container_to_update, page):
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
                    text="Crear Código",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: crear_codigo_accion(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Editar Código",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: editar_codigo_accion(e, TablaCodigo_contenido, e.page)
                ),
                ft.FilledButton(
                    text="Eliminar Código",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e: eliminar_codigo_accion(e, TablaCodigo_contenido, e.page)
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
