import sqlite3
import flet as ft

from datetime import datetime


empresa = "Ejemplo_1"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"app/data/{BasedeDatos}"

def crear_base_datos():
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()
    conn.commit()
    conn.close()


def crear_tabla_GRUPO(ruta_BD):
    """
    Establece una conexión a la base de datos SQLite y crea la tabla GRUPO si no existe.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:  # Usamos 'with' para asegurar el cierre automático de la conexión
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
        raise  # Re-lanza la excepción para que el llamador pueda manejarla

def crear_tabla_SUBGRUPO(ruta_BD):
    """
    Crea la tabla SUBGRUPO (Nivel 2) si no existe.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
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
        raise  # Re-lanza la excepción para que el llamador la maneje

def crear_tabla_CUENTAS(ruta_BD):
    """
    Crea la tabla CUENTAS (Nivel 3) si no existe.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
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
    except sqlite3.Error as e:
        print(f"Error al crear la tabla CUENTAS: {e}")
        raise  # Re-lanza la excepción para que el llamador la maneje


#crear_base_datos()
#crear_tabla_GRUPO(ruta_BD)
#crear_tabla_SUBGRUPO(ruta_BD)
#crear_tabla_CUENTAS(ruta_BD)


# --------------------------------- INSERTAR DATOS ---------------------------------

def insertar_datos_grupo(ruta_BD, descripcion_grupo):
    """
    Inserta datos en la tabla GRUPO (Nivel 1).

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
        descripcion_grupo (str): Descripción del grupo.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO GRUPO (descripcion_grupo) VALUES (?)
            """, (descripcion_grupo.upper(),))  # <-- Aquí convertimos a mayúsculas
            conn.commit()
        print(f"Insertado en GRUPO (Nivel 1): descripcion_grupo='{descripcion_grupo.upper()}'")
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en GRUPO (Nivel 1): {e}")
        raise  # Re-lanza la excepción para que el llamador la maneje

def insertar_datos_subgrupo(ruta_BD, grupo_id, descripcion_subgrupo):
    """
    Inserta datos en la tabla SUBGRUPO (Nivel 2).

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
        grupo_id (int): ID del grupo al que pertenece.
        descripcion_subgrupo (str): Descripción del subgrupo.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
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
            cursor.execute("""
                INSERT INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo))
            conn.commit()
        print(f"Insertado en SUBGRUPO (Nivel 2): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2='{desc_2}', descripcion_grupo='{descripcion_grupo}', descripcion_subgrupo='{descripcion_subgrupo}'")
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en SUBGRUPO (Nivel 2): {e}")
        raise  # Re-lanza la excepción para que el llamador la maneje

def insertar_datos_cuenta(ruta_BD, grupo_id, subgrupo_id, descripcion_n3):
    """
    Inserta datos en la tabla CUENTAS (Nivel 3).

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
        grupo_id (int): ID del grupo al que pertenece.
        subgrupo_id (int): ID del subgrupo al que pertenece.
        descripcion_n3 (str): Descripción de la cuenta.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
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
                cursor.execute("""
                    INSERT INTO CUENTAS (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3))
                conn.commit()
                print(f"Insertado en CUENTAS (Nivel 3): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2={desc_2}, nivel3_id={nivel3_id}, descripcion_n3='{descripcion_n3}', cod_3={cod_3}, desc_3='{desc_3}'")
            else:
                print(f"No se encontró subgrupo con grupo_id={grupo_id} y subgrupo_id={subgrupo_id}")
                # Es importante decidir cómo manejar este caso.  Aquí, simplemente se imprime un mensaje.
                # Otra opción sería lanzar una excepción:
                # raise ValueError(f"No se encontró subgrupo con grupo_id={grupo_id} y subgrupo_id={subgrupo_id}")
    except sqlite3.Error as e:
        print(f"Error al insertar en CUENTAS (Nivel 3): {e}")
        raise





# ---------------------------------- MOSTRAR DATOS ----------------------------------

def mostrar_datos_grupo(ruta_BD):
    """
    Muestra todos los datos de la tabla GRUPO.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GRUPO")
            registros = cursor.fetchall()
        print("\nContenido de la tabla GRUPO (Nivel 1):")
        for registro in registros:
            print(registro)
    except sqlite3.Error as e:
        print(f"Error al mostrar datos de GRUPO: {e}")
        raise

def mostrar_datos_subgrupo(ruta_BD):
    """
    Muestra todos los datos de la tabla SUBGRUPO.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_2, desc_2 FROM SUBGRUPO")
            registros = cursor.fetchall()
        print("\nContenido de la tabla SUBGRUPO (Nivel 2):")
        for registro in registros:
            print(registro)
    except sqlite3.Error as e:
        print(f"Error al mostrar datos de SUBGRUPO: {e}")
        raise

def mostrar_datos_cuentas(ruta_BD):
    """
    Muestra todos los datos de la tabla CUENTAS.

    Args:
        ruta_BD (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BD)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_3, desc_3 FROM CUENTAS")
            registros = cursor.fetchall()
        print("\nContenido de la tabla CUENTAS (Nivel 3):")
        for registro in registros:
            print(registro)
    except sqlite3.Error as e:
        print(f"Error al mostrar datos de CUENTAS: {e}")
        raise


#mostrar_datos_grupo(ruta_BD)
#mostrar_datos_subgrupo(ruta_BD)
#mostrar_datos_cuentas(ruta_BD)
# ---------------------------------- ACTUALIZAR DATOS ----------------------------------


# ---------------------------------- ELIMINAR DATOS ----------------------------------



# ---------------------------------- ejemplo DATOS ----------------------------------

#crear_base_datos()
#crear_tabla_GRUPO(ruta_BD)
#crear_tabla_SUBGRUPO(ruta_BD)
#crear_tabla_CUENTAS(ruta_BD)

#mostrar_datos_grupo(ruta_BD)
#mostrar_datos_subgrupo(ruta_BD)
#mostrar_datos_cuentas(ruta_BD)


def ver_tablas_base_datos():
    """Consulta y muestra todas las tablas existentes en la base de datos."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener los nombres de todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()

    print("Tablas en la base de datos:")
    if tablas:
        for tabla in tablas:
            print(f"- {tabla[0]}")
    else:
        print("No hay tablas en la base de datos.")

    conn.close()

#ver_tablas_base_datos()


'''
   # Insertar datos en CUENTAS (Nivel 1)
insertar_datos_grupo(ruta_BD, "Cuentas Financieras")
insertar_datos_grupo(ruta_BD, "Deudas")
insertar_datos_grupo(ruta_BD, "Gastos")
insertar_datos_grupo(ruta_BD, "Ingresos")
 ''' 

'''
   # Insertar datos en CUENTAS (Nivel 2)
insertar_datos_subgrupo(ruta_BD, 1, "Efectivo")
insertar_datos_subgrupo(ruta_BD, 1, "Caixa Enginyers")
insertar_datos_subgrupo(ruta_BD, 1, "Self Bank")
insertar_datos_subgrupo(ruta_BD, 1, "DeGiro")
insertar_datos_subgrupo(ruta_BD, 1, "Trade Republic")
insertar_datos_subgrupo(ruta_BD, 1, "Santander")
insertar_datos_subgrupo(ruta_BD, 1, "BBVA")
insertar_datos_subgrupo(ruta_BD, 1, "B.Sabadell")
insertar_datos_subgrupo(ruta_BD, 1, "Civislend")
insertar_datos_subgrupo(ruta_BD, 1, "StockCrowd")
insertar_datos_subgrupo(ruta_BD, 1, "Mintos")
insertar_datos_subgrupo(ruta_BD, 1, "Bestinver")
insertar_datos_subgrupo(ruta_BD, 2, "Ahorro Hijos")
insertar_datos_subgrupo(ruta_BD, 2, "Deudas Casa")
insertar_datos_subgrupo(ruta_BD, 2, "Deudas inversiones")
insertar_datos_subgrupo(ruta_BD, 3, "Gastos fijos")
insertar_datos_subgrupo(ruta_BD, 3, "Gastos Variables")
insertar_datos_subgrupo(ruta_BD, 3, "Otros Gastos")
insertar_datos_subgrupo(ruta_BD, 4, "Salarios")
insertar_datos_subgrupo(ruta_BD, 4, "No Salariales")
insertar_datos_subgrupo(ruta_BD, 4, "Otros Ingresos")
''' 

'''
   # Insertar datos en CUENTAS (Nivel 3)
insertar_datos_cuenta(ruta_BD, 1, 1, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 1, "Depósitos")
insertar_datos_cuenta(ruta_BD, 1, 1, "Fondos Inv.")
insertar_datos_cuenta(ruta_BD, 1, 1, "Cta.Cte. $")
insertar_datos_cuenta(ruta_BD, 1, 1, "Depósitos $")
insertar_datos_cuenta(ruta_BD, 1, 2, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 2, "Cta. Remunerada")
insertar_datos_cuenta(ruta_BD, 1, 2, "Depósitos")
insertar_datos_cuenta(ruta_BD, 1, 2, "Fondos Inv.")
insertar_datos_cuenta(ruta_BD, 1, 2, "F.Inv. Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 4, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 4, "Renta Variable")
insertar_datos_cuenta(ruta_BD, 1, 4, "Derivados Financieros")
insertar_datos_cuenta(ruta_BD, 1, 3, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 3, "Renta Variable")
insertar_datos_cuenta(ruta_BD, 1, 3, "ETF")
insertar_datos_cuenta(ruta_BD, 1, 5, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 5, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 1, 6, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 6, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 1, 7, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 1, 8, "Plan Pensiones")
insertar_datos_cuenta(ruta_BD, 1, 8, "Fondos Inv.")
insertar_datos_cuenta(ruta_BD, 1, 9, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 1, 10, "CapitalCell")
insertar_datos_cuenta(ruta_BD, 1, 10, "Cebiotec")
insertar_datos_cuenta(ruta_BD, 1, 11, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 1, 12, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 12, "Depósitos")
insertar_datos_cuenta(ruta_BD, 1, 13, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 13, "Depósitos")    
insertar_datos_cuenta(ruta_BD, 1, 14, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 14, "Depósitos")    
insertar_datos_cuenta(ruta_BD, 1, 15, "Cta.Cte.")
insertar_datos_cuenta(ruta_BD, 1, 15, "Depósitos") 
insertar_datos_cuenta(ruta_BD, 1, 15, "Crowfunding")    
insertar_datos_cuenta(ruta_BD, 2, 1, "Roger")
insertar_datos_cuenta(ruta_BD, 2, 1, "Enric")
insertar_datos_cuenta(ruta_BD, 2, 2, "Enaire 0%")
insertar_datos_cuenta(ruta_BD, 2, 3, "Inversiones JMG")
insertar_datos_cuenta(ruta_BD, 2, 3, "Avis")
insertar_datos_cuenta(ruta_BD, 2, 3, "Tata")
insertar_datos_cuenta(ruta_BD, 2, 3, "Albert")
insertar_datos_cuenta(ruta_BD, 2, 3, "Joan Moises")
insertar_datos_cuenta(ruta_BD, 3, 1, "Comida")
insertar_datos_cuenta(ruta_BD, 3, 1, "Agua")
insertar_datos_cuenta(ruta_BD, 3, 1, "Luz")
insertar_datos_cuenta(ruta_BD, 3, 1, "Gas")
insertar_datos_cuenta(ruta_BD, 3, 1, "Teléfono/Internet")
insertar_datos_cuenta(ruta_BD, 3, 1, "Limpieza")
insertar_datos_cuenta(ruta_BD, 3, 1, "Comunidad Vecinos")
insertar_datos_cuenta(ruta_BD, 3, 1, "Otros Gastos Fijos")
insertar_datos_cuenta(ruta_BD, 3, 2, "Ropa")
insertar_datos_cuenta(ruta_BD, 3, 2, "Salud")
insertar_datos_cuenta(ruta_BD, 3, 2, "Transporte")
insertar_datos_cuenta(ruta_BD, 3, 2, "Seguros")
insertar_datos_cuenta(ruta_BD, 3, 2, "Impuestos")
insertar_datos_cuenta(ruta_BD, 3, 2, "Vacaciones")
insertar_datos_cuenta(ruta_BD, 3, 2, "Otros Gastos Variables")
insertar_datos_cuenta(ruta_BD, 3, 3, "Gastos Extraordinarios")
insertar_datos_cuenta(ruta_BD, 3, 3, "Otros Gastos Extraordinarios")
insertar_datos_cuenta(ruta_BD, 3, 3, "Cuadrar Saldos")
insertar_datos_cuenta(ruta_BD, 4, 1, "Montse")
insertar_datos_cuenta(ruta_BD, 4, 1, "Carlos")
insertar_datos_cuenta(ruta_BD, 4, 1, "Pensión")
insertar_datos_cuenta(ruta_BD, 4, 2, "Bancarios")
insertar_datos_cuenta(ruta_BD, 4, 2, "Renta Fija")
insertar_datos_cuenta(ruta_BD, 4, 2, "Renta Variable")
insertar_datos_cuenta(ruta_BD, 4, 2, "Fondos Inv.")
insertar_datos_cuenta(ruta_BD, 4, 2, "Crowfunding")
insertar_datos_cuenta(ruta_BD, 4, 3, "Otros Ingresos")

'''



