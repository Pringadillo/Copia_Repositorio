import flet as ft

def main(page: ft.Page):
    page.title = "Mi primera imagen con Flet"
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Ruta de la imagen (asegúrate de que la imagen esté en la misma carpeta)
    # Si tu imagen está en una subcarpeta, por ejemplo 'assets', usa 'assets/mi_imagen.png'
    image_path = "foto1.jpeg" 

    page.add(
        ft.Column(
            [
                ft.Text("¡Aquí tienes tu imagen!", size=20, weight=ft.FontWeight.BOLD),
                ft.Image(
                    src=image_path,
                    width=300,  # Ancho deseado de la imagen
                    height=300, # Alto deseado de la imagen
                    fit=ft.ImageFit.CONTAIN, # Ajusta la imagen dentro de los límites
                    border_radius=ft.border_radius.all(10), # Opcional: bordes redondeados
                ),
                ft.Text("¡Flet es genial!", size=16),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20, # Espacio entre los elementos de la columna
        )
    )

# Ejecuta la aplicación
if __name__ == "__main__":
    ft.app(target=main) # Para una aplicación web o de escritorio
    # Si quieres una aplicación web que se abra en el navegador y no en una ventana de escritorio:
    # ft.app(target=main, view=ft.WEB_BROWSER)