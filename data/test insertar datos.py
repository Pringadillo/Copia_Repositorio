import sqlite3
import os
from datetime import datetime

empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"

# --------------------------- CREAR BASE DE DATOS ---------------------------
def crear_base_datos():
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()
    conn.commit()
    conn.close()

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

#crear_base_datos()
#ver_tablas_base_datos()

# ------------------------  TABLA_NIVEL1
def crear_tabla_nivel1():
    """Crea la tabla nivel1 si no existe."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear tabla para el nivel 1
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla nivel1 creada (si no existía).")

def insertar_datos_nivel1(descripcion):
    """Inserta un nuevo registro en la tabla nivel1."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar un nuevo registro en la tabla nivel1
    cursor.execute("INSERT INTO nivel1 (descripcion) VALUES (?)", (descripcion,))
    
    conn.commit()
    conn.close()
    print(f"Se ha insertado el registro en nivel1: {descripcion}")

def ver_tabla_nivel1():
    """Consulta y muestra todos los registros de la tabla nivel1."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener todos los registros de la tabla nivel1
    cursor.execute("SELECT * FROM nivel1")
    resultados = cursor.fetchall()

    print("Contenido de la tabla nivel1:")
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, {fila[1]}")
    else:
        print("La tabla nivel1 está vacía.")

    conn.close()

def eliminar_datos_nivel1():
    """Elimina todos los registros de la tabla nivel1."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar todos los registros de la tabla nivel1
    cursor.execute("DELETE FROM nivel1")
    
    conn.commit()
    conn.close()
    print("Todos los registros de la tabla nivel1 han sido eliminados.")

#crear_tabla_nivel1()
#insertar_datos_nivel1("Cuentas Financieras")
#insertar_datos_nivel1("Pasivo")
#insertar_datos_nivel1("Gastos")
#insertar_datos_nivel1("Ingresos")
#ver_tabla_nivel1()
#eliminar_datos_nivel1()

# -------------------------  TABLA_NIVEL2 
def crear_tabla_nivel2():
    """Crea la tabla nivel2 si no existe."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear tabla para el nivel 2
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        nivel1_id INTEGER NOT NULL,
        FOREIGN KEY (nivel1_id) REFERENCES nivel1 (id)
    )
    """)

    conn.commit()
    conn.close()
    
def insertar_datos_nivel2(descripcion, nivel1_id):
    """Inserta un nuevo registro en la tabla nivel2."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar un nuevo registro en la tabla nivel2
    cursor.execute("INSERT INTO nivel2 (descripcion, nivel1_id) VALUES (?, ?)", (descripcion, nivel1_id))
    
    conn.commit()
    conn.close()
    print(f"Se ha insertado el registro en nivel2: {descripcion}, nivel1_id: {nivel1_id}")

def ver_tabla_nivel2():
    """Consulta y muestra todos los registros de la tabla nivel2."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener todos los registros de la tabla nivel2
    cursor.execute("SELECT * FROM nivel2")
    resultados = cursor.fetchall()

    print("Contenido de la tabla nivel2:")
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, Descripción: {fila[1]}, Nivel1_ID: {fila[2]}")
    else:
        print("La tabla nivel2 está vacía.")

    conn.close()

def actualizar_datos_nivel2(id, nueva_descripcion, nuevo_nivel1_id):
    """Actualiza un registro en la tabla nivel2."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE nivel2
    SET descripcion = ?, nivel1_id = ?
    WHERE id = ?
    """, (nueva_descripcion, nuevo_nivel1_id, id))
    
    conn.commit()
    conn.close()
    print(f"Se ha actualizado el registro con ID: {id}")

def eliminar_datos_nivel2(id):
    """Elimina un registro específico de la tabla nivel2."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar el registro con el ID especificado
    cursor.execute("DELETE FROM nivel2 WHERE id = ?", (id,))
    
    conn.commit()
    conn.close()
    print(f"Se ha eliminado el registro con ID: {id}")

#crear_tabla_nivel2()
#insertar_datos_nivel2("CaixaEnginyers", 1)
#actualizar_datos_nivel2(3, "Self Bank", 1)
#eliminar_datos_nivel2(3)
#ver_tabla_nivel2()
# --------------------------   TABLA_NIVEL3

def crear_tabla_nivel3():
    """Crea la tabla nivel3 si no existe."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear tabla para el nivel 3
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        nivel2_id INTEGER NOT NULL,
        importe REAL DEFAULT 0,  -- Nueva columna para importe
        fecha_inicio TEXT NOT NULL DEFAULT (DATE('now')),  -- Fecha obligatoria, por defecto el día actual
        FOREIGN KEY (nivel2_id) REFERENCES nivel2 (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla nivel3 creada (si no existía).")

def insertar_datos_nivel3(descripcion, nivel2_id, importe=0, fecha_inicio=None):
    """Inserta un nuevo registro en la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar un nuevo registro en la tabla nivel3
    cursor.execute("""
    INSERT INTO nivel3 (descripcion, nivel2_id, importe, fecha_inicio)
    VALUES (?, ?, ?, ?)
    """, (descripcion, nivel2_id, importe, fecha_inicio))
    
    conn.commit()
    conn.close()
    
def ver_tabla_nivel3():
    """Consulta y muestra todos los registros de la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener todos los registros de la tabla nivel3
    cursor.execute("SELECT * FROM nivel3")
    resultados = cursor.fetchall()

    print("Contenido de la tabla nivel3:")
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, Descripción: {fila[1]}, Nivel2_ID: {fila[2]}, Importe: {fila[3]}, Fecha Inicio: {fila[4]}")
    else:
        print("La tabla nivel3 está vacía.")

    conn.close()

def actualizar_datos_nivel3(id, nueva_descripcion, nuevo_nivel2_id, nuevo_importe, nueva_fecha_inicio):
    """Actualiza un registro en la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Actualizar el registro con el ID especificado
    cursor.execute("""
    UPDATE nivel3
    SET descripcion = ?, nivel2_id = ?, importe = ?, fecha_inicio = ?
    WHERE id = ?
    """, (nueva_descripcion, nuevo_nivel2_id, nuevo_importe, nueva_fecha_inicio, id))
    
    conn.commit()
    conn.close()
    print(f"Se ha actualizado el registro con ID: {id}")

def eliminar_datos_nivel3(id):
    """Elimina un registro específico de la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar el registro con el ID especificado
    cursor.execute("DELETE FROM nivel3 WHERE id = ?", (id,))
    
    conn.commit()
    conn.close()
    print(f"Se ha eliminado el registro con ID: {id}")

#crear_tabla_nivel3()
#insertar_datos_nivel3("Carlos", 1, 100, "2025-01-01")  # Suponiendo que nivel2_id = 1 existe
#insertar_datos_nivel3("Montse", 1, 200, "2025-01-02")  # Suponiendo que nivel2_id = 1 existe
#insertar_datos_nivel3("Cta.Cte.", 3, 3000, "2025-01-03")  # Suponiendo que nivel2_id = 1 existe
#actualizar_datos_nivel3(4, "Depósito", 1, 20000, "2025-03-10")
#eliminar_datos_nivel3(3)
#ver_tabla_nivel3()

