import flet as ft
import sqlite3
import os

# --- Configuración de la Base de Datos de Prueba ---
empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"

# Función para inicializar la base de datos de prueba si no existe
def inicializar_bd_prueba():
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DIARIO (
                id_diario INTEGER PRIMARY KEY AUTOINCREMENT,
                fechaValor TEXT NOT NULL,
                concepto TEXT,
                Debe REAL,
                Haber REAL
            )
        """)
        # Insertar algunos datos de prueba si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM DIARIO")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO DIARIO (fechaValor, concepto, Debe, Haber) VALUES (?, ?, ?, ?)",
                           ("2025-06-01", "Compra de mercancías", 100.00, 0.00))
            cursor.execute("INSERT INTO DIARIO (fechaValor, concepto, Debe, Haber) VALUES (?, ?, ?, ?)",
                           ("2025-06-01", "Venta de servicios", 0.00, 250.00))
            cursor.execute("INSERT INTO DIARIO (fechaValor, concepto, Debe, Haber) VALUES (?, ?, ?, ?)",
                           ("2025-06-02", "Pago de alquiler", 500.00, 0.00))
            cursor.execute("INSERT INTO DIARIO (fechaValor, concepto, Debe, Haber) VALUES (?, ?, ?, ?)",
                           ("2025-06-03", "Ingreso por intereses", 0.00, 15.75))
            cursor.execute("INSERT INTO DIARIO (fechaValor, concepto, Debe, Haber) VALUES (?, ?, ?, ?)",
                           ("2025-06-02", "Depósito bancario", 0.00, 1000.00)) # Fecha desordenada intencionadamente
        conn.commit()
        print(f"Base de datos de prueba '{ruta_BDapp}' inicializada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos de prueba: {e}")
    finally:
        if conn:
            conn.close()

# --- Tu función para obtener datos del diario ---
def obtener_asientos_diario(ruta_BDapp):
    """
    Obtiene todos los registros de la tabla DIARIO.
    devuelve una lista de diccionarios, donde cada diccionario representa una fila de la tabla DIARIO. 
    """
    datos = []
    try:
        conn = sqlite3.connect(ruta_BDapp)
        conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
        with conn:
            cursor = conn.cursor()
            # Ordenar por fechaValor de forma descendente y luego por id_diario descendente
            cursor.execute("SELECT * FROM DIARIO ORDER BY fechaValor DESC, id_diario DESC") 
            datos = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error al obtener datos de DIARIO: {e}")
        # Manejo de errores: por ejemplo, retornar una lista vacía o levantar una excepción
    return datos

# --- Tu función mostrar_Tabla_Diario (con la indentación corregida y algunas adaptaciones para el ejemplo) ---
# Hemos modificado esta función para que reciba 'page' y 'cuerpo_principal_diario' directamente,
# lo que es una forma más robusta de manejar la actualización en Flet.
# Ya no es un manejador de evento 'e', sino una función para actualizar un control específico.
def actualizar_contenido_diario(page: ft.Page, cuerpo_principal_diario: ft.Container):
    asientos = obtener_asientos_diario(ruta_BDapp)
    
    if not asientos:
        # Si no hay datos, se actualiza el contenido del contenedor principal
        cuerpo_principal_diario.content = ft.Container(
            content=ft.Text("No hay datos en el diario para mostrar.", text_align=ft.TextAlign.CENTER),
            alignment=ft.alignment.center,
            #padding=20,
            expand=True
        )
        page.update()
        return

    column_names = list(asientos[0].keys())

    columns = []
    for col_name in column_names:
        columns.append(
            ft.DataColumn(
                ft.Text(col_name, weight=ft.FontWeight.BOLD),
                # on_sort=lambda e: print(f"Ordenando por {e.column}"), # Desactivado para simplificar el ejemplo
            )
        )

    rows = []
    for asiento in asientos:
        cells = []
        for col_name in column_names:
            cells.append(ft.DataCell(ft.Text(str(asiento[col_name]))))
        rows.append(ft.DataRow(cells=cells))

    data_table = ft.DataTable(
        columns=columns,
        rows=rows,
        sort_column_index=0,  # Columna por defecto para ordenar (ej. la primera)
        sort_ascending=True,  # Orden ascendente por defecto
        heading_row_color=ft.Colors.BLUE_GREY_100,
        data_row_color={"hovered": ft.Colors.BLUE_GREY_50},
        border=ft.border.all(1, ft.Colors.GREY_300),
        column_spacing=20,
        horizontal_margin=10,
        divider_thickness=1,
    )

    # Creamos el contenedor que envolverá la tabla
    tabla_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Diario de Asientos", size=24, weight=ft.FontWeight.BOLD),
                data_table,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        #padding=20,
        alignment=ft.alignment.center,
        expand=True
    )
    
    # Actualizamos el contenido del contenedor principal del diario
    cuerpo_principal_diario.content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Libro Diario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                tabla_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True
        ),
        alignment=ft.alignment.center,
        #padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        expand=True
    )
    page.update() # Se llama a update en la página para que los cambios se reflejen

# --- Función principal de Flet ---
def main(page: ft.Page):
    page.title = "Ejemplo de Libro Diario con Flet y SQLite"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 1000
    page.window_height = 700

    # Inicializa la base de datos de prueba
    inicializar_bd_prueba()

    # Define el contenedor principal que contendrá el diario
    # Lo inicializamos con un texto de "Cargando..."
    cuerpo_principal_diario = ft.Container(
        content=ft.Column([ft.Text("Cargando Libro Diario...")], 
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                          alignment=ft.MainAxisAlignment.CENTER,
                          expand=True),
        expand=True,
        alignment=ft.alignment.center,
        #padding=20,
        bgcolor=ft.Colors.BLUE_GREY_50,
        border_radius=ft.border_radius.all(10)
    )

    # Un botón para recargar/mostrar el diario
    btn_recargar_diario = ft.ElevatedButton(
        "Recargar Libro Diario",
        #icon=ft.icons.REFRESH,
        on_click=lambda e: actualizar_contenido_diario(page, cuerpo_principal_diario)
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Mi Aplicación Contable", size=32, weight=ft.FontWeight.BOLD),
                        btn_recargar_diario,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=False,
                    spacing=20
                ),
                ft.Divider(height=20, thickness=2),
                cuerpo_principal_diario, # Aquí es donde se mostrará el contenido del diario
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            #padding=20
        )
    )

    # Llama a la función para cargar el diario al inicio de la aplicación
    actualizar_contenido_diario(page, cuerpo_principal_diario)
    page.update()

# Ejecuta la aplicación Flet
if __name__ == "__main__":
    ft.app(target=main)