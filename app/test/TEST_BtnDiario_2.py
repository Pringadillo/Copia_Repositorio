import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"






import flet as ft

def main(page: ft.Page):
    page.title = "Contabilidad Doméstica"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False

    # List to store transactions
    transactions = []

    def add_transaction(e):
        if description_input.value and amount_input.value:
            try:
                amount = float(amount_input.value)
                transaction_type = type_dropdown.value
                
                # Determine sign of amount based on type
                if transaction_type == "Gasto":
                    amount = -abs(amount)
                else: # Ingreso
                    amount = abs(amount)

                transactions.append({"description": description_input.value, 
                                     "amount": amount, 
                                     "type": transaction_type})
                
                # Clear input fields
                description_input.value = ""
                amount_input.value = ""
                
                update_transactions_display()
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Por favor, introduce un monto numérico válido.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700
                )
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, rellena todos los campos.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700
            )
            page.snack_bar.open = True
            page.update()

    def update_transactions_display():
        transactions_list.controls.clear()
        total_balance = 0.0
        for i, transaction in enumerate(transactions):
            amount_color = ft.Colors.GREEN_600 if transaction["type"] == "Ingreso" else ft.Colors.RED_600
            total_balance += transaction["amount"]

            transactions_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(transaction["description"], size=16),
                                ft.Text(f"{transaction['amount']:.2f} €", size=16, weight=ft.FontWeight.BOLD, color=amount_color),
                            ]
                        )
                    )
                )
            )
        balance_text.value = f"Saldo Total: {total_balance:.2f} €"
        balance_text.color = ft.Colors.GREEN_700 if total_balance >= 0 else ft.Colors.RED_700


    # Input fields
    description_input = ft.TextField(
        label="Descripción", 
        hint_text="Ej: Compra supermercado",
        expand=True
    )
    amount_input = ft.TextField(
        label="Monto", 
        hint_text="Ej: 50.75", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=150
    )
    type_dropdown = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("Ingreso"),
            ft.dropdown.Option("Gasto"),
        ],
        value="Gasto", # Default value
        width=150
    )

    add_button = ft.ElevatedButton(
        text="Añadir Transacción",
        icon=ft.Icons.ADD,
        on_click=add_transaction,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
        )
    )
    
    # Display area for transactions
    transactions_list = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        controls=[],
    )

    balance_text = ft.Text("Saldo Total: 0.00 €", size=20, weight=ft.FontWeight.BOLD)

    page.add(
        ft.AppBar(
            title=ft.Text("Contabilidad Doméstica", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.BLUE_700,
            center_title=True
        ),
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Nueva Transacción", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    ft.Row(
                        controls=[
                            description_input,
                            amount_input,
                        ]
                    ),
                    type_dropdown,
                    ft.Container(height=10), # Spacer
                    add_button,
                    ft.Divider(height=30, color=ft.Colors.GREY_400),
                    ft.Text("Movimientos", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    transactions_list,
                    ft.Divider(height=30, color=ft.Colors.GREY_400),
                    balance_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=ft.padding.all(20),
            width=page.window_width,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)


''' 
Este código es un ejemplo de cómo crear un formulario básico en Flet para probar un botón relacionado con el Diario. 
continuando con mi programa de cuentas de casa, quiero empezar a trabajar sobre el Diario. Como siempre lo haré con python y la libreria flet, sqlite3

Creo que voy a empezar a pedirte ha realizar una labla en sqlite3 del diario, ha de contener los siguientes campos, con las siguientes condiciones:

id: unico, no nulo, primary key

fecha: no nulo dd/mm/aa

Grupo: no nulo, ha de coincidir con descripcion_grupo de la tabla GRUPO

subgrupo: no nulo, ha de coincidir con descripcion_subgrupo de la tabla SUBGRUPO

Cuenta: no nulo, ha de coincidir con descripcion_n3 de la tabla CUENTAS

importe: no nulo, con 2 decimales y el guion de negativo si es necesario

PyG: 
'''