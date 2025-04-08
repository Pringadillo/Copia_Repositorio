import flet as ft

def crear_appbar(page):
    def boton_click(e):
        if e.control.text == "Diario":
            page.controls[0].controls[1].content = ft.Text("Contenido del Diario")
        elif e.control.text == "Mayor":
            page.controls[0].controls[1].content = ft.Text("Contenido del Mayor")
        elif e.control.text == "Balance":
            page.controls[0].controls[1].content = ft.Text("Contenido del Balance")
        elif e.control.text == "Saldos":
            page.controls[0].controls[1].content = ft.Text("Contenido de Saldos")
        elif e.control.text == "Configuración":
            page.controls[0].controls[1].content = ft.Text("Contenido de Configuración")

        page.update()

    appbar = ft.AppBar(
        title=ft.Row(
            [
                # Primeros botones centrados
                ft.Row(
                    [
                        ft.TextButton(
                            text="Tabla Códigos",
                            icon=ft.icons.ACCOUNT_TREE,  # Ícono para el botón "Tabla Código"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                        ft.TextButton(
                            text="Diario",
                            icon=ft.icons.BOOK,  # Ícono para el botón "Diario"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                        ft.TextButton(
                            text="Mayor",
                            icon=ft.icons.LIST,  # Ícono para el botón "Mayor"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),
                        ft.TextButton(
                            text="Perdidas y Ganancias",
                            icon=ft.icons.PIE_CHART,  # Ícono para el botón "Perdidas y Ganancias"
                            #icon=ft.icons.BALANCE,  # Ícono para el botón "Perdidas y Ganancias"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),                        
                        ft.TextButton(
                            text="Balance",
                            icon=ft.icons.BALANCE,  # Ícono para el botón "Balance"
                            on_click=boton_click,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18, letter_spacing=2)
                            ),
                        ),

                        ft.TextButton(
                            text="sumas y Saldos",
                            icon=ft.icons.BAR_CHART,  # Ícono para el botón "Sunas y Saldos"
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
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar los primeros botones
                    expand=True,  # Ocupa el espacio disponible
                ),
                # Último botón a la derecha
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