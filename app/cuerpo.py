import flet as ft

def crear_cuerpo():
    columna_cuentas = ft.Column(
        # saldos bancarios
        controls=[
            ft.Text("Cuentas Bancarias", size=20),
            ft.Text("Cuenta 1: $1000"),
            ft.Text("Cuenta 2: $2500"),
            ft.Text("Cuenta 3: $500"),
            # Agrega más cuentas según sea necesario
        ],

        # Resumen de productos financieros

        width=200,
    )

    contenido_central = ft.Container(bgcolor=ft.colors.BLUE_GREY_100, expand=True)

    cuerpo = ft.Row(
        controls=[
            columna_cuentas,
            contenido_central,
        ],
        expand=True,
    )

    return cuerpo