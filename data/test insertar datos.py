import sqlite3

empresa = "Mi Empresa"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"

def crear_tablas():
    """Crea las tablas para los tres niveles jerárquicos."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar la tabla nivel3 si ya existe
    cursor.execute("DROP TABLE IF EXISTS nivel3")

    # Crear tabla para el nivel 1
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    )
    """)

    # Crear tabla para el nivel 2
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        nivel1_id INTEGER NOT NULL,
        FOREIGN KEY (nivel1_id) REFERENCES nivel1 (id)
    )
    """)

    # Crear tabla para el nivel 3
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nivel3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        nivel2_id INTEGER NOT NULL,
        importe REAL DEFAULT 0,  -- Nueva columna para importe
        fecha_inicio TEXT,       -- Nueva columna para fecha de inicio
        FOREIGN KEY (nivel2_id) REFERENCES nivel2 (id)
    )
    """)

    conn.commit()
    conn.close()

def insertar_datos():
    """Inserta datos en las tablas jerárquicas."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Insertar datos en nivel 1
    cursor.execute("INSERT INTO nivel1 (descripcion) VALUES ('Activo')")
    cursor.execute("INSERT INTO nivel1 (descripcion) VALUES ('Pasivo')")

    # Obtener el ID del nivel 1 "Activo"
    cursor.execute("SELECT id FROM nivel1 WHERE descripcion = 'Activo'")
    activo_id = cursor.fetchone()[0]

    # Insertar datos en nivel 2 bajo "Activo"
    cursor.execute("INSERT INTO nivel2 (descripcion, nivel1_id) VALUES ('Caja', ?)", (activo_id,))
    cursor.execute("INSERT INTO nivel2 (descripcion, nivel1_id) VALUES ('Bancos', ?)", (activo_id,))

    # Obtener el ID del nivel 2 "Caja"
    cursor.execute("SELECT id FROM nivel2 WHERE descripcion = 'Caja'")
    caja_id = cursor.fetchone()[0]

    # Insertar datos en nivel 3 bajo "Caja"
    cursor.execute("INSERT INTO nivel3 (descripcion, nivel2_id, importe, fecha_inicio) VALUES ('Caja General', ?, 1500, '2025-01-01')", (caja_id,))
    cursor.execute("INSERT INTO nivel3 (descripcion, nivel2_id, importe, fecha_inicio) VALUES ('Caja Chica', ?, 500, '2025-02-01')", (caja_id,))

    conn.commit()
    conn.close()

def consultar_formato_jerarquico():
    """Consulta y muestra la jerarquía en formato '1.01.01' con la descripción del último nivel."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Consulta para obtener la jerarquía en formato "1.01.01"
    cursor.execute("""
    SELECT 
        n1.id AS nivel1_id,
        n2.id AS nivel2_id,
        n3.id AS nivel3_id,
        n1.descripcion AS nivel1_desc,
        n2.descripcion AS nivel2_desc,
        n3.descripcion AS nivel3_desc,
        n3.importe AS nivel3_importe,
        n3.fecha_inicio AS nivel3_fecha_inicio
    FROM nivel1 n1
    LEFT JOIN nivel2 n2 ON n1.id = n2.nivel1_id
    LEFT JOIN nivel3 n3 ON n2.id = n3.nivel2_id
    ORDER BY n1.id, n2.id, n3.id
    """)

    print("Jerarquía en formato '1.01.01':")
    for row in cursor.fetchall():
        nivel1_id = row[0]
        nivel2_id = row[1] if row[1] is not None else 0
        nivel3_id = row[2] if row[2] is not None else 0
        descripcion = row[5] if row[5] is not None else row[4] if row[4] is not None else row[3]
        importe = row[6] if row[6] is not None else 0
        fecha_inicio = row[7] if row[7] is not None else "N/A"

        # Formatear el código jerárquico
        codigo_jerarquico = f"{nivel1_id}.{nivel2_id:02}.{nivel3_id:02}"
        print(f"{codigo_jerarquico} - {descripcion} - Importe: {importe} - Fecha Inicio: {fecha_inicio}")

    conn.close()

def verificar_estructura_tabla():
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Ejecutar PRAGMA para obtener la información de la tabla nivel3
    cursor.execute("PRAGMA table_info(nivel3);")
    print("Estructura de la tabla nivel3:")
    for row in cursor.fetchall():
        print(row)

    conn.close()


def eliminar_datos():
    """Elimina todos los datos de las tablas jerárquicas."""
    conn = sqlite3.connect(ruta_BD)
    cursor = conn.cursor()

    # Eliminar datos de las tablas en orden jerárquico (de nivel3 a nivel1)
    cursor.execute("DELETE FROM nivel3")
    cursor.execute("DELETE FROM nivel2")
    cursor.execute("DELETE FROM nivel1")

    conn.commit()
    conn.close()
    print("Todos los datos han sido eliminados de las tablas.")



# Ejecutar las funciones
#crear_tablas()
#insertar_datos()
#consultar_formato_jerarquico()
#verificar_estructura_tabla()
#eliminar_datos()

