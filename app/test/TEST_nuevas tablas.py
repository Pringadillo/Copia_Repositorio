

import sqlite3

def crear_tabla_GRUPO(ruta_BDapp):
    """
    Crea la tabla 'GRUPO' (Nivel 1) en la base de datos SQLite si no existe.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GRUPO (
                    grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desc_grupo TEXT NOT NULL UNIQUE CHECK (desc_grupo = UPPER(desc_grupo)),
                    tipo_grupo TEXT NOT NULL CHECK (tipo_grupo IN ('Balance', 'PyG'))
                )
            """)
            conn.commit()
        print("Tabla GRUPO (Nivel 1) creada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al conectar o crear la tabla GRUPO: {e}")
        raise

def crear_tabla_BALANCE(ruta_BDapp):
    """
    Crea la tabla 'BALANCE' (Nivel 1 para cuentas de Balance) en la base de datos SQLite si no existe.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS BALANCE (
                    balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desc_balance TEXT NOT NULL UNIQUE CHECK (desc_balance = UPPER(desc_balance))
                )
            """)
            conn.commit()
        print("Tabla BALANCE (Nivel 1) creada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al conectar o crear la tabla BALANCE: {e}")
        raise

def crear_tabla_PYG(ruta_BDapp):
    """
    Crea la tabla 'PYG' (Nivel 1 para cuentas de Pérdidas y Ganancias) en la base de datos SQLite si no existe.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PYG (
                    pyg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    desc_pyg TEXT NOT NULL UNIQUE CHECK (desc_pyg = UPPER(desc_pyg))
                )
            """)
            conn.commit()
        print("Tabla PYG (Nivel 1) creada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al conectar o crear la tabla PYG: {e}")
        raise


def crear_tabla_SUBGRUPO(ruta_BDapp):
    """
    Crea la tabla 'SUBGRUPO' (Nivel 2) en la base de datos SQLite si no existe.
    Establece la relación con la tabla GRUPO.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SUBGRUPO (
                    subgrupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grupo_id INTEGER NOT NULL,
                    cod_2 TEXT NOT NULL,
                    desc_subgrupo TEXT NOT NULL,
                    FOREIGN KEY (grupo_id) REFERENCES GRUPO (grupo_id),
                    UNIQUE (grupo_id, cod_2),
                    UNIQUE (grupo_id, desc_subgrupo)
                )
            """)
            conn.commit()
        print("Tabla SUBGRUPO (Nivel 2) creada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla SUBGRUPO: {e}")
        raise

def crear_tabla_CUENTAS(ruta_BDapp):
    """
    Crea la tabla 'CUENTAS' (Nivel 3) en la base de datos SQLite si no existe.
    Establece la relación con la tabla SUBGRUPO y asegura la coherencia
    con la estructura de datos jerárquica.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS CUENTAS (
                    grupo_id INTEGER NOT NULL,
                    subgrupo_id INTEGER NOT NULL,
                    cuentas_id INTEGER NOT NULL,
                    descripcion_n3 TEXT NOT NULL,
                    cod_3 TEXT NOT NULL UNIQUE,

                    PRIMARY KEY (grupo_id, subgrupo_id, cuentas_id),

                    FOREIGN KEY (grupo_id, subgrupo_id)
                        REFERENCES SUBGRUPO(grupo_id, subgrupo_id)
                )
            """)
            conn.commit()
        print(f"Tabla CUENTAS (Nivel 3) creada correctamente en {ruta_BDapp}.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla CUENTAS: {e}")
        raise


def crear_tabla_Diario(ruta_BDapp):
    """
    Crea la tabla DIARIO si no existe, con las columnas especificadas,
    incluyendo IDs con FOREIGN KEYs para la integridad y las nuevas columnas.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DIARIO (
                    id_diario INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    fechaValor TEXT NOT NULL, -- Formato esperado: 'DD/MM/AAAA'

                    -- Claves Foráneas para la estructura de Cuentas Contables (Balance)
                    Grupo_Balance INTEGER NOT NULL,
                    Subgrupo_Balance INTEGER NOT NULL,
                    Cuenta_Balance INTEGER NOT NULL,

                    -- Claves Foráneas para la estructura de Pérdidas y Ganancias (PyG)
                    -- NOTA: Estas FKs asumen la existencia de tablas PyG, CATEGORIAS, SUBCATEGORIAS
                    -- con las PRIMARY KEYs adecuadas.
                    Grupo_PyG INTEGER NOT NULL,
                    Categoria_PyG INTEGER NOT NULL,
                    Subcategoria_PyG INTEGER NOT NULL,

                    descripcionDiario TEXT,
                    importe REAL NOT NULL,

                    traspaso INTEGER DEFAULT 0, -- 0 (No) por defecto, 1 (Sí)
                    n_traspaso TEXT,           -- Número de traspaso, por defecto NULL
                    validado INTEGER DEFAULT 0, -- 0 (No) por defecto, 1 (Sí). Renombrado de 'Revisado'
                    conciliado INTEGER,         -- Número de conciliación
                    fecha_registro_asiento TEXT NOT NULL DEFAULT (date('now')), -- Fecha de registro del asiento

                    -- Definición de las FOREIGN KEYs para Balance
                    FOREIGN KEY (Grupo_Balance) REFERENCES GRUPO (grupo_id),
                    FOREIGN KEY (Grupo_Balance, Subgrupo_Balance) REFERENCES SUBGRUPO (grupo_id, subgrupo_id),
                    FOREIGN KEY (Grupo_Balance, Subgrupo_Balance, Cuenta_Balance) REFERENCES CUENTAS (grupo_id, subgrupo_id, cuentas_id),

                    -- Definición de las FOREIGN KEYs para PyG (asumiendo sus tablas y PKs)
                    FOREIGN KEY (Grupo_PyG) REFERENCES PyG (grupo_id),
                    FOREIGN KEY (Grupo_PyG, Categoria_PyG) REFERENCES CATEGORIAS (PyG_id, categoria_id),
                    FOREIGN KEY (Grupo_PyG, Categoria_PyG, Subcategoria_PyG) REFERENCES SUBCATEGORIAS (PyG_id, categoria_id, subcategoria_id)
                )
            ''')
            conn.commit()
        print(f"Tabla DIARIO creada/actualizada exitosamente en {ruta_BDapp} con la nueva estructura.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla DIARIO: {e}")
        raise
