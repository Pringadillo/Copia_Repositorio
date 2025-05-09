import sqlite3
import sys
import os

# Obtiene la ruta absoluta del directorio padre de 'app/Menu' (que es la raíz del proyecto)
ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ruta_raiz)

#from app import globals

#para comprobar si existen los modulos'
#ruta_bd = globals.ruta_BD  # Importamos la ruta de la base de datos desde globals.py
#print(ruta_bd)
print(ruta_raiz)
#print(globals.ruta_BD)

ruta_bd = os.path.join(ruta_raiz, "data", "bd_TEST_100.db")  # Ruta de la base de datos
#print(ruta_bd)

from datetime import datetime



def establecer_conexion(ruta_bd):
    """
    Establece una conexión a la base de datos SQLite.

    Args:
        ruta_bd (str): La ruta al archivo de la base de datos.

    Returns:
        sqlite3.Connection: Un objeto de conexión a la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_bd)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
def crear_conexion():
    """
    Crea una conexión a la base de datos SQLite especificada en la variable 'ruta_bd'.
    Si la base de datos no existe, se creará un nuevo archivo de base de datos.

    Retorna:
        sqlite3.Connection: Un objeto de conexión a la base de datos.
                        Retorna None si ocurre un error al conectar.
    """
    #ruta_bd = globals.ruta_BD  # Ruta de la base de datos desde globals.py
    conn = establecer_conexion(ruta_bd)
    return conn

def crear_tabla_grupo(conn):
    """
    Crea la tabla GRUPO (Nivel 1) si no existe.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GRUPO (
            grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion_grupo TEXT NOT NULL UNIQUE CHECK (descripcion_grupo = UPPER(descripcion_grupo))
        )
    """)
    conn.commit()
    print("Tabla GRUPO (Nivel 1) creada (si no existía).")

def crear_tabla_subgrupo(conn):
    """
    Crea la tabla SUBGRUPO (Nivel 2) si no existe.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
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

def crear_tabla_cuentas(conn):
    """
    Crea la tabla CUENTAS (Nivel 3) si no existe.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CUENTAS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER NOT NULL,
            subgrupo_id INTEGER NOT NULL,
            cod_2 TEXT NOT NULL,
            desc_2 TEXT NOT NULL,
            nivel3_id INTEGER NOT NULL,
            descripcion_n3 TEXT NOT NULL,
            cod_3 TEXT NOT NULL UNIQUE,
            desc_3 TEXT NOT NULL,
            FOREIGN KEY (grupo_id, subgrupo_id) REFERENCES SUBGRUPO (grupo_id, subgrupo_id),
            UNIQUE (grupo_id, subgrupo_id, nivel3_id)
        )
    """)
    conn.commit()
    print("Tabla CUENTAS (Nivel 3) creada (si no existía).")

def insertar_datos_grupo(conn, descripcion_grupo):
    """
    Inserta datos en la tabla GRUPO (Nivel 1).

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
        descripcion_grupo (str): Descripción del grupo.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO GRUPO (descripcion_grupo) VALUES (?)
        """, (descripcion_grupo,))
        conn.commit()
        print(f"Insertado en GRUPO (Nivel 1): descripcion_grupo='{descripcion_grupo}'")
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en GRUPO (Nivel 1): {e}")

