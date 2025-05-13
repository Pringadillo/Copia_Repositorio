import flet as ft

import app.Menu.CodigosTabla as CodigosTabla


usuario = "KK_de_Vaca"  # Nombre del usuario


def crear_appbar(page):
    def boton_click(e):
        if e.control.text == "Tabla de Códigos":
            page.controls[0].controls[1].content = CodigosTabla.menu_TablaCodigos()
        elif e.control.text == "Diario":
            page.controls[0].controls[1].content = ft.Text("Contenido del DIARIO")
        elif e.control.text == "Informes":
            page.controls[0].controls[1].content = ft.Text("Contenido del INFORMES")
        elif e.control.text == "Inversiones":
            page.controls[0].controls[1].content = ft.Text("Contenido del INVERSIONES")
        elif e.control.text == "Configuración":
            page.controls[0].controls[1].content = ft.Text("Contenido de CONFIGURACION")
        elif e.control.text == "Salir":
            page.controls[0].controls[1].content = ft.Text("Contenido de SALIR")

        page.update()

    appbar = ft.AppBar(
        title=ft.Row(
            [
                # Botones Izquierda
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.icons.PERSON,  # Ícono de una persona
                                size=50,  # Tamaño del ícono
                                color=ft.colors.BLUE,  # Color del ícono
                            ),
                            ft.Text(
                                usuario,  # Nombre del usuario
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,  # Alinear contenido a la izquierda
                        spacing=5,  # Espaciado entre la imagen y el texto
                    ),
                    alignment=ft.alignment.top_left,  # Alinear el contenedor a la izquierda
                    padding=10,  # Espaciado interno del contenedor
                ),

                # Botones del Centro
                ft.Row(
                    [
                        ft.TextButton(
                            text="Diario",
                            icon=ft.icons.BOOK,  # Ícono para el botón "Diario"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                        ft.TextButton(
                            text="Informes",
                            icon=ft.icons.LIST,  # Ícono para el botón "Informes"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),                    
                        ft.TextButton(
                            text="Inversiones",
                            icon=ft.icons.ATTACH_MONEY,  # Ícono para el botón "Inversiones"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                                            ft.TextButton(
                            text="Tabla de Códigos",
                            icon=ft.icons.ACCOUNT_TREE,  # Ícono para el botón "Tabla Código"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar los primeros botones
                    expand=True,  # Ocupa el espacio disponible
                ),
                # Botones Derecha
                ft.TextButton(
                    text="Configuración",
                    icon=ft.icons.SETTINGS,  # Ícono para el botón "Configuración"
                    on_click=boton_click,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Salir",
                    icon=ft.icons.EXIT_TO_APP_OUTLINED,  # Ícono para el botón "Salir"
                    on_click=boton_click,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),                
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Espaciado entre los grupos
        )
    )
    return appbar


