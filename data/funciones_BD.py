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

# -------------------------  TABLA PRODUCTOS FINANCIEROS

def crear_tabla_productosfinancieros():
    """Crea la tabla productosfinancieros si no existe."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear tabla para productos financieros
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productosfinancieros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla productosfinancieros creada (si no existía).")

def insertar_datos_productosfinancieros(descripcion):
    """Inserta un nuevo registro en la tabla productosfinancieros."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar un nuevo registro en la tabla productosfinancieros
    cursor.execute("""
    INSERT INTO productosfinancieros (descripcion)
    VALUES (?)
    """, (descripcion,))
    
    conn.commit()
    conn.close()
    print(f"Se ha insertado el registro en productosfinancieros: {descripcion}")

def ver_tabla_productosfinancieros():
    """Consulta y muestra todos los registros de la tabla productosfinancieros."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener todos los registros de la tabla productosfinancieros
    cursor.execute("SELECT * FROM productosfinancieros")
    resultados = cursor.fetchall()

    print("Contenido de la tabla productosfinancieros:")
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, Descripción: {fila[1]}")
    else:
        print("La tabla productosfinancieros está vacía.")

    conn.close()

def actualizar_datos_productosfinancieros(id, nueva_descripcion):
    """Actualiza un registro en la tabla productosfinancieros."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Actualizar el registro con el ID especificado
    cursor.execute("""
    UPDATE productosfinancieros
    SET descripcion = ?
    WHERE id = ?
    """, (nueva_descripcion, id))
    
    conn.commit()
    conn.close()
    print(f"Se ha actualizado el registro con ID: {id}")

def eliminar_datos_productosfinancieros(id):
    """Elimina un registro específico de la tabla productosfinancieros."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar el registro con el ID especificado
    cursor.execute("DELETE FROM productosfinancieros WHERE id = ?", (id,))
    
    conn.commit()
    conn.close()
    print(f"Se ha eliminado el registro con ID: {id}")

#crear_tabla_productosfinancieros()
#insertar_datos_productosfinancieros("Cta.Remunerada")
#actualizar_datos_productosfinancieros(2, "Cta.Remunerada")
#eliminar_datos_productosfinancieros(3)
#ver_tabla_productosfinancieros()


# --------------------------   TABLA_NIVEL3

def crear_tabla_nivel3():
    """Crea la tabla nivel3 si no existe."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear tabla para el nivel 3
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nivel1_id INTEGER NOT NULL,  
        nivel2_id INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        importe REAL DEFAULT 0,  
        fecha_inicio TEXT NOT NULL DEFAULT (DATE('now')),  -- Fecha obligatoria, por defecto el día actual
        FOREIGN KEY (nivel1_id) REFERENCES nivel1 (id),  -- Relación con nivel1
        FOREIGN KEY (nivel2_id) REFERENCES nivel2 (id)   -- Relación con nivel2
    )
    """)

    conn.commit()
    conn.close()
    print("Tabla nivel3 creada (si no existía).")

def insertar_datos_nivel3( nivel1_id, nivel2_id, descripcion, importe=0, fecha_inicio=None):
    """Inserta un nuevo registro en la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar un nuevo registro en la tabla nivel3
    cursor.execute("""
    INSERT INTO nivel3 (nivel1_id, nivel2_id, descripcion, importe, fecha_inicio)
    VALUES (?, ?, ?, ?, ?)
    """, (nivel1_id, nivel2_id, descripcion, importe, fecha_inicio))
    
    conn.commit()
    conn.close()
    print(f"Se ha insertado el registro en nivel3: {descripcion}, nivel1_id: {nivel1_id}, nivel2_id: {nivel2_id}")

