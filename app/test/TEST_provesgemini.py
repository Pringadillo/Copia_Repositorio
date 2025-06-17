import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"



def mostrar_codigos_por_grupo(ruta_BDapp: str, grupo_id_seleccionado: int) -> list[ft.Control]:
    """
    Retrieves and formats account groups and subgroups from the database
    for a specific group_id, to be displayed in Flet.

    Args:
        ruta_BDapp (str): The path to the SQLite database file.
        grupo_id_seleccionado (int): The ID of the group to filter by.

    Returns:
        list[ft.Control]: A list of Flet Text controls representing the
                          formatted group and subgroup hierarchy.
    """
    formatted_controls = []
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # Get the main group description
        cursor.execute("SELECT descripcion_grupo FROM GRUPO WHERE grupo_id = ?", (grupo_id_seleccionado,))
        grupo_data = cursor.fetchone()

        if grupo_data:
            descripcion_grupo = grupo_data[0]
            # Format the main group
            formatted_controls.append(
                ft.Text(f"{str(grupo_id_seleccionado).zfill(2)} {descripcion_grupo}", size=16, weight=ft.FontWeight.BOLD)
            )

            # Get subgroups for the selected group
            cursor.execute("""
                SELECT subgrupo_id, descripcion_subgrupo
                FROM SUBGRUPO
                WHERE grupo_id = ?
                ORDER BY subgrupo_id
            """, (grupo_id_seleccionado,))
            subgrupos = cursor.fetchall()

            for subgrupo_id, descripcion_subgrupo in subgrupos:
                # Format the subgroups with indentation
                formatted_controls.append(
                    ft.Text(f"        {str(subgrupo_id).zfill(2)} {descripcion_subgrupo}", size=14)
                )
        else:
            formatted_controls.append(ft.Text(f"No se encontró el grupo con ID: {grupo_id_seleccionado}", color=ft.colors.RED_500))

    except sqlite3.Error as e:
        formatted_controls.append(ft.Text(f"Error de base de datos: {e}", color=ft.colors.RED_500))
    finally:
        if conn:
            conn.close()
    return formatted_controls



import flet as ft
import sqlite3

# --- (Pega aquí tus funciones crear_tabla_GRUPO, crear_tabla_SUBGRUPO, crear_tabla_CUENTAS) ---
# Para propósitos de demostración, definamos estas funciones localmente o asegúrate de que sean accesibles.

def crear_tabla_GRUPO(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GRUPO (
                    grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion_grupo TEXT NOT NULL UNIQUE CHECK (descripcion_grupo = UPPER(descripcion_grupo))
                )
            """)
            conn.commit()
        print("Tabla GRUPO (Nivel 1) creada (si no existía).")
    except sqlite3.Error as e:
        print(f"Error al conectar o crear la tabla GRUPO: {e}")
        raise

def crear_tabla_SUBGRUPO(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SUBGRUPO (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grupo_id INTEGER NOT NULL,
                    subgrupo_id INTEGER NOT NULL,
                    cod_2 TEXT NOT NULL UNIQUE,
                    desc_2 TEXT NOT NULL,
                    descripcion_grupo TEXT NOT NULL,
                    descripcion_subgrupo TEXT NOT NULL,
                    FOREIGN KEY (grupo_id) REFERENCES GRUPO (grupo_id),
                    UNIQUE (grupo_id, subgrupo_id)
                )
            """)
            conn.commit()
        print("Tabla SUBGRUPO (Nivel 2) creada (si no existía).")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla SUBGRUPO: {e}")
        raise

