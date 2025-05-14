import sqlite3
import os
from datetime import date

empresa = "TEST_Empresa_1"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"


# ---------------------------------------- FUNCIONES DE CREAR BASE DE DATOS Y TABLAS ----------------------------------------
def crear_base_datos():
    conn = sqlite3.connect(ruta_BDapp)
    conn.commit()
    conn.close()

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


# ---------------------------------------- FUNCIONES DE INSERTAR DATOS ----------------------------------------
def insertar_datos_grupo(ruta_BDapp, descripcion_grupo):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO GRUPO (descripcion_grupo) VALUES (?)
            """, (descripcion_grupo.upper(),))
            conn.commit()
        print(f"Insertado en GRUPO (Nivel 1): descripcion_grupo='{descripcion_grupo.upper()}'")
    except sqlite3.IntegrityError as e:
        print(f"Error al insertar en GRUPO (Nivel 1): {e}")
        raise

def insertar_datos_subgrupo(ruta_BDapp, grupo_id, descripcion_subgrupo):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
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
        raise

def insertar_datos_cuenta(ruta_BDapp, grupo_id, subgrupo_id, descripcion_n3, saldo_inicial=0.0, fecha_inicio=None):
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(MAX(nivel3_id), 0) + 1
                FROM CUENTAS
                WHERE grupo_id = ? AND subgrupo_id = ?
            """, (grupo_id, subgrupo_id))
            nivel3_id = cursor.fetchone()[0]
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
                fecha_inicio_insertar = fecha_inicio if fecha_inicio else date.today().isoformat()
                cursor.execute("""
                    INSERT INTO CUENTAS (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3, Saldo_inicial, Fecha_Inicio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (grupo_id, subgrupo_id, cod_2, desc_2, nivel3_id, descripcion_n3, cod_3, desc_3, saldo_inicial, fecha_inicio_insertar))
                conn.commit()
                print(f"Insertado en CUENTAS (Nivel 3): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2={desc_2}, nivel3_id={nivel3_id}, descripcion_n3='{descripcion_n3}', cod_3={cod_3}, desc_3='{desc_3}', Saldo_inicial={saldo_inicial}, Fecha_Inicio='{fecha_inicio_insertar}'")
            else:
                print(f"No se encontró subgrupo con grupo_id={grupo_id} y subgrupo_id={subgrupo_id}")
    except sqlite3.Error as e:
        print(f"Error al insertar en CUENTAS (Nivel 3): {e}")
        raise


# ---------------------------------------- FUNCIONES DE MOSTRAR DATOS ----------------------------------------
def mostrar_datos_grupo(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
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

def mostrar_datos_subgrupo(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
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

def mostrar_datos_cuentas(ruta_BDapp):
    try:
        conn = sqlite3.connect(ruta_BDapp)
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

def ver_tablas_base_datos():
    conn = sqlite3.connect(ruta_BDapp)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:")
    if tablas:
        for tabla in tablas:
            print(f"- {tabla[0]}")
    else:
        print("No hay tablas en la base de datos.")
    conn.close()

# ---------------------------------------- FUNCIONES DE INICIO ----------------------------------------
def inicio_Base_datos():
    crear_base_datos()
    crear_tabla_GRUPO(ruta_BDapp)
    crear_tabla_SUBGRUPO(ruta_BDapp)
    crear_tabla_CUENTAS(ruta_BDapp)

def insertar_datos_iniciales():
    # ... (igual que tu función actual, usando ruta_BDapp en todas las llamadas)

    """
    Inserta datos iniciales en la base de datos.
    """

    # Insertar datos en GRUPO (Nivel 1)
    insertar_datos_grupo(ruta_BDapp, "Cuentas Financieras")
    insertar_datos_grupo(ruta_BDapp, "Deudas")
    insertar_datos_grupo(ruta_BDapp, "Gastos")
    insertar_datos_grupo(ruta_BDapp, "Ingresos")

    # Insertar datos en CUENTAS (Nivel 2)
    insertar_datos_subgrupo(ruta_BDapp, 1, "Efectivo")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Caixa Enginyers")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Self Bank")
    insertar_datos_subgrupo(ruta_BDapp, 1, "DeGiro")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Trade Republic")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Santander")
    insertar_datos_subgrupo(ruta_BDapp, 1, "BBVA")
    insertar_datos_subgrupo(ruta_BDapp, 1, "B.Sabadell")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Civislend")
    insertar_datos_subgrupo(ruta_BDapp, 1, "StockCrowd")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Mintos")
    insertar_datos_subgrupo(ruta_BDapp, 1, "Bestinver")
    insertar_datos_subgrupo(ruta_BDapp, 2, "Ahorro Hijos")
    insertar_datos_subgrupo(ruta_BDapp, 2, "Deudas Casa")
    insertar_datos_subgrupo(ruta_BDapp, 2, "Deudas inversiones")
    insertar_datos_subgrupo(ruta_BDapp, 3, "Gastos fijos")
    insertar_datos_subgrupo(ruta_BDapp, 3, "Gastos Variables")
    insertar_datos_subgrupo(ruta_BDapp, 3, "Otros Gastos")
    insertar_datos_subgrupo(ruta_BDapp, 4, "Salarios")
    insertar_datos_subgrupo(ruta_BDapp, 4, "No Salariales")
    insertar_datos_subgrupo(ruta_BDapp, 4, "Otros Ingresos")

    # Insertar datos en CUENTAS (Nivel 3)
    insertar_datos_cuenta(ruta_BDapp, 1, 1, "Carlos")
    insertar_datos_cuenta(ruta_BDapp, 1, 1, "Montse")    
    insertar_datos_cuenta(ruta_BDapp, 1, 2, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 2, "Depósitos")
    insertar_datos_cuenta(ruta_BDapp, 1, 2, "Fondos Inv.")
    insertar_datos_cuenta(ruta_BDapp, 1, 2, "Cta.Cte. $")
    insertar_datos_cuenta(ruta_BDapp, 1, 2, "Depósitos $")
    insertar_datos_cuenta(ruta_BDapp, 1, 3, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 3, "Cta. Remunerada")
    insertar_datos_cuenta(ruta_BDapp, 1, 3, "Fondos Inv.")
    insertar_datos_cuenta(ruta_BDapp, 1, 3, "F.Inv. Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 4, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 4, "Renta Variable")
    insertar_datos_cuenta(ruta_BDapp, 1, 4, "ETF")
    insertar_datos_cuenta(ruta_BDapp, 1, 4, "Fondos Inv.")  
    insertar_datos_cuenta(ruta_BDapp, 1, 5, "Cta.Remunerada.")
    insertar_datos_cuenta(ruta_BDapp, 1, 5, "Renta Variable")
    insertar_datos_cuenta(ruta_BDapp, 1, 5, "ETF")
    insertar_datos_cuenta(ruta_BDapp, 1, 6, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 6, "Crowfunding")
    insertar_datos_cuenta(ruta_BDapp, 1, 6, "Derivados Financieros")
    insertar_datos_cuenta(ruta_BDapp, 1, 7, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 7, "P.P Empresa")
    insertar_datos_cuenta(ruta_BDapp, 1, 8, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 9, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 9, "Crowfunding")
    insertar_datos_cuenta(ruta_BDapp, 1, 10, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 10, "Crowfunding")
    insertar_datos_cuenta(ruta_BDapp, 1, 11, "Cta.Cte.")
    insertar_datos_cuenta(ruta_BDapp, 1, 11, "Crowfunding") 
    insertar_datos_cuenta(ruta_BDapp, 1, 12, "Plan Pensiones")
    insertar_datos_cuenta(ruta_BDapp, 1, 12, "Fondos Inv.")
    insertar_datos_cuenta(ruta_BDapp, 1, 13, "CapitalCell")
    insertar_datos_cuenta(ruta_BDapp, 1, 13, "Cebiotec")    
    insertar_datos_cuenta(ruta_BDapp, 2, 1, "Roger")
    insertar_datos_cuenta(ruta_BDapp, 2, 1, "Enric")
    insertar_datos_cuenta(ruta_BDapp, 2, 2, "Enaire 0%")
    insertar_datos_cuenta(ruta_BDapp, 2, 3, "Inversiones JMG")
    insertar_datos_cuenta(ruta_BDapp, 2, 3, "Avis")
    insertar_datos_cuenta(ruta_BDapp, 2, 3, "Tata")
    insertar_datos_cuenta(ruta_BDapp, 2, 3, "Albert")
    insertar_datos_cuenta(ruta_BDapp, 2, 3, "Joan Moises")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Comida")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Agua")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Luz")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Gas")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Teléfono/Internet")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Limpieza")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Comunidad Vecinos")
    insertar_datos_cuenta(ruta_BDapp, 3, 1, "Otros Gastos Fijos")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Ropa")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Salud")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Transporte")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Seguros")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Impuestos")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Vacaciones")
    insertar_datos_cuenta(ruta_BDapp, 3, 2, "Otros Gastos Variables")
    insertar_datos_cuenta(ruta_BDapp, 3, 3, "Gastos Extraordinarios")
    insertar_datos_cuenta(ruta_BDapp, 3, 3, "Otros Gastos Extraordinarios")
    insertar_datos_cuenta(ruta_BDapp, 3, 3, "Cuadrar Saldos")
    insertar_datos_cuenta(ruta_BDapp, 4, 1, "Montse")
    insertar_datos_cuenta(ruta_BDapp, 4, 1, "Carlos")
    insertar_datos_cuenta(ruta_BDapp, 4, 1, "Pensión")
    insertar_datos_cuenta(ruta_BDapp, 4, 2, "Bancarios")
    insertar_datos_cuenta(ruta_BDapp, 4, 2, "Renta Fija")
    insertar_datos_cuenta(ruta_BDapp, 4, 2, "Renta Variable")
    insertar_datos_cuenta(ruta_BDapp, 4, 2, "Fondos Inv.")
    insertar_datos_cuenta(ruta_BDapp, 4, 2, "Crowfunding")
    insertar_datos_cuenta(ruta_BDapp, 4, 3, "Otros Ingresos")




if __name__ == "__main__":
    def existe_base_de_datos(ruta_db):
        return os.path.exists(ruta_db)

    if existe_base_de_datos(ruta_BDapp):
        print(f"La base de datos '{ruta_BDapp}' existe.")
        try:
            conn = sqlite3.connect(ruta_BDapp)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    else:
        print(f"La base de datos '{ruta_BDapp}' NO EXISTE.")
        inicio_Base_datos()
        ver_tablas_base_datos()
        insertar_datos_iniciales()
        mostrar_datos_grupo(ruta_BDapp)
        mostrar_datos_subgrupo(ruta_BDapp)
        mostrar_datos_cuentas(ruta_BDapp)

    
