import flet as ft

def crear_cuerpo():
    columna_lateral = ft.Column(
        # saldos bancarios
        controls=[
            ft.Text("Cuentas Bancarias", size=20),
            ft.Text("Cuenta 1: $100010"),
            ft.Text("Cuenta 2: $250010"),
            ft.Text("Cuenta 3: $50010"),
            # Agrega más cuentas según sea necesario
        ],

        # Resumen de productos financieros

        width=200,
    )

    contenido_central = ft.Container(bgcolor=ft.colors.BLUE_GREY_100, expand=True)

    cuerpo = ft.Row(
        controls=[
            columna_lateral,
            contenido_central,
        ],
        expand=True,
    )

    return cuerpo