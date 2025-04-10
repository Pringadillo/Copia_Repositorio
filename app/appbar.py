import flet as ft



usuario = "Nombre Usuario"  # Nombre del usuario
contenido_cuerpo = ""

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
        elif e.control.text == "SumasySaldos":
            page.controls[0].controls[1].content = ft.Text("Contenido de Saldos")
        elif e.control.text == "Configuración":
            page.controls[0].controls[1].content = ft.Text("Contenido de Configuración")

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

# -----------------------  FUNCIONES MENU  -----------------------
def TablaCodigos():
    # Submenu CRUD de la tabla código
    submenu = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Ver Tabla Códigos",
                    icon=ft.icons.TABLE_CHART,  # Ícono para "Ver Tabla"
                    on_click=ver_TablaCodigos,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Crear Código",
                    icon=ft.icons.ADD,  # Ícono para "Crear"
                    on_click=crear_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),

                ft.TextButton(
                    text="Actualizar Código",
                    icon=ft.icons.EDIT,  # Ícono para "Actualizar"
                    on_click=actualizar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
                ft.TextButton(
                    text="Eliminar Código",
                    icon=ft.icons.DELETE,  # Ícono para "Eliminar"
                    on_click=eliminar_codigo,  # Pasa directamente la función
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=18, letter_spacing=2)
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,  # Centrar los botones horizontalmente
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
def SumasySaldos():
    pass
def Inversiones():  
    pass
def Configuracion():
    pass
def Salir():
    pass


# -----------------------  SUBMENU TABLA CODIGOS -----------------------
def ver_TablaCodigos(e):
    print("Ver Tabla Códigos")

    contenido_cuerpo = ft.Container(
        # poner la tabla Códigos aquí------------------------------------
        content=ft.Column(
            controls=[
                ft.Text("Contenido de Tabla Códigos", size=20),

            ],
            expand=True,
        ),
        #expand=3,  # Asegura que el contenido ocupe más espacio que el submenú
    )



def crear_codigo(e):
    print("Crear Código")

def leer_codigo(e):
    print("Ver Tabla")    

def actualizar_codigo(e):
    print("Modificar Código")

def eliminar_codigo(e):  
    print("Eliminar Código")

# -----------------------  SUBMENU DIARIO -----------------------



# -----------------------  SUBMENU MAYOR -----------------------



# -----------------------  SUBMENU PerdidasGanancias -----------------------


# -----------------------  SUBMENU Balance -----------------------



# -----------------------  SUBMENU SumasSaldos -----------------------




# -----------------------  SUBMENU Inversiones -----------------------



# -----------------------  SUBMENU Salir -----------------------