def ver_tabla_nivel3():
    """Consulta y muestra todos los registros de la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener todos los registros de la tabla nivel3
    cursor.execute("""
    SELECT 
        nivel3.nivel1_id, 
        nivel3.nivel2_id, 
        nivel3.id, 
        nivel3.descripcion, 
        nivel3.importe, 
        nivel3.fecha_inicio 
    FROM nivel3
    """)
    resultados = cursor.fetchall()

    print("Contenido de la tabla nivel3:")
    if resultados:
        for fila in resultados:
            print(f"ID: {fila[0]}, {fila[1]},  {fila[2]}, : {fila[3]}, Importe: {fila[4]}, Fecha Inicio: {fila[5]}")
    else:
        print("La tabla nivel3 está vacía.")

    conn.close()

def actualizar_datos_nivel3(id, nueva_descripcion, nuevo_nivel1_id, nuevo_nivel2_id, nuevo_importe, nueva_fecha_inicio):
    """Actualiza un registro en la tabla nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Actualizar el registro con el ID especificado
    cursor.execute("""
    UPDATE nivel3
    SET descripcion = ?, nivel1_id = ?, nivel2_id = ?, importe = ?, fecha_inicio = ?
    WHERE id = ?
    """, (nueva_descripcion, nuevo_nivel1_id, nuevo_nivel2_id, nuevo_importe, nueva_fecha_inicio, id))
    
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
#insertar_datos_nivel3( 1, 1,"Carlos", 100, "2025-01-01")  # Suponiendo que nivel2_id = 1 existe
#insertar_datos_nivel3("Montse", 1, 1, 200, "2025-01-02")  # Suponiendo que nivel2_id = 1 existe
#insertar_datos_nivel3("Cta.Cte.", 1, 3, 3000, "2025-01-03")  # Suponiendo que nivel2_id = 1 existe
#actualizar_datos_nivel3(4, "Depósito", 1, 1, 20000, "2025-03-10")
#eliminar_datos_nivel3(3)
#ver_tabla_nivel3()




# ------------------------------ CREAR TABLA INICIAL ------------------------------
# ---------------------------------------------------------------------------------

def insertar_datos_iniciales():
    #crear_base_datos()
    # Crear tablas productos financieros
    #crear_tabla_productosfinancieros()
    insertar_datos_productosfinancieros("Cta. Cte.")
    insertar_datos_productosfinancieros("Cta. Remunerada")
    insertar_datos_productosfinancieros("Depósito")
    insertar_datos_productosfinancieros("Fondo Inversión")
    insertar_datos_productosfinancieros("Renta Fija")
    insertar_datos_productosfinancieros("Renta Variable")
    insertar_datos_productosfinancieros("Fondo Pensiones")
    insertar_datos_productosfinancieros("Crowdfunding")
    insertar_datos_productosfinancieros("Inversiones en empresas")
    insertar_datos_productosfinancieros("Derivados fiancieros")
    #Datos Tabla_nivel1
    #crear_tabla_nivel1()
    insertar_datos_nivel1("Cuentas Financieras")
    insertar_datos_nivel1("Pasivo")
    insertar_datos_nivel1("Gastos")
    insertar_datos_nivel1("Ingresos")
    #Datos Tabla_nivel2
    #crear_tabla_nivel2()
    insertar_datos_nivel2("Efectivo", 1)  
    insertar_datos_nivel2("Caixa Enginyers", 1)
    insertar_datos_nivel2("Self Bank", 1)
    insertar_datos_nivel2("DeGiro", 1)
    insertar_datos_nivel2("Trade Republic", 1)
    insertar_datos_nivel2("Santander", 1)
    insertar_datos_nivel2("BBVA", 1)
    insertar_datos_nivel2("B.Sabadell", 1)
    insertar_datos_nivel2("Civislend", 1)
    insertar_datos_nivel2("StockCrowd", 1)
    insertar_datos_nivel2("Mintos", 1)
    insertar_datos_nivel2("Bestinver", 1)
    insertar_datos_nivel2("Ahorro Hijos", 2)
    insertar_datos_nivel2("Deudas Casa", 2)
    insertar_datos_nivel2("Deudas inversiones", 2)   
    insertar_datos_nivel2("Gastos fijos", 3)
    insertar_datos_nivel2("Gastos Variables", 3)
    insertar_datos_nivel2("Otros Gastos", 3)       
    insertar_datos_nivel2("Salarios", 4)
    insertar_datos_nivel2("No Salariales", 4)
    insertar_datos_nivel2("Otros Ingresos", 4)
    #Datos Tabla_nivel3
    #crear_tabla_nivel3()
    insertar_datos_nivel3(1,1,"Carlos", 50, "2025-01-01") 
    insertar_datos_nivel3(1,1,"Montse", 50, "2025-01-01")
    insertar_datos_nivel3(1,2,"Cta.Cte.", 5060, "2025-01-01")
    insertar_datos_nivel3(1,2,"Cta. Remunerada", 10000, "2025-01-01")
    insertar_datos_nivel3(1,3,"Cta. Cte.", 1000, "2025-01-01")
    insertar_datos_nivel3(1,3,"Cta. Remunerada", 6000, "2025-01-01")
    insertar_datos_nivel3(2,1,"Roger", 6000, "2025-01-01")
    insertar_datos_nivel3(2,1,"Enric", 6000, "2025-01-01")
    insertar_datos_nivel3(2,2,"Enaire 0%", 6000, "2025-01-01")
    insertar_datos_nivel3(2,2,"Avis", 6000, "2025-01-01")
    insertar_datos_nivel3(2,3,"JMG inversiones", 90000, "2025-01-01")
    insertar_datos_nivel3(3,1,"Agua", 0, "2025-01-01")
    insertar_datos_nivel3(3,1,"Luz", 0, "2025-01-01")
    insertar_datos_nivel3(3,1,"Gas", 0, "2025-01-01")
    insertar_datos_nivel3(3,2,"Salud", 0, "2025-01-01")
    insertar_datos_nivel3(3,3,"Otros Gastos", 0, "2025-01-01")
    insertar_datos_nivel3(4,1,"Montse", 0, "2025-01-01")
    insertar_datos_nivel3(4,1,"Carlos", 0, "2025-01-01")
    insertar_datos_nivel3(4,1,"Pensió", 0, "2025-01-01")
    insertar_datos_nivel3(4,2,"Int. Bancarios", 0, "2025-01-01")
    insertar_datos_nivel3(4,2,"Int. Crowd.", 0, "2025-01-01")
    insertar_datos_nivel3(4,3,"Otros Ingresos", 0, "2025-01-01")

   
   