def insertar_datos_subgrupo(conn, grupo_id, descripcion_subgrupo):
    """
    Inserta datos en la tabla SUBGRUPO (Nivel 2).

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
        grupo_id (int): ID del grupo al que pertenece.
        descripcion_subgrupo (str): Descripción del subgrupo.
    """
    cursor = conn.cursor()
    # Obtener el máximo subgrupo_id para el grupo_id dado
    cursor.execute("""
        SELECT COALESCE(MAX(subgrupo_id), 0) + 1
        FROM SUBGRUPO
        WHERE grupo_id = ?
    """, (grupo_id,))
    subgrupo_id = cursor.fetchone()[0]
    cursor.execute("""
        SELECT descripcion_grupo
        FROM GRUPO
        WHERE grupo_id = ?
    """, (grupo_id,))
    descripcion_grupo = cursor.fetchone()[0]
    cod_2 = f"{grupo_id}.{subgrupo_id:02d}"
    desc_2 = f"{descripcion_grupo} - {descripcion_subgrupo}"
    try:
        cursor.execute("""
            INSERT INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo))
        conn.commit()
        print(f"Insertado en SUBGRUPO (Nivel 2): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2='{desc_2}', descripcion_grupo='{descripcion_grupo}', descripcion_subgrupo='{descripcion_subgrupo}'")
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en SUBGRUPO (Nivel 2): {e}")

def insertar_datos_cuenta(conn, grupo_id, subgrupo_id, descripcion_n3):
    """
    Inserta datos en la tabla CUENTAS (Nivel 3).

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
        grupo_id (int): ID del grupo al que pertenece.
        subgrupo_id (int): ID del subgrupo al que pertenece.
        descripcion_n3 (str): Descripción de la cuenta.
    """
    cursor = conn.cursor()
    # Obtener el máximo nivel3_id para el grupo_id y subgrupo_id dados
    cursor.execute("""
        SELECT COALESCE(MAX(nivel3_id), 0) + 1
        FROM CUENTAS
        WHERE grupo_id = ? AND subgrupo_id = ?
    """, (grupo_id, subgrupo_id))
    nivel3_id = cursor.fetchone()[0]
    # Obtener cod_2 y desc_2 de la tabla SUBGRUPO
    cursor.execute("""
        SELECT cod_2, desc_2
        FROM SUBGRUPO
        WHERE grupo_id = ? AND subgrupo_id = ?
    """, (grupo_id, subgrupo_id))
    resultado = cursor.fetchone()
    if resultado is not None:
        cod_2 = resultado[0]
        desc_2 = resultado[1]
        cod_3 = f"{cod_2}.{nivel3_id:02d}"
        desc_3 = f"{desc_2} - {descripcion_n3}"
        try:
            cursor.execute("""
                INSERT INTO CUENTAS (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3))
            conn.commit()
            print(f"Insertado en CUENTAS (Nivel 3): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2={desc_2}, nivel3_id={nivel3_id}, descripcion_n3='{descripcion_n3}', cod_3={cod_3}, desc_3='{desc_3}'")
        except sqlite3.IntegrityError as e:
            print(f"Error al insertar en CUENTAS (Nivel 3): {e}")
    else:
        print(f"No se encontró subgrupo con grupo_id={grupo_id} y subgrupo_id={subgrupo_id}")

def mostrar_datos_grupo(conn):
    """
    Muestra todos los datos de la tabla GRUPO.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GRUPO")
    registros = cursor.fetchall()
    print("\nContenido de la tabla GRUPO (Nivel 1):")
    for registro in registros:
        print(registro)

def mostrar_datos_subgrupo(conn):
    """
    Muestra todos los datos de la tabla SUBGRUPO.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT cod_2, desc_2 FROM SUBGRUPO")
    registros = cursor.fetchall()
    print("\nContenido de la tabla SUBGRUPO (Nivel 2):")
    for registro in registros:
        print(registro)