def crear_tabla_CUENTAS(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CUENTAS (
                grupo_id INTEGER NOT NULL,
                subgrupo_id INTEGER NOT NULL,
                cod_2 TEXT NOT NULL,
                desc_2 TEXT NOT NULL,
                nivel3_id INTEGER NOT NULL,
                descripcion_n3 TEXT NOT NULL,
                cod_3 TEXT NOT NULL UNIQUE,
                desc_3 TEXT NOT NULL,
                Saldo_inicial REAL NOT NULL DEFAULT 0,
                Fecha_Inicio TEXT NOT NULL DEFAULT CURRENT_DATE,
                PRIMARY KEY (grupo_id, subgrupo_id, nivel3_id),
                FOREIGN KEY (grupo_id, subgrupo_id) REFERENCES SUBGRUPO(grupo_id, subgrupo_id)
            )
        """)
        conn.commit()
        print(f"Tabla CUENTAS creada exitosamente en {ruta_BDapp} con los campos Saldo_inicial y Fecha_Inicio.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla CUENTAS: {e}")
        raise
    finally:
        if conn:
            conn.close()

# --- (Fin de las funciones de creación de tablas) ---

def main(page: ft.Page):
    page.title = "Contabilidad Doméstica"
    page.vertical_alignment = ft.MainAxisAlignment.START

    db_path = "contabilidad.db" # Tu archivo de base de datos

    # Inicializar tablas y poblar con datos de ejemplo para demostración
    crear_tabla_GRUPO(db_path)
    crear_tabla_SUBGRUPO(db_path)
    crear_tabla_CUENTAS(db_path) # Aunque CUENTAS no se usa directamente aquí para la visualización, es buena práctica crearla.

    # Insertar algunos datos de ejemplo si las tablas están vacías
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insertar datos GRUPO
        cursor.execute("INSERT OR IGNORE INTO GRUPO (grupo_id, descripcion_grupo) VALUES (?, ?)", (1, "EFECTIVO"))
        cursor.execute("INSERT OR IGNORE INTO GRUPO (grupo_id, descripcion_grupo) VALUES (?, ?)", (2, "CAIXA ENGINYERS"))
        cursor.execute("INSERT OR IGNORE INTO GRUPO (grupo_id, descripcion_grupo) VALUES (?, ?)", (3, "SELF BANK"))
        cursor.execute("INSERT OR IGNORE INTO GRUPO (grupo_id, descripcion_grupo) VALUES (?, ?)", (4, "DEGIRO"))

        # Insertar datos SUBGRUPO para GRUPO 1 (EFECTIVO)
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (1, 1, '01_CARLOS', 'Carlos', 'EFECTIVO', 'Carlos'))
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (1, 2, '02_MONTSE', 'Montse', 'EFECTIVO', 'Montse'))

        # Insertar datos SUBGRUPO para GRUPO 2 (CAIXA ENGINYERS)
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (2, 1, '01_CTA.CTE.', 'Cta.Cte.', 'CAIXA ENGINYERS', 'Cta.Cte.'))
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (2, 2, '02_DEPOSITOS', 'Depósitos', 'CAIXA ENGINYERS', 'Depósitos'))
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (2, 3, '03_FONDOS_INV.', 'Fondos Inv.', 'CAIXA ENGINYERS', 'Fondos Inv.'))

        # Insertar datos SUBGRUPO para GRUPO 3 (SELF BANK)
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (3, 1, '01_CTA.CTE._SB', 'Cta.Cte.', 'SELF BANK', 'Cta.Cte.'))

        # Insertar datos SUBGRUPO para GRUPO 4 (DEGIRO)
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (4, 1, '01_CTA.CTE._DG', 'Cta.Cte.', 'DEGIRO', 'Cta.Cte.'))
        cursor.execute("INSERT OR IGNORE INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo) VALUES (?, ?, ?, ?, ?, ?)", (4, 2, '02_RENTA_VAR.', 'Renta Variable', 'DEGIRO', 'Renta Variable'))

        conn.commit()
        print("Datos de ejemplo insertados (si no estaban ya presentes).")
    except sqlite3.Error as e:
        print(f"Error al insertar datos de ejemplo: {e}")
    finally:
        if conn:
            conn.close()

    # Ejemplo de uso: Mostrar cuentas para GRUPO con grupo_id = 2 (Caixa Enginyers)
    grupo_id_a_mostrar = 2
    controles_cuentas = mostrar_codigos_por_grupo(db_path, grupo_id_a_mostrar)

    # Una columna de Flet para contener la jerarquía de cuentas
    columna_cuentas = ft.Column(
        controls=controles_cuentas,
        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(
        ft.AppBar(title=ft.Text(f"Cuentas por Grupo: {grupo_id_a_mostrar}")),
        ft.Container(
            content=columna_cuentas,
            padding=20,
            alignment=ft.alignment.top_left,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)