def crear_vista_niveles():
    """Crea una vista que combina nivel1, nivel2 y nivel3."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Crear la vista
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS vista_niveles AS
    SELECT 
        nivel1.id AS id_nivel1,
        nivel2.id AS id_nivel2,
        nivel3.id AS id_nivel3,
        nivel1.descripcion AS concepto_nivel1,
        nivel2.descripcion AS concepto_nivel2,
        nivel3.descripcion AS concepto_nivel3,
        nivel3.importe AS importe,
        nivel3.fecha_inicio AS fechainicio
    FROM 
        nivel3
    INNER JOIN 
        nivel2 ON nivel3.nivel2_id = nivel2.id
    INNER JOIN 
        nivel1 ON nivel3.nivel1_id = nivel1.id
    """)

    conn.commit()
    conn.close()
    print("Vista 'vista_niveles' creada (si no existía).")

def ver_vista_niveles():
    """Consulta y muestra los datos de la vista 'vista_niveles'."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consultar la vista
    cursor.execute("SELECT * FROM vista_niveles")
    resultados = cursor.fetchall()

    print("Contenido de la vista 'vista_niveles':")
    if resultados:
        for fila in resultados:
            print(f"ID Nivel1: {fila[0]}, ID Nivel2: {fila[1]}, ID Nivel3: {fila[2]}, "
                  f"Concepto Nivel1: {fila[3]}, Concepto Nivel2: {fila[4]}, Concepto Nivel3: {fila[5]}, "
                  f"Importe: {fila[6]}, Fecha Inicio: {fila[7]}")
    else:
        print("La vista 'vista_niveles' está vacía.")

    conn.close()


#crear_tabla_codigo_inicio()



def verificar_estado_base_datos():
    """Verifica si la base de datos y las tablas existen."""
    print("Verificando estado de la base de datos...")
    crear_base_datos()
    ver_tablas_base_datos()

def crear_tabla_codigo_inicio():
    """Crea la base de datos y las tablas necesarias en el orden correcto."""
    crear_base_datos()
    crear_tabla_nivel1()
    crear_tabla_nivel2()
    crear_tabla_nivel3()
    crear_tabla_productosfinancieros()
    print("Todas las tablas se han creado correctamente.")


def ver_tabla_transformada():
    """Consulta y muestra una tabla transformada con las columnas solicitadas."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener los datos transformados
    cursor.execute("""
    SELECT 
        nivel1.id || '.' || nivel2.id || '.' || nivel3.id AS codigo,
        nivel1.descripcion AS concepto_nivel1,
        nivel2.descripcion AS concepto_nivel2,
        nivel3.descripcion AS concepto_nivel3,
        nivel3.importe AS importe,
        nivel3.fecha_inicio AS fecha
    FROM 
        nivel3
    INNER JOIN 
        nivel2 ON nivel3.nivel2_id = nivel2.id
    INNER JOIN 
        nivel1 ON nivel3.nivel1_id = nivel1.id
    """)
    resultados = cursor.fetchall()

    print("Tabla transformada:")
    if resultados:
        for fila in resultados:
            print(f"{fila[0]}, {fila[1]}, {fila[2]},{fila[3]}, Importe: {fila[4]}, Fecha: {fila[5]}")
    else:
        print("No hay datos en la tabla transformada.")

    conn.close()


#verificar_estado_base_datos()
#crear_tabla_codigo_inicio()
#insertar_datos_iniciales()
#ver_tabla_transformada()