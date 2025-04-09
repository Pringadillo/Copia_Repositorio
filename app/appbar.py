import flet as ft

def crear_appbar(page):
    def boton_click(e):
        if e.control.text == "Tabla Códigos":
            page.controls[0].controls[1].content = TablaCodigos()
        elif e.control.text == "Diario":
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
                            text="Sumas y Saldos",
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

def TablaCodigos():
    # Submenu CRUD de la tabla código
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Crear",
                    icon=ft.icons.ADD,  # Ícono para "Crear"
                    on_click=crear_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Leer",
                    icon=ft.icons.RECEIPT,  # Ícono para "Leer"
                    on_click=leer_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Actualizar",
                    icon=ft.icons.EDIT,  # Ícono para "Actualizar"
                    on_click=actualizar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Eliminar",
                    icon=ft.icons.DELETE,  # Ícono para "Eliminar"
                    on_click=eliminar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar los botones horizontalmente
            spacing=20,  # Espaciado entre los botones
        ),
        bgcolor=ft.colors.LIGHT_BLUE_50,  # Fondo suave para el submenú
        padding=10,  # Espaciado interno del contenedor
        border_radius=ft.border_radius.all(10),  # Bordes redondeados
            )
    
    # Contenido de la tabla de códigos
    contenido_cuerpo = ft.Container(
        # poner la tabla Códigos aquí------------------------------------
        content=ft.Column(
            controls=[
                ft.Text("Contenido de Tabla Códigos", size=20),
                ft.Text("Código 1: Descripción 1"),
                ft.Text("Código 2: Descripción 2"),
                ft.Text("Código 3: Descripción 3"),
                # Agrega más códigos según sea necesario
            ],
            expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )

    # Fila que contiene el submenú y el coColumnnido
    cuerpo = ft.Column(
        controls=[
            submenu,  # Submenú a la izquierda
            contenido_cuerpo,  # Contenido a la derecha
        ],
        expand=True,
    )

    return cuerpo

def Diario():
    pass
def Mayor():
    pass        
def PerdidasGanancias():
    pass
def Balance():
    pass
def SumasSaldos():
    pass
def Inversiones():  
    pass
def Configuracion():
    pass
def Salir():
    pass
def guardar():
    pass


def crear_codigo():
    print ("Crear Código")
def leer_codigo():
    pass    
def actualizar_codigo():
    pass
def eliminar_codigo():  
    pass