def mostrar_datos_cuentas(conn):
    """
    Muestra todos los datos de la tabla CUENTAS.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT cod_3, desc_3 FROM CUENTAS")
    registros = cursor.fetchall()
    print("\nContenido de la tabla CUENTAS (Nivel 3):")
    for registro in registros:
        print(registro)

def mostrar_subgrupos_y_cuentas_por_grupo(conn, grupo_id):
    """
    Muestra los subgrupos y cuentas asociadas a un grupo específico.

    Args:
        conn (sqlite3.Connection): Objeto de conexión a la base de datos.
        grupo_id (int): ID del grupo para el cual se desean mostrar los subgrupos y cuentas.
    """
    cursor = conn.cursor()

    # Obtener los subgrupos del grupo solicitado
    cursor.execute("""
        SELECT subgrupo_id, descripcion_subgrupo
        FROM SUBGRUPO
        WHERE grupo_id = ?
    """, (grupo_id,))
    subgrupos = cursor.fetchall()

    if not subgrupos:
        print(f"No se encontraron subgrupos para el grupo con ID {grupo_id}.")
        return

    print(f"\nSubgrupos y cuentas del grupo con ID {grupo_id}:\n")

    # Iterar sobre los subgrupos y obtener las cuentas asociadas
    for subgrupo_id, descripcion_subgrupo in subgrupos:
        print(f"{subgrupo_id} - {descripcion_subgrupo}")

        # Obtener las cuentas asociadas al subgrupo
        cursor.execute("""
            SELECT cod_3, desc_3
            FROM CUENTAS
            WHERE grupo_id = ? AND subgrupo_id = ?
        """, (grupo_id, subgrupo_id))
        cuentas = cursor.fetchall()

        if cuentas:
            for cod_3, desc_3 in cuentas:
                print(f"    {cod_3} -  {desc_3}")
        else:
            print("    No hay cuentas asociadas a este subgrupo.")

def Crear_Tablas(ruta_bd):
    """
    Crea todas las tablas necesarias en la base de datos.

    Args:
        ruta_bd (str): La ruta al archivo de la base de datos.
    """
    conn = establecer_conexion(ruta_bd)
    if conn:
        crear_tabla_grupo(conn)
        crear_tabla_subgrupo(conn)
        crear_tabla_cuentas(conn)
        conn.close()

def Insertar_Datos_Iniciales(ruta_bd):
    """
    Inserta los datos iniciales en las tablas de la base de datos.

    Args:
        ruta_bd (str): La ruta al archivo de la base de datos.
    """
    conn = crear_conexion()
    if conn:
        # Insertar los datos iniciales en GRUPO (Nivel 1)
        insertar_datos_grupo(conn, "PRODCTOS FINANCIEROS")
        insertar_datos_grupo(conn, "DEUDAS")
        insertar_datos_grupo(conn, "GASTOS")
        insertar_datos_grupo(conn, "INGRESOS")

        # Insertar datos en SUBGRUPO (Nivel 2)
        insertar_datos_subgrupo(conn, 1, "Caixa Enginyers")
        insertar_datos_subgrupo(conn, 1, "Self Banc")
        insertar_datos_subgrupo(conn, 1, "DeGiro")
        insertar_datos_subgrupo(conn, 1, "Santander")
        insertar_datos_subgrupo(conn, 1, "Stockcrowd")
        insertar_datos_subgrupo(conn, 1, "Civislend")
        insertar_datos_subgrupo(conn, 1, "T.R.Publicidad")
        insertar_datos_subgrupo(conn, 1, "Bestinver")
        insertar_datos_subgrupo(conn, 1, "Bufete Perez Pozo")
        insertar_datos_subgrupo(conn, 1, "Kontactalia")
        insertar_datos_subgrupo(conn, 1, "Inversiones en empresas")
        insertar_datos_subgrupo(conn, 1, "Carmon Inversores")
        insertar_datos_subgrupo(conn, 1, "Trade Republic")
        insertar_datos_subgrupo(conn, 1, "B Sabadell")
        insertar_datos_subgrupo(conn, 1, "BBVA")
        insertar_datos_subgrupo(conn, 1, "Minto")
        insertar_datos_subgrupo(conn, 2, "Deudas Familiares")
        insertar_datos_subgrupo(conn, 2, "Deudas Casa")
        insertar_datos_subgrupo(conn, 2, "Otras Deudas")
        insertar_datos_subgrupo(conn, 3, "Gastos Fijos")
        insertar_datos_subgrupo(conn, 3, "Gastos Variables")
        insertar_datos_subgrupo(conn, 3, "Gastos Extraordinarios")
        insertar_datos_subgrupo(conn, 4, "Salarios")
        insertar_datos_subgrupo(conn, 4, "Inversiones")
        insertar_datos_subgrupo(conn, 4, "Otros Ingresos")

        # Insertar datos en CUENTAS (Nivel 3)
        insertar_datos_cuenta(conn, 1, 1, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 1, "Depósitos")
        insertar_datos_cuenta(conn, 1, 1, "Fondos Inv.")
        insertar_datos_cuenta(conn, 1, 1, "Cta.Cte. $")
        insertar_datos_cuenta(conn, 1, 1, "Depósitos $")
        insertar_datos_cuenta(conn, 1, 2, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 2, "Cta. Remunerada")
        insertar_datos_cuenta(conn, 1, 2, "Depósitos")
        insertar_datos_cuenta(conn, 1, 2, "Fondos Inv.")
        insertar_datos_cuenta(conn, 1, 2, "F.Inv. Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 4, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 4, "Renta Variable")
        insertar_datos_cuenta(conn, 1, 4, "Derivados Financieros")
        insertar_datos_cuenta(conn, 1, 3, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 3, "Renta Variable")
        insertar_datos_cuenta(conn, 1, 3, "ETF")
        insertar_datos_cuenta(conn, 1, 5, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 5, "Crowfunding")
        insertar_datos_cuenta(conn, 1, 6, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 6, "Crowfunding")
        insertar_datos_cuenta(conn, 1, 7, "Crowfunding")
        insertar_datos_cuenta(conn, 1, 8, "Plan Pensiones")
        insertar_datos_cuenta(conn, 1, 8, "Fondos Inv.")
        insertar_datos_cuenta(conn, 1, 9, "Crowfunding")
        insertar_datos_cuenta(conn, 1, 10, "CapitalCell")
        insertar_datos_cuenta(conn, 1, 10, "Cebiotec")
        insertar_datos_cuenta(conn, 1, 11, "Crowfunding")
        insertar_datos_cuenta(conn, 1, 12, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 12, "Depósitos")
        insertar_datos_cuenta(conn, 1, 13, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 13, "Depósitos")
        insertar_datos_cuenta(conn, 1, 14, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 14, "Depósitos")
        insertar_datos_cuenta(conn, 1, 15, "Cta.Cte.")
        insertar_datos_cuenta(conn, 1, 15, "Depósitos")
        insertar_datos_cuenta(conn, 1, 16, "Crowfunding")
        insertar_datos_cuenta(conn, 2, 1, "Roger")
        insertar_datos_cuenta(conn, 2, 1, "Enric")
        insertar_datos_cuenta(conn, 2, 2, "Enaire 0%")
        insertar_datos_cuenta(conn, 2, 3, "Inversiones JMG")
        insertar_datos_cuenta(conn, 2, 3, "Avis")
        insertar_datos_cuenta(conn, 2, 3, "Tata")
        insertar_datos_cuenta(conn, 2, 3, "Albert")
        insertar_datos_cuenta(conn, 2, 3, "Joan Moises")
        insertar_datos_cuenta(conn, 3, 1, "Comida")
        insertar_datos_cuenta(conn, 3, 1, "Agua")
        insertar_datos_cuenta(conn, 3, 1, "Luz")
        insertar_datos_cuenta(conn, 3, 1, "Gas")
        insertar_datos_cuenta(conn, 3, 1, "Teléfono/Internet")
        insertar_datos_cuenta(conn, 3, 1, "Limpieza")
        insertar_datos_cuenta(conn, 3, 1, "Comunidad Vecinos")
        insertar_datos_cuenta(conn, 3, 1, "Otros Gastos Fijos")
        insertar_datos_cuenta(conn, 3, 2, "Ropa")
        insertar_datos_cuenta(conn, 3, 2, "Salud")
        insertar_datos_cuenta(conn, 3, 2, "Transporte")
        insertar_datos_cuenta(conn, 3, 2, "Seguros")
        insertar_datos_cuenta(conn, 3, 2, "Impuestos")
        insertar_datos_cuenta(conn, 3, 2, "Vacaciones")
        insertar_datos_cuenta(conn, 3, 2, "Otros Gastos Variables")
        insertar_datos_cuenta(conn, 3, 3, "Gastos Extraordinarios")
        insertar_datos_cuenta(conn, 3, 3, "Otros Gastos Extraordinarios")
        insertar_datos_cuenta(conn, 3, 3, "Cuadrar Saldos")
        insertar_datos_cuenta(conn, 4, 1, "Montse")
        insertar_datos_cuenta(conn, 4, 1, "Carlos")
        insertar_datos_cuenta(conn, 4, 1, "Pensión")
        insertar_datos_cuenta(conn, 4, 2, "Bancarios")
        insertar_datos_cuenta(conn, 4, 2, "Renta Fija")
        insertar_datos_cuenta(conn, 4, 2, "Renta Variable")
        insertar_datos_cuenta(conn, 4, 2, "Fondos Inv.")
        insertar_datos_cuenta(conn, 4, 2, "Crowfunding")
        insertar_datos_cuenta(conn, 4, 3, "Otros Ingresos")

        conn.close()

Insertar_Datos_Iniciales(ruta_bd)

