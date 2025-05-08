import sqlite3

empresa = "Test_BD_2"
BasedeDatos = f"bd_{empresa}.db"
ruta_BD = f"./data/{BasedeDatos}"

def crear_tabla_grupo():
    """
    Crea la tabla GRUPO (Nivel 1) si no existe.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS GRUPO (
                grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion_grupo TEXT NOT NULL UNIQUE CHECK (descripcion_grupo = UPPER(descripcion_grupo))
            )
        """)
        conn.commit()
    print("Tabla GRUPO (Nivel 1) creada (si no existía).")

def crear_tabla_subgrupo():
    """
    Crea la tabla SUBGRUPO (Nivel 2) si no existe.
    """
    with sqlite3.connect(ruta_BD) as conn:
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

def crear_tabla_cuentas():
    """
    Crea la tabla CUENTAS (Nivel 3) si no existe.
    """
    with sqlite3.connect(ruta_BD) as conn:
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


def insertar_datos_grupo(descripcion_grupo):
    """
    Inserta datos en la tabla GRUPO (Nivel 1).

    Args:
        descripcion_grupo (str): Descripción del grupo.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO GRUPO (descripcion_grupo) VALUES (?)
            """, (descripcion_grupo,))
            conn.commit()
            print(f"Insertado en GRUPO (Nivel 1): descripcion_grupo='{descripcion_grupo}'")
        except sqlite3.IntegrityError as e:
            print(f"Error al insertar en GRUPO (Nivel 1): {e}")

def insertar_datos_subgrupo(grupo_id, descripcion_subgrupo):
    """
    Inserta datos en la tabla SUBGRUPO (Nivel 2).

    Args:
        grupo_id (int): ID del grupo al que pertenece.
        descripcion_subgrupo (str): Descripción del subgrupo.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        # Obtener el máximo subgrupo_id para el grupo_id dado
        cursor.execute("""
            SELECT COALESCE(MAX(subgrupo_id), 0) + 1
            FROM SUBGRUPO
            WHERE grupo_id = ?
        """, (grupo_id,))
        subgrupo_id = cursor.fetchone()[0]
        cod_2 = f"{grupo_id}.{subgrupo_id:02d}"
        cursor.execute("""
            SELECT descripcion_grupo
            FROM GRUPO
            WHERE grupo_id = ?
        """, (grupo_id,))
        descripcion_grupo = cursor.fetchone()[0]
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

def insertar_datos_cuenta(grupo_id, subgrupo_id, descripcion_n3):
    """
    Inserta datos en la tabla CUENTAS (Nivel 3).

    Args:
        grupo_id (int): ID del grupo al que pertenece.
        subgrupo_id (int): ID del subgrupo al que pertenece.
        descripcion_n3 (str): Descripción de la cuenta.
    """
    with sqlite3.connect(ruta_BD) as conn:
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

def mostrar_datos_grupo():
    """
    Muestra todos los datos de la tabla GRUPO.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GRUPO")
        registros = cursor.fetchall()
    print("\nContenido de la tabla GRUPO (Nivel 1):")
    for registro in registros:
        print(registro)

def mostrar_datos_subgrupo():
    """
    Muestra todos los datos de la tabla SUBGRUPO.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT cod_2, desc_2 FROM SUBGRUPO")
        registros = cursor.fetchall()
    print("\nContenido de la tabla SUBGRUPO (Nivel 2):")
    for registro in registros:
        print(registro)

def mostrar_datos_cuentas():
    """
    Muestra todos los datos de la tabla CUENTAS.
    """
    with sqlite3.connect(ruta_BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT cod_3, desc_3 FROM CUENTAS")
        registros = cursor.fetchall()
    print("\nContenido de la tabla CUENTAS (Nivel 3):")
    for registro in registros:
        print(registro)

if __name__ == "__main__":
    # Crear las tablas
    crear_tabla_grupo()
    crear_tabla_subgrupo()
    crear_tabla_cuentas()

    # Insertar los datos iniciales en GRUPO (Nivel 1)
    insertar_datos_grupo("ACTIVO")
    insertar_datos_grupo("DEUDAS")
    insertar_datos_grupo("GASTOS")
    insertar_datos_grupo("INGRESOS")

    # Insertar datos en SUBGRUPO (Nivel 2)
    insertar_datos_subgrupo(1, "Bancos")
    insertar_datos_subgrupo(1, "Inversiones")
    insertar_datos_subgrupo(1, "Caja")
    insertar_datos_subgrupo(2, "Préstamos")
    insertar_datos_subgrupo(2, "Tarjetas Crédito")
    insertar_datos_subgrupo(2, "Proveedores")
    insertar_datos_subgrupo(3, "Sueldos")
    insertar_datos_subgrupo(3, "Alquiler")
    insertar_datos_subgrupo(3, "Suministros")
    insertar_datos_subgrupo(4, "Ventas")
    insertar_datos_subgrupo(4, "Servicios")
    insertar_datos_subgrupo(4, "Intereses")

    # Insertar datos en CUENTAS (Nivel 3)
    insertar_datos_cuenta(1, 1, "Cuenta Corriente")
    insertar_datos_cuenta(1, 1, "Cuenta Ahorros")
    insertar_datos_cuenta(1, 2, "Acciones")
    insertar_datos_cuenta(1, 2, "Bonos")
    insertar_datos_cuenta(2, 1, "Préstamo Hipotecario")
    insertar_datos_cuenta(2, 2, "Préstamo Automotriz")
    insertar_datos_cuenta(3, 2, "Salario Base")
    insertar_datos_cuenta(3, 3, "Bonificaciones")
    insertar_datos_cuenta(4, 1, "Ventas Netas")
    insertar_datos_cuenta(4, 3, "Devoluciones en Ventas")

    # Mostrar los datos
    mostrar_datos_grupo()
    mostrar_datos_subgrupo()
    mostrar_datos_cuentas()