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


    def Subcuenta_accion_crear(e, container_to_update, page):
        print ("CREANDO SUBGRUPO")
        pass
    def Subcuenta_accion_modificar(e, container_to_update, page):
        print ("modificandeo SUBGRUPO")
        pass
    def Subcuenta_accion_eliminar(e, container_to_update, page):
        print ("eliminando SUBGRUPO")
        pass

    def Cuenta_accion_crear(e, container_to_update, page):
        print ("CREANDO cuenta")
        pass
    def Cuenta_accion_modificar(e, container_to_update, page):
        print ("modificancod cuenat")
        pass
    def Cuenta_accion_eliminar(e, container_to_update, page):
        print ("eliminando CUENTA")
        pass





    # fUNCIONES  de los botones
    def btn_crear_subcuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Crear Subcuenta".
        crear un nuevo SUBGRUPO, a partir de escoger el GRUPO.
        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """
        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge en grupo donde crear el subgrupo"),
                ft.Text("2º Revisa en el desplegable SUBGRUPO, para que no exista un concepto parecido"),
                ft.Text("3º Si aún así crees que necesitas un nuevo SUBGRUPO"),
                ft.Text("\t\tUtiliza un concepto corto y descriptivo, que englobe a las cuentas que representará"),
                ft.Text("\t\tCrear para tener el nuevo SUBGRUPO\n\t\tVolver para cancelar")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column]
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200, # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        dynamic_dropdown_selectors = globals.ventana_hasta_subgrupo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("Crear nuevo SUBGRUPO", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,
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
                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Crear Subgrupo",
                            on_click=lambda e: Subcuenta_accion_crear(e, container_to_update, page)
                        ),
                        ft.ElevatedButton(
                            text="Volver",
                            on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page),
                            icon=ft.Icons.ARROW_BACK
                        ),
                        #ft.Container(width=30) # Añade este espaciador
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
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

    def btn_editar_subcuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Crear Subcuenta".
        Modifica el nombre de un SUBGRUPO
        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """
        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge el grupo al que pertenece el SUBGRUPO"),
                ft.Text("2º del desplegable SUBGRUPO escoge el que deseas editar"),
                ft.Text("3º Escribe el nuevo contenido para el SUBGRUPO"),
                ft.Text(
                    "\t\tUtiliza un concepto corto y descriptivo, que englobe a las cuentas que representará"
                ),
                ft.Text(
                    "\t\tActualizar para modificar el SUBGRUPO\n\t\tVolver para cancelar"
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column],
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200,  # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        # Se asume que 'globals.ventana_hasta_subgrupo' y 'ruta_BDapp' están definidos.
        dynamic_dropdown_selectors = globals.ventana_hasta_subgrupo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("editar SUBGRUPO", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Nombre SUBGRUPO", hint_text="Ej: Gastos Extra", width=500
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Actualizar Subgrupo",
                            on_click=lambda e: Subcuenta_accion_modificar(
                                e, container_to_update, page
                            ),
                            icon=ft.icons.UPDATE,  
                        ),
                        ft.ElevatedButton(
                            text="Volver",
                            on_click=lambda ev: reset_tabla_codigo_contenido(
                                ev, container_to_update, page
                            ),
                            icon=ft.icons.ARROW_BACK, 
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        )

        # Actualiza el contenido del contenedor y la página.
        container_to_update.content = new_content_column
        container_to_update.update()
        page.update()
   
    def btn_eliminar_subcuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Eliminar Subcuenta".
        Elimina el SUBGRUPO escogido
        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """
        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge el grupo al que pertenece SUBGRUPO"),
                ft.Text("2º del desplegable SUBGRUPO escoge el que deseas ELIMINAR"),
                ft.Text("RECUERDA: "),
                ft.Text(
                    "\t\tNo se puede eliminar un SUBGRUPO con cuentas asociadas"
                ),
                ft.Text(
                    "\t\tNo se puede eliminar un SUBGRUPO con importe diferente a cero"
                ),
                ft.Text(
                    "\t\tUna vez eliminado un SUBGRUPO, no se puede recuperar"
                ),
                ft.Text(
                    "\t\tEliminar para borrar el SUBGRUPO\n\t\tVolver para cancelar"
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column],
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200,  # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        # Se asume que 'globals.ventana_hasta_subgrupo' y 'ruta_BDapp' están definidos.
        dynamic_dropdown_selectors = globals.ventana_hasta_subgrupo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("Eliminar SUBGRUPO", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,

                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.FilledButton(text="Eliminar Código Permanentemente", on_click=lambda ev: Subcuenta_accion_eliminar(ev, container_to_update, page), icon=ft.Icons.WARNING, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_ACCENT_700)),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        )

        # Actualiza el contenido del contenedor y la página.
        container_to_update.content = new_content_column
        container_to_update.update()
        page.update()

    def btn_crear_cuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Crear Cuenta".
        Este formulario incluye desplegables en cascada
        para Grupo, Subgrupo y Cuentas.

        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """

        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge en grupo y subgrupo"),
                ft.Text("2º Revisa en el desplegable CUENTA, para que no exista un concepto parecido"),
                ft.Text("3º Si aún así crees que necesitas una nueva CUENTA"),
                ft.Text("\t\tUtiliza un concepto corto y descriptivo"),
                ft.Text("\t\tCrear para tener el nuevo SUBGRUPO\n\t\tVolver para cancelar")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column]
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200, # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        dynamic_dropdown_selectors = globals.ventana_codigo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("Crear nueva CUENTA", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Nombre CUENTA",
                            hint_text="Ej: gasolina",
                            width=500
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Crear Cuenta",
                            on_click=lambda e: Cuenta_accion_crear(e, container_to_update, page)
                        ),
                        ft.ElevatedButton(
                            text="Volver",
                            on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page),
                            icon=ft.Icons.ARROW_BACK
                        ),
                        #ft.Container(width=30) # Añade este espaciador
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
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

    def btn_editar_cuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Editar Subcuenta".
        Modifica el nombre de la Cuenta seleccionada
        Args:
            e (ft.ControlEvent): El objeto evento del clic del botón.
            container_to_update (ft.Container): El contenedor de Flet cuyo contenido
                                            será reemplazado por el nuevo formulario de creación de código.
            page (ft.Page): El objeto de página de Flet, utilizado para actualizar la interfaz de usuario.
        """
        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge el grupo, subgrupo y Cuenta que deseas editarO"),
                ft.Text("2º Escribe el nuevo nombre de la Cuenta"),
                ft.Text(
                    "\t\tUtiliza un concepto corto y descriptivo"
                ),
                ft.Text(
                    "\t\tActualizar para modificar la Cuenta\n\t\tVolver para cancelar"
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column],
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200,  # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        # Se asume que 'globals.ventana_hasta_subgrupo' y 'ruta_BDapp' están definidos.
        dynamic_dropdown_selectors = globals.ventana_codigo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("editar CUENTA", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Nombre CUENTA", hint_text="Ej: ocio", width=500
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Actualizar Cuenta",
                            on_click=lambda e: Cuenta_accion_modificar(
                                e, container_to_update, page
                            ),
                            icon=ft.icons.UPDATE,  
                        ),
                        ft.ElevatedButton(
                            text="Volver",
                            on_click=lambda ev: reset_tabla_codigo_contenido(
                                ev, container_to_update, page
                            ),
                            icon=ft.icons.ARROW_BACK, 
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        )

        # Actualiza el contenido del contenedor y la página.
        container_to_update.content = new_content_column
        container_to_update.update()
        page.update()
 
    def btn_eliminar_cuenta(e, container_to_update, page):
        """
        Gestiona la acción que ocurre cuando se hace clic en el botón "Eliminar Cuenta".
        Elimina la CUENTA escogida
        """
        # Creamos el contenido de las INSTRUCCIONES
        instrucciones_content_column = ft.Column(
            controls=[
                ft.Text("1º Escoge el grupo al que pertenece la CUENTA"),
                ft.Text("2º Escoge el subgrupo al que pertenece la CUENTA"),
                ft.Text("3º Selecciona la CUENTA que deseas ELIMINAR"),
                ft.Text("RECUERDA: "),
                ft.Text(
                    "\t\tNo se puede eliminar un CUENTA con importe diferente a cero"
                ),
                ft.Text(
                    "\t\tUna vez eliminado la CUENTA, no se puede recuperar"
                ),
                ft.Text(
                    "\t\tEliminar para borrar la CUENTA\n\t\tVolver para cancelar"
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,  # Alinea todos los Text a la izquierda
        )
        # Creamos el ExpansionTile
        instrucciones_desplegable = ft.ExpansionTile(
            title=ft.Text(
                "Instrucciones",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            # Le pasamos el ft.Column que creamos para que el contenido esté alineado
            controls=[instrucciones_content_column],
        )
        # Envolvemos el ExpansionTile en un ft.Container para darle un color de fondo
        instrucciones_container = ft.Container(
            content=instrucciones_desplegable,
            bgcolor=ft.colors.BLUE_GREY_200,  # <-- Le aplicamos el color aquí
        )

        # Llama a 'ventana_codigo' para obtener el control Row de los desplegables.
        # Se asume que 'globals.ventana_codigo' y 'ruta_BDapp' están definidos.
        dynamic_dropdown_selectors = globals.ventana_codigo(ruta_BDapp)

        # Crea el nuevo control Column para agrupar todos los elementos del formulario.
        new_content_column = ft.Column(
            controls=[
                ft.Text("Eliminar CUENTA", size=20, weight=ft.FontWeight.BOLD),
                instrucciones_container,
                dynamic_dropdown_selectors,

                # Un "espacio flexible" que empujará los botones hacia abajo
                ft.Row(
                    height=10,  # La fila tendrá una altura de 10 píxeles
                ),
                ft.FilledButton(text="Eliminar CUENTA Permanentemente", on_click=lambda ev: Cuenta_accion_eliminar(ev, container_to_update, page),icon=ft.Icons.WARNING, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_ACCENT_700)),
                ft.FilledButton(text="Volver", on_click=lambda ev: reset_tabla_codigo_contenido(ev, container_to_update, page), icon=ft.Icons.ARROW_BACK),

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        )

        # Actualiza el contenido del contenedor y la página.
        container_to_update.content = new_content_column
        container_to_update.update()
        page.update()


    # --- Título de la Tabla Códigos --------------------------------------------
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

    # --- Subtítulo de la tabla Códigos (contiene los botones de acción) ---------
    # Inicialmente invisible. Su visibilidad se controla con el botón de configuración.
    # IMPORTANTE: Se define aquí para que toggle_subtitulo_visibility pueda referenciarlo.
    TablaCodigo_subtitulo = ft.Container(
        content=ft.Row(
            controls=[
                ft.FilledButton(
                    text="Crear Subgrupo",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: btn_crear_subcuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.GREEN_400,  # <-- Se agregó esta línea para el color
                        )
                ),
                ft.FilledButton(
                    text="Editar Subgrupo",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: btn_editar_subcuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.GREEN_400,  # <-- Se agregó esta línea para el color
                        )
                ),
                ft.FilledButton(
                    text="Eliminar Subgrupo",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e: btn_eliminar_subcuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.GREEN_400,  # <-- Se agregó esta línea para el color
                        )
                ),
                ft.FilledButton(
                    text="Crear Cuenta",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: btn_crear_cuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_500,  # <-- Se agregó esta línea para el color
                        )
                ),                
                 ft.FilledButton(
                    text="Editar Cuenta",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: btn_editar_cuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_500,  # <-- Se agregó esta línea para el color
                        )
                ),
                ft.FilledButton(
                    text="Eliminar Cuenta",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=lambda e: btn_eliminar_cuenta(e, TablaCodigo_contenido, e.page),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_500,  # <-- Se agregó esta línea para el color
                        )
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

    
    # ---------------------- Estructura principal de la vista -------------------------------------------------------
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



