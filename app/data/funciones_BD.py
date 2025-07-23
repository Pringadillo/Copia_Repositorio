import sqlite3
import flet as ft

from app import globals
from datetime import date



# ---------------------------------------- FUNCIONES DE CREAR BASE DE DATOS Y TABLAS ----------------------------------------
def crear_base_datos():
    conn = sqlite3.connect(ruta_BDapp)
    conn.commit()
    conn.close()

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

def crear_tabla_DIARIO(ruta_BDapp):
    """
    Crea la tabla DIARIO si no existe, con las columnas especificadas.
    Esta versión no incluye claves foráneas para simplificar el inicio desde cero,
    enfocándose solo en las columnas solicitadas.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DIARIO (
                    diario_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL, -- Formato esperado: 'DD/MM/AA'
                    grupo_balance TEXT NOT NULL,
                    subgrupo_balance TEXT NOT NULL,
                    cuenta_balance TEXT NOT NULL,
                    importe REAL NOT NULL, -- REAL para números con decimales y negativos
                    traspaso INTEGER DEFAULT 0, -- 0 para 'no', 1 para 'sí'
                    n_traspaso INTEGER, -- Números positivos sin decimales (NULL si no hay traspaso)
                    grupo_PyG TEXT NOT NULL,
                    subgrupo_PyG TEXT NOT NULL,
                    cuenta_PyG TEXT NOT NULL,
                    auditado INTEGER DEFAULT 0, -- 0 para 'no', 1 para 'sí'
                    fecha_registro TEXT NOT NULL DEFAULT (date('now')) -- Fecha actual por defecto
                )
            ''')
            conn.commit()
        print(f"Tabla DIARIO creada/actualizada exitosamente en {ruta_BDapp}.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla DIARIO: {e}")
        raise

# ---------------------------------------- FUNCIONES DE INSERTAR DATOS ----------------------------------------

def insertar_datos_grupo(ruta_BDapp, desc_grupo, tipo_grupo): # ¡Cambiado aquí!
    """
    Inserta un nuevo grupo en la tabla GRUPO de la base de datos,
    asegurándose de no insertar descripciones de grupo duplicadas.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        desc_grupo (str): La descripción del grupo (se convertirá a mayúsculas
                          antes de la inserción y la comprobación).
        tipo_grupo (str): El tipo de grupo ('Balance' o 'PyG'). -- ¡Cambiado aquí!
    """
    desc_grupo_upper = desc_grupo.upper()

    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()

            # 1. Comprobar si el grupo ya existe
            cursor.execute("SELECT COUNT(*) FROM GRUPO WHERE desc_grupo = ?", (desc_grupo_upper,))
            if cursor.fetchone()[0] > 0:
                print(f"Advertencia: El grupo '{desc_grupo_upper}' ya existe en la base de datos. No se insertará duplicado.")
                return

            # 2. Si no existe, proceder con la inserción
            cursor.execute("""
                INSERT INTO GRUPO (desc_grupo, tipo_grupo) VALUES (?, ?) 
            """, (desc_grupo_upper, tipo_grupo))
            conn.commit()
            print(f"Insertado en GRUPO (Nivel 1): desc_grupo='{desc_grupo_upper}', tipo_grupo='{tipo_grupo}'") # ¡Cambiado aquí!

    except sqlite3.IntegrityError as e:
        print(f"Error de integridad al insertar en GRUPO (Nivel 1): {e}")
        raise
    except sqlite3.Error as e:
        print(f"Error general de SQLite al insertar en GRUPO (Nivel 1): {e}")
        raise

def insertar_datos_subgrupo(ruta_BDapp: str, grupo_id: int, cod_2_input: str, desc_subgrupo_input: str):
    """
    Inserta un nuevo subgrupo en la tabla SUBGRUPO de la base de datos.
    Asegura que el cod_2 sea único y que la combinación (grupo_id, desc_subgrupo)
    también sea única.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        grupo_id (int): El ID del grupo padre al que pertenece este subgrupo.
        cod_2_input (str): El código único de 2do nivel para el subgrupo (ej: "430").
        desc_subgrupo_input (str): La descripción del subgrupo (ej: "CLIENTES POR VENTAS").
    """
    # Convertir a mayúsculas si es necesario, asegurando consistencia con el CHECK de GRUPO
    # Aunque SUBGRUPO no tiene un CHECK de UPPER, es buena práctica si quieres consistencia
    desc_subgrupo_upper = desc_subgrupo_input.upper()

    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()

            # --- COMPROBACIONES PREVIAS PARA EVITAR ERRORES DE INTEGRIDAD ---
            # Estas comprobaciones son redundantes si las restricciones UNIQUE y FOREIGN KEY

            # 1. Verificar si el grupo_id principal existe
            cursor.execute("SELECT COUNT(*) FROM GRUPO WHERE grupo_id = ?", (grupo_id,))
            if cursor.fetchone()[0] == 0:
                print(f"Error: El grupo_id '{grupo_id}' no existe en la tabla GRUPO. No se puede insertar el subgrupo '{desc_subgrupo_upper}'.")
                return # Salir de la función si el grupo padre no existe

            # 2. Comprobar si hay cod_2 duplicado para el MISMO grupo_id
            cursor.execute("SELECT COUNT(*) FROM SUBGRUPO WHERE grupo_id = ? AND cod_2 = ?", (grupo_id, cod_2_input))
            if cursor.fetchone()[0] > 0:
                print(f"Advertencia: El cod_2 '{cod_2_input}' ya existe para el grupo_id '{grupo_id}'. No se insertará duplicado para '{desc_subgrupo_upper}'.")
                return # Salir si el cod_2 ya existe para el mismo grupo_id

            # 3. Verificar si hay una combinación duplicada (grupo_id, desc_subgrupo)
            cursor.execute("""
                SELECT COUNT(*) FROM SUBGRUPO
                WHERE grupo_id = ? AND desc_subgrupo = ?
            """, (grupo_id, desc_subgrupo_upper))
            if cursor.fetchone()[0] > 0:
                print(f"Advertencia: Ya existe un subgrupo con la descripción '{desc_subgrupo_upper}' para el grupo_id '{grupo_id}'. No se insertará duplicado.")
                return # Salir si la combinación ya existe

            # --- Si todas las comprobaciones pasan, proceder con la inserción ---
            cursor.execute("""
                INSERT INTO SUBGRUPO (grupo_id, cod_2, desc_subgrupo)
                VALUES (?, ?, ?)
            """, (grupo_id, cod_2_input, desc_subgrupo_upper))
            conn.commit()

            # Obtener el subgrupo_id generado automáticamente
            new_subgrupo_id = cursor.lastrowid
            print(f"Insertado en SUBGRUPO (Nivel 2): ID={new_subgrupo_id}, Grupo ID={grupo_id}, Código='{cod_2_input}', Descripción='{desc_subgrupo_upper}'")

    except sqlite3.IntegrityError as e:
        # Este 'catch-all' es para cualquier otra violación de integridad que las comprobaciones previas no cubran
        print(f"Error de integridad al insertar en SUBGRUPO (Nivel 2): {e}")
        raise # Propagar el error de integridad

    except sqlite3.Error as e:
        print(f"Error general de SQLite al insertar en SUBGRUPO (Nivel 2): {e}")
        raise # Propagar cualquier otro error de SQLite

def insertar_datos_cuenta(ruta_BDapp: str, grupo_id: int, cod_2_subgrupo_input: str, descripcion_n3_input: str):
    """
    Inserta una nueva cuenta (Nivel 3) en la tabla CUENTAS de la base de datos.
    Encuentra el subgrupo_id a partir de grupo_id y cod_2_subgrupo_input (ya que subgrupo_id es AUTOINCREMENT).
    Genera automáticamente cuentas_id y cod_3 con formato X.YY.ZZ.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        grupo_id (int): El ID del grupo padre al que pertenece esta cuenta.
        cod_2_subgrupo_input (str): El código de 2do nivel (cod_2) del subgrupo padre.
                                    Este es el identificador que usaremos para encontrar el subgrupo.
        descripcion_n3_input (str): La descripción específica de esta cuenta (ej: "CAJA").
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()

            # 1. Obtener subgrupo_id, cod_2 y desc_subgrupo del subgrupo padre
            # *** CAMBIO CLAVE AQUÍ: Buscamos por cod_2_subgrupo_input en lugar de subgrupo_id ***
            cursor.execute("""
                SELECT subgrupo_id, cod_2, desc_subgrupo
                FROM SUBGRUPO
                WHERE grupo_id = ? AND cod_2 = ?
            """, (grupo_id, cod_2_subgrupo_input))
            resultado_subgrupo = cursor.fetchone()

            if resultado_subgrupo is None:
                # El error ahora indica que no se encontró el subgrupo por cod_2
                print(f"Error: No se encontró subgrupo con grupo_id={grupo_id} y cod_2='{cod_2_subgrupo_input}'. No se puede insertar la cuenta.")
                return

            # Extraemos los valores. subgrupo_id_encontrado es el ID REAL auto-generado.
            subgrupo_id_encontrado = resultado_subgrupo[0]
            cod_2_subgrupo = resultado_subgrupo[1] # Este es el mismo que cod_2_subgrupo_input
            desc_subgrupo_padre = resultado_subgrupo[2]

            # 2. Calcular el siguiente cuentas_id para este grupo_id y el subgrupo_id_encontrado
            # Usamos el subgrupo_id REAL que acabamos de encontrar.
            cursor.execute("""
                SELECT COALESCE(MAX(cuentas_id), 0) + 1
                FROM CUENTAS
                WHERE grupo_id = ? AND subgrupo_id = ?
            """, (grupo_id, subgrupo_id_encontrado))
            cuentas_id = cursor.fetchone()[0]

            # 3. Construir cod_3 y la descripción completa
            # Formateamos cod_2_subgrupo y cuentas_id a dos dígitos con ceros iniciales (YY.ZZ)
            cod_2_formateado = f"{int(cod_2_subgrupo):02d}"
            cuentas_id_formateado = f"{cuentas_id:02d}"

            # El formato final del código es X.YY.ZZ, asegurando unicidad global.
            cod_3 = f"{grupo_id}.{cod_2_formateado}.{cuentas_id_formateado}"
            
            descripcion_n3_para_db = descripcion_n3_input.upper()
            desc_completa_cuenta = f"{desc_subgrupo_padre} - {descripcion_n3_para_db}"

            # --- INSERTAR EN LA TABLA CUENTAS ---
            # Usamos el subgrupo_id_encontrado y el cuentas_id calculado
            cursor.execute("""
                INSERT INTO CUENTAS (grupo_id, subgrupo_id, cuentas_id, descripcion_n3, cod_3)
                VALUES (?, ?, ?, ?, ?)
            """, (grupo_id, subgrupo_id_encontrado, cuentas_id, descripcion_n3_para_db, cod_3))
            
            conn.commit()

            print(f"Insertado en CUENTAS (Nivel 3): "
                  f"Grupo ID={grupo_id}, Subgrupo ID={subgrupo_id_encontrado}, " # Reportamos el ID real
                  f"Cuentas ID={cuentas_id}, Descripción N3='{descripcion_n3_para_db}', "
                  f"Código Cuenta='{cod_3}', Descripción Completa Generada='{desc_completa_cuenta}'")

    except sqlite3.IntegrityError as e:
        print(f"Error de integridad al insertar en CUENTAS (Nivel 3): {e}")
        raise

    except sqlite3.Error as e:
        print(f"Error general de SQLite al insertar en CUENTAS (Nivel 3): {e}")
        raise

def insertar_datos_diario(
    ruta_BDapp: str,
    fecha: str,
    grupo_balance: str,
    subgrupo_balance: str,
    cuenta_balance: str,
    importe: float,
    grupo_PyG: str, # Parámetro obligatorio movido antes de los opcionales
    subgrupo_PyG: str, # Parámetro obligatorio movido antes de los opcionales
    cuenta_PyG: str, # Parámetro obligatorio movido antes de los opcionales
    traspaso: int = 0, # 0 para 'no', 1 para 'sí'
    n_traspaso: int = None, # NULL por defecto
    auditado: int = 0 # 0 para 'no', 1 para 'sí'
):
    """
    Inserta un nuevo registro en la tabla DIARIO.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        fecha (str): La fecha del asiento (formato 'DD/MM/AA').
        grupo_balance (str): El nombre del grupo de balance.
        subgrupo_balance (str): El nombre del subgrupo de balance.
        cuenta_balance (str): El nombre de la cuenta de balance.
        importe (float): El importe del asiento (acepta decimales y negativos).
        traspaso (int): Indicador de traspaso (0=No, 1=Sí). Por defecto 0.
        n_traspaso (int): Número de traspaso (opcional). Por defecto None.
        grupo_PyG (str): El nombre del grupo de Pérdidas y Ganancias.
        subgrupo_PyG (str): El nombre del subgrupo de Pérdidas y Ganancias.
        cuenta_PyG (str): El nombre de la cuenta de Pérdidas y Ganancias.
        auditado (int): Indicador de auditoría (0=No, 1=Sí). Por defecto 0.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO DIARIO (
                    fecha, grupo_balance, subgrupo_balance, cuenta_balance,
                    importe, traspaso, n_traspaso,
                    grupo_PyG, subgrupo_PyG, cuenta_PyG, auditado, fecha_registro
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    fecha, grupo_balance, subgrupo_balance, cuenta_balance,
                    importe, traspaso, n_traspaso,
                    grupo_PyG, subgrupo_PyG, cuenta_PyG, auditado,
                    datetime.date.today().strftime('%Y-%m-%d') # Formato YYYY-MM-DD para la fecha de registro
                )
            )
            conn.commit()
        print(f"Registro insertado exitosamente en DIARIO.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos en la tabla DIARIO: {e}")
        raise

# ---------------------------------------- FUNCIONES OBTENER DATOS ----------------------------------------

def obtener_datos_grupo(ruta_BDapp):
    """
    Obtiene todos los datos de la tabla GRUPO como una lista de diccionarios,
    donde cada diccionario representa una fila y las claves son los nombres de las columnas.
    Devuelve una lista, no la imprime directamente.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.

    Returns:
        list[dict]: Una lista donde cada diccionario representa una fila de la tabla GRUPO.
                    Retorna una lista vacía si ocurre un error o no hay datos.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            # Configura el cursor para que devuelva filas como diccionarios
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GRUPO")
            registros = cursor.fetchall()

            # Convertir sqlite3.Row a diccionarios estándar
            return [dict(row) for row in registros]

    except sqlite3.Error as e:
        print(f"Error al obtener datos de GRUPO: {e}")
        return []

def obtener_datos_subgrupo(ruta_BDapp: str, grupo_id: int = None) -> list[dict]:
    """
    Obtiene todos los datos de la tabla SUBGRUPO (o para un grupo específico)
    como una lista de diccionarios.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para el que se desean obtener
                                   los subgrupos. Si es None, obtiene todos los subgrupos.
                                   Por defecto es None.

    Returns:
        list[dict]: Una lista donde cada diccionario representa una fila de la tabla SUBGRUPO.
                    Retorna una lista vacía en caso de error o si no se encuentran subgrupos.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
            cursor = conn.cursor()

            query = "SELECT subgrupo_id, grupo_id, cod_2, desc_subgrupo FROM SUBGRUPO"
            params = ()

            if grupo_id is not None:
                query += " WHERE grupo_id = ?"
                params = (grupo_id,)

            query += """
                     ORDER BY
                         grupo_id,
                         CAST(SUBSTR(cod_2, 1, INSTR(cod_2, '.') - 1) AS INTEGER), -- Parte antes del punto (el 'x' en 'x.xx')
                         CAST(SUBSTR(cod_2, INSTR(cod_2, '.') + 1) AS INTEGER)    -- Parte después del punto (el 'xx' en 'x.xx')
                     """
            
            cursor.execute(query, params)
            registros = cursor.fetchall()

            # Convertir sqlite3.Row a diccionarios estándar para mayor compatibilidad
            return [dict(row) for row in registros]

    except sqlite3.Error as e:
        print(f"Error al obtener datos de SUBGRUPO (Grupo ID: {grupo_id if grupo_id is not None else 'Todos'}): {e}")
        return []

def obtener_datos_cuentas(ruta_BDapp: str, grupo_id: int = None, subgrupo_id: int = None) -> list[dict]:
    """
    Obtiene datos de la tabla CUENTAS, con opciones para filtrar por grupo_id y/o subgrupo_id.
    Devuelve las filas como diccionarios para facilitar el acceso por nombre de columna.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para filtrar. Si es None, no filtra por grupo.
                                   Por defecto es None.
        subgrupo_id (int, optional): El ID del subgrupo para filtrar. Si es None, no filtra por subgrupo.
                                      Por defecto es None.

    Returns:
        list[dict]: Una lista donde cada diccionario representa una fila de la tabla CUENTAS.
                    Retorna una lista vacía en caso de error o si no se encuentran cuentas.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre (ej. row['cod_3'])
            cursor = conn.cursor()

            # Seleccionamos todas las columnas relevantes de la tabla CUENTAS
            query = "SELECT grupo_id, subgrupo_id, cuentas_id, descripcion_n3, cod_3 FROM CUENTAS"
            conditions = []
            params = []

            # Construimos la cláusula WHERE dinámicamente si se proporcionan filtros
            if grupo_id is not None:
                conditions.append("grupo_id = ?")
                params.append(grupo_id)
            
            if subgrupo_id is not None:
                conditions.append("subgrupo_id = ?")
                params.append(subgrupo_id)

            if conditions: # Si hay alguna condición, añadir la cláusula WHERE
                query += " WHERE " + " AND ".join(conditions)

            # Ordenar para una presentación lógica: primero por grupo_id, luego subgrupo_id (parte YY),
            # y finalmente por cuentas_id (parte ZZ), asegurando el orden numérico correcto (X.YY.ZZ).
            query += """
                     ORDER BY
                         grupo_id ASC,
                         CAST(SUBSTR(cod_3, INSTR(cod_3, '.') + 1, 2) AS INTEGER) ASC,   -- Parte YY de X.YY.ZZ (asumiendo 2 dígitos)
                         CAST(SUBSTR(cod_3, LENGTH(cod_3) - 1) AS INTEGER) ASC           -- Parte ZZ de X.YY.ZZ (asumiendo 2 dígitos al final)
                     """
            
            # Ejecutamos la consulta con los parámetros
            cursor.execute(query, tuple(params))

            registros = cursor.fetchall()
            # Convertimos los objetos sqlite3.Row a diccionarios estándar
            return [dict(row) for row in registros]

    except sqlite3.Error as e:
        print(f"Error al obtener datos de CUENTAS: {e}")
        return []

def mostrar_datos_cuentas(ruta_BDapp: str, grupo_id: int = None, subgrupo_id: int = None):
    """
    Muestra el contenido de la tabla CUENTAS (Nivel 3) en la consola.
    Puede filtrar por grupo_id y/o subgrupo_id si se proporcionan.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para el que se desean mostrar
                                   las cuentas. Si es None, muestra todas.
        subgrupo_id (int, optional): El ID del subgrupo para el que se desean mostrar
                                      las cuentas. Si es None, muestra todas dentro del grupo.
    """
    # Determina el encabezado de la sección de datos
    if grupo_id is None and subgrupo_id is None:
        print("\n--- Contenido de la tabla CUENTAS (Nivel 3) ---")
    elif grupo_id is not None and subgrupo_id is None:
        print(f"\n--- Contenido de la tabla CUENTAS (Nivel 3) para Grupo ID: {grupo_id} ---")
    else: # Ambos grupo_id y subgrupo_id están presentes
        print(f"\n--- Contenido de la tabla CUENTAS (Nivel 3) para Grupo ID: {grupo_id}, Subgrupo ID: {subgrupo_id} ---")

    # Obtiene los datos usando la función obtener_datos_cuentas
    registros = obtener_datos_cuentas(ruta_BDapp, grupo_id, subgrupo_id)

    # Verifica si se encontraron registros
    if not registros:
        print("No hay datos de cuentas que mostrar o hubo un error al obtenerlos.")
        print("-" * 80) # Separador visual
        return

    # Imprimir encabezados de columna formateados
    # Ajusta los anchos según el tamaño máximo esperado de tus datos
    print(f"{'Grupo ID':<10} {'Subgrupo ID':<13} {'Cuenta ID':<11} {'Código Cuenta':<15} {'Descripción Cuenta':<35}")
    print("-" * 85) # Separador visual

    # Itera sobre cada registro e imprime sus valores formateados
    for registro in registros:
        # Accede a los valores por el nombre de la columna
        print(f"{registro.get('grupo_id', ''):<10} "
              f"{registro.get('subgrupo_id', ''):<13} "
              f"{registro.get('cuentas_id', ''):<11} "
              f"{registro.get('cod_3', ''):<15} "
              f"{registro.get('descripcion_n3', ''):<35}")
    print("-" * 85) # Separador visual final

def mostrar_datos_DIARIO(ruta_BDapp):
    """
    Lee y muestra todos los registros de la tabla 'DIARIO'.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DIARIO")
            rows = cursor.fetchall()

            if rows:
                print("\n--- Contenido de la tabla DIARIO ---")
                # Imprimir encabezados de columna
                # Esto asume que el orden de las columnas es el mismo que en la creación de la tabla
                print(
                    f"{'diario_id':<10} | {'fecha':<10} | {'grupo_balance':<15} | "
                    f"{'subgrupo_balance':<18} | {'cuenta_balance':<15} | {'importe':<10} | "
                    f"{'traspaso':<8} | {'n_traspaso':<10} | {'grupo_PyG':<10} | "
                    f"{'subgrupo_PyG':<13} | {'cuenta_PyG':<10} | {'auditado':<8} | "
                    f"{'fecha_registro':<15}"
                )
                print("-" * 170) # Línea separadora

                for row in rows:
                    # Imprimir cada fila formateada
                    print(
                        f"{row[0]:<10} | {row[1]:<10} | {row[2]:<15} | "
                        f"{row[3]:<18} | {row[4]:<15} | {row[5]:<10.2f} | " # Formato para 2 decimales
                        f"{'Sí' if row[6] == 1 else 'No':<8} | {str(row[7] if row[7] is not None else 'N/A'):<10} | "
                        f"{row[8]:<10} | {row[9]:<13} | {row[10]:<10} | "
                        f"{'Sí' if row[11] == 1 else 'No':<8} | {row[12]:<15}"
                    )
            else:
                print("\nLa tabla DIARIO está vacía.")
        return rows
    except sqlite3.Error as e:
        print(f"Error al leer la tabla DIARIO: {e}")
        return None

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

def mostrar_datos_subgrupo(ruta_BDapp: str, grupo_id: int = None):
    """
    Muestra el contenido de la tabla SUBGRUPO (Nivel 2) en la consola.
    Puede filtrar por grupo_id si se proporciona.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para el que se desean mostrar
                                   los subgrupos. Si es None, muestra todos.
    """
    if grupo_id is None:
        print("\n--- Contenido de la tabla SUBGRUPO (Nivel 2) ---")
    else:
        print(f"\n--- Contenido de la tabla SUBGRUPO (Nivel 2) para Grupo ID: {grupo_id} ---")

    registros = obtener_datos_subgrupo(ruta_BDapp, grupo_id)

    if not registros:
        print("No hay datos de subgrupos que mostrar o hubo un error al obtenerlos.")
        print("-" * 50)
        return

    # Obtener los nombres de las columnas de la primera fila (ya que son diccionarios)
    # y formatear para la cabecera
    # Si quieres una cabecera específica, puedes definirla manualmente:
    # headers = ["ID Subgrupo", "ID Grupo", "Código", "Descripción del Subgrupo"]

    # Imprimir encabezados de columna formateados
    # Ajusta los anchos según el tamaño máximo esperado de tus datos
    print(f"{'ID Subgrupo':<13} {'ID Grupo':<10} {'Código':<10} {'Descripción del Subgrupo':<30}")
    print("-" * 75) # Separador visual

    for registro in registros:
        print(f"{registro.get('subgrupo_id', ''):<13} "
              f"{registro.get('grupo_id', ''):<10} "
              f"{registro.get('cod_2', ''):<10} "
              f"{registro.get('desc_subgrupo', ''):<30}")
    print("-" * 75) # Separador visual final

def obtener_grupos_por_tipo(ruta_BDapp, tipo):
    """
    Obtiene los grupos de la tabla GRUPO según el tipo especificado ('Balance' o 'PyG').
    Devuelve una lista de tuplas, donde cada tupla contiene (grupo_id, desc_grupo).

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        tipo (str): El tipo de grupo a filtrar ('Balance' o 'PyG').

    Returns:
        list: Una lista de tuplas, donde cada tupla es (grupo_id, desc_grupo).
              Devuelve una lista vacía ([]) si no se encuentran resultados o si hay un error.
    """
    resultados = []
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT grupo_id, desc_grupo FROM GRUPO WHERE tipo_grupo = ?", (tipo,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    resultados.append((row[0], row[1])) # Añade la tupla (id, descripcion) directamente
            # No se imprime nada en la consola si hay o no resultados
        return resultados
    except sqlite3.Error as e:
        # Se sigue imprimiendo el error en caso de fallo de la base de datos
        print(f"Error al leer la tabla GRUPO por tipo: {e}")
        return [] # Devuelve una lista vacía en caso de error


def mostrar_datos_cuentas(ruta_BDapp: str, grupo_id: int = None, subgrupo_id: int = None):
    """
    Muestra el contenido de la tabla CUENTAS (Nivel 3) en la consola.
    Puede filtrar por grupo_id y/o subgrupo_id si se proporcionan.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para el que se desean mostrar
                                   las cuentas. Si es None, muestra todas.
        subgrupo_id (int, optional): El ID del subgrupo para el que se desean mostrar
                                      las cuentas. Si es None, muestra todas dentro del grupo.
    """
    # Determina el encabezado de la sección de datos
    if grupo_id is None and subgrupo_id is None:
        print("\n--- Contenido de la tabla CUENTAS (Nivel 3) ---")
    elif grupo_id is not None and subgrupo_id is None:
        print(f"\n--- Contenido de la tabla CUENTAS (Nivel 3) para Grupo ID: {grupo_id} ---")
    else: # Ambos grupo_id y subgrupo_id están presentes
        print(f"\n--- Contenido de la tabla CUENTAS (Nivel 3) para Grupo ID: {grupo_id}, Subgrupo ID: {subgrupo_id} ---")

    # Obtiene los datos usando la función obtener_datos_cuentas
    registros = obtener_datos_cuentas(ruta_BDapp, grupo_id, subgrupo_id)

    # Verifica si se encontraron registros
    if not registros:
        print("No hay datos de cuentas que mostrar o hubo un error al obtenerlos.")
        print("-" * 80) # Separador visual
        return

    # Imprimir encabezados de columna formateados
    # Ajusta los anchos según el tamaño máximo esperado de tus datos
    print(f"{'Grupo ID':<10} {'Subgrupo ID':<13} {'Cuenta ID':<11} {'Código Cuenta':<15} {'Descripción Cuenta':<35}")
    print("-" * 85) # Separador visual

    # Itera sobre cada registro e imprime sus valores formateados
    for registro in registros:
        # Accede a los valores por el nombre de la columna
        print(f"{registro.get('grupo_id', ''):<10} "
              f"{registro.get('subgrupo_id', ''):<13} "
              f"{registro.get('cuentas_id', ''):<11} "
              f"{registro.get('cod_3', ''):<15} "
              f"{registro.get('descripcion_n3', ''):<35}")
    print("-" * 85) # Separador visual final 


def mostrar_saldoInicio_cuentas(ruta_BDapp):
    """
    Muestra los campos cod_3, desc_3, Saldo_inicial y Fecha_Inicio
    de todos los registros en la tabla CUENTAS.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_3, desc_3, Saldo_inicial, Fecha_Inicio FROM CUENTAS")
            registros = cursor.fetchall()
        print("\nContenido de la tabla CUENTAS (Nivel 3):")
        if registros:
            print(f"{'Código':<10} | {'Descripción':<40} | {'Saldo Inicial':<15} | {'Fecha Inicio'}")
            print("-" * 80)
            for registro in registros:
                cod_3, desc_3, saldo_inicial, fecha_inicio = registro
                print(f"{cod_3:<10} | {desc_3:<40} | {saldo_inicial:<15.2f} | {fecha_inicio}")
        else:
            print("La tabla CUENTAS está vacía.")
    except sqlite3.Error as e:
        print(f"Error al mostrar datos de CUENTAS: {e}")
        raise
    finally:
        if conn:
            conn.close()

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


def mostrar_cuentas_por_grupo_flet(ruta_BDapp: str, grupo_id_buscado: int) -> list[ft.Control]:
    """
    Muestra de forma jerárquica los subgrupos (Nivel 2) y cuentas (Nivel 3)
    para un grupo_id específico, formateado para Flet.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        grupo_id_buscado (int): El ID del grupo a buscar.

    Returns:
        list[ft.Control]: Una lista de controles Flet (ft.Text, ft.Divider) que representan
                          la jerarquía de subgrupos y cuentas.
    """
    formatted_controls = []
    
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn: # Usa 'with' para asegurar que la conexión se cierre automáticamente
            conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
            cursor = conn.cursor()

            # Opcional: Obtener la descripción del GRUPO principal para mostrarla al inicio
            # Asegúrate de que el nombre de la columna 'desc_grupo' coincide con tu esquema
            cursor.execute("SELECT desc_grupo FROM GRUPO WHERE grupo_id = ?", (grupo_id_buscado,))
            grupo_data = cursor.fetchone()

            if grupo_data:
                formatted_controls.append(
                    ft.Text(f"{str(grupo_id_buscado).zfill(2)} {grupo_data['desc_grupo']}", # Acceso por nombre
                            size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
                )
                formatted_controls.append(ft.Divider()) # Separador visual
            else:
                formatted_controls.append(ft.Text(f"¡Oops! No se encontró el Grupo ID: {grupo_id_buscado}",
                                                 color=ft.Colors.RED_500, size=16))
                return formatted_controls # Si no hay grupo, salimos temprano.

            # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
            cursor.execute("""
                SELECT
                    S.subgrupo_id,
                    S.cod_2,
                    S.descripcion_subgrupo
                FROM
                    SUBGRUPO S
                WHERE
                    S.grupo_id = ?
                ORDER BY
                    S.cod_2 -- Es más común ordenar por el código para jerarquía
            """, (grupo_id_buscado,))
            subgrupos = cursor.fetchall()

            if not subgrupos:
                formatted_controls.append(
                    ft.Text(f"   No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.",
                            size=14, color=ft.colors.GREY_600)
                )
                # No retornamos aquí, para que el divisor final se añada si el grupo principal existe.

            # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
            for subgrupo in subgrupos:
                # Acceso por nombre de columna (gracias a conn.row_factory)
                subgrupo_id = subgrupo['subgrupo_id']
                cod_subgrupo_completo = subgrupo['cod_2']
                descripcion_subgrupo = subgrupo['descripcion_subgrupo']

                # Formato para el título del subgrupo (Nivel 2)
                formatted_controls.append(
                    ft.Text(f"  {cod_subgrupo_completo} {descripcion_subgrupo}",
                            size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700)
                )

                # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
                cursor.execute("""
                    SELECT
                        C.nivel3_id,
                        C.descripcion_n3,
                        C.cod_3
                    FROM
                        CUENTAS C
                    WHERE
                        C.grupo_id = ? AND C.subgrupo_id = ?
                    ORDER BY
                        C.cod_3 -- Es más común ordenar por el código para jerarquía
                """, (grupo_id_buscado, subgrupo_id))
                cuentas_nivel3 = cursor.fetchall()

                if not cuentas_nivel3:
                    formatted_controls.append(
                        ft.Text(f"        No hay cuentas asociadas al subgrupo {cod_subgrupo_completo}.",
                                size=14, color=ft.Colors.GREY_500)
                    )

                # 3. Añadir las cuentas de Nivel 3 con su formato
                for cuenta_n3 in cuentas_nivel3:
                    # Acceso por nombre de columna
                    # nivel3_id = cuenta_n3['nivel3_id'] # No usado en el formato actual
                    descripcion_n3 = cuenta_n3['descripcion_n3']
                    cod_full_n3 = cuenta_n3['cod_3']

                    # Formato para la cuenta (Nivel 3)
                    formatted_controls.append(
                        ft.Text(f"    {cod_full_n3} {descripcion_n3}",
                                size=14, color=ft.Colors.BLUE_GREY_500)
                    )
            
            # Un divisor final para separar la información de un grupo si hay más elementos después.
            formatted_controls.append(ft.Divider()) 

    except sqlite3.Error as e:
        formatted_controls.append(
            ft.Text(f"Error de base de datos al mostrar cuentas: {e}",
                    color=ft.Colors.RED_500, size=16)
        )
    # Ya no se necesita un bloque 'finally' explícito para cerrar 'conn' 
    # porque 'with conn:' se encarga de ello.
    return formatted_controls

def mostrar_cuentas_por_grupo(ruta_BDapp: str, grupo_id_buscado: int):
    """
    Muestra de forma jerárquica los subgrupos (nivel 2) y cuentas (nivel 3)
    para un grupo_id específico en la consola.

    Formato de salida esperado:
    01 Título del Grupo Principal
    ---
      XX Título del Subgrupo (Ej: 01 Activo Corriente)
          YY Descripción de la Cuenta (Ej: 01 Caja y Bancos)
          ZZ Descripción de la Cuenta (Ej: 02 Inversiones Temporales)
      XX Título del Subgrupo (Ej: 02 Activo No Corriente)
          YY Descripción de la Cuenta (Ej: 01 Inmuebles)
    ---
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn: # Asegura que la conexión se cierre automáticamente
            conn.row_factory = sqlite3.Row # Acceso a columnas por nombre
            cursor = conn.cursor()

            # 0. Obtener y mostrar la descripción del GRUPO principal
            cursor.execute("SELECT desc_grupo FROM GRUPO WHERE grupo_id = ?", (grupo_id_buscado,))
            grupo_data = cursor.fetchone()

            if grupo_data:
                print(f"\n--- Cuentas para el Grupo: {str(grupo_id_buscado).zfill(2)} {grupo_data['desc_grupo']} ---")
                print("-" * 50)
            else:
                print(f"Error: No se encontró el Grupo ID: {grupo_id_buscado} en la base de datos.")
                return # Si no hay grupo, no tiene sentido continuar.

            # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
            # Ahora unimos con la tabla SUBGRUPO para obtener los datos correctos del subgrupo.
            cursor.execute("""
                SELECT
                    S.subgrupo_id,
                    S.cod_2,
                    S.descripcion_subgrupo
                FROM
                    SUBGRUPO S
                WHERE
                    S.grupo_id = ?
                ORDER BY
                    S.cod_2 -- Ordenar por el código para una jerarquía numérica
            """, (grupo_id_buscado,))
            subgrupos = cursor.fetchall()

            if not subgrupos:
                print(f"  No se encontraron subgrupos asociados al Grupo '{grupo_data['desc_grupo']}'.")
                print("-" * 50) # Cierre del separador
                return

            # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
            for subgrupo in subgrupos:
                # Acceso por nombre de columna
                subgrupo_id = subgrupo['subgrupo_id']
                cod_subgrupo = subgrupo['cod_2']
                desc_subgrupo = subgrupo['descripcion_subgrupo']

                # Formato para el título del subgrupo (Nivel 2)
                print(f"  {cod_subgrupo} {desc_subgrupo}")

                # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
                cursor.execute("""
                    SELECT
                        C.cod_3,
                        C.descripcion_n3
                    FROM
                        CUENTAS C
                    WHERE
                        C.grupo_id = ? AND C.subgrupo_id = ?
                    ORDER BY
                        C.cod_3 -- Ordenar por el código para una jerarquía numérica
                """, (grupo_id_buscado, subgrupo_id))
                cuentas_nivel3 = cursor.fetchall()

                if not cuentas_nivel3:
                    print(f"        No hay cuentas (nivel 3) para el subgrupo '{cod_subgrupo} {desc_subgrupo}'.")

                # 3. Imprimir las cuentas de Nivel 3 con su formato
                for cuenta_n3 in cuentas_nivel3:
                    # Acceso por nombre de columna
                    cod_full_n3 = cuenta_n3['cod_3']
                    desc_n3 = cuenta_n3['descripcion_n3']

                    # Formato para las cuentas de nivel 3 (con sangría)
                    print(f"        {cod_full_n3} {desc_n3}")
            
            print("-" * 50) # Cierre del separador

    except sqlite3.Error as e:
        print(f"Error de base de datos al mostrar cuentas por grupo: {e}")
        # En una función de "mostrar", a menudo se prefiere imprimir el error y no lanzar.
        # Si se necesita que el error se propague, descomentar 'raise'.
        # raise

def mostrar_cuentas_por_grupo2(ruta_BDapp, grupo_id_buscado):
    """
    Muestra de forma jerárquica los subgrupos (nivel 2) y cuentas (nivel 3)
    para un grupo_id específico, siguiendo el formato:
    01 Titulo (Subgrupo)
        01 Descripción (Cuenta Nivel 3)
        02 Descripción (Cuenta Nivel 3)
    02 Titulo (Subgrupo)
        01 Descripción (Cuenta Nivel 3)
    """
    conn = None # Inicializar conn a None para asegurar que se cierre en caso de error
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
        # Seleccionamos directamente 'descripcion_subgrupo' de la tabla SUBGRUPO para evitar el prefijo del grupo.
        cursor.execute("""
            SELECT
                S.subgrupo_id,
                S.cod_2,
                S.descripcion_subgrupo
            FROM
                SUBGRUPO S
            WHERE
                S.grupo_id = ?
            ORDER BY
                S.subgrupo_id
        """, (grupo_id_buscado,))
        subgrupos = cursor.fetchall()

        if not subgrupos:
            print(f"No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.")
            return

        # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
        for i, subgrupo in enumerate(subgrupos):
            subgrupo_id = subgrupo[0]
            cod_subgrupo = subgrupo[1]
            # Usamos la descripción del subgrupo sin el prefijo del grupo
            descripcion_subgrupo_limpia = subgrupo[2] 

            # Formato para el título del subgrupo (Nivel 2)
            print(f"{i + 1:02d} {descripcion_subgrupo_limpia}") 

            # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
            cursor.execute("""
                SELECT
                    descripcion_n3, 
                    cod_3
                FROM
                    CUENTAS
                WHERE
                    grupo_id = ? AND subgrupo_id = ?
                ORDER BY
                    nivel3_id
            """, (grupo_id_buscado, subgrupo_id))
            cuentas_nivel3 = cursor.fetchall()

            if not cuentas_nivel3:
                print(f"       No se encontraron cuentas de nivel 3 para el subgrupo {cod_subgrupo}.")

            # 3. Imprimir las cuentas de Nivel 3 con su formato
            for j, cuenta_n3 in enumerate(cuentas_nivel3):
                desc_n3 = cuenta_n3[0] 
                cod_full_n3 = cuenta_n3[1] 

                print(f"       {j + 1:02d} {desc_n3}") 


    except sqlite3.Error as e:
        print(f"Error al mostrar cuentas por grupo: {e}")
        # Puedes descomentar 'raise' si quieres que la excepción se propague y el programa se detenga
        # raise 
    finally:
        if conn:
            conn.close()


def obtener_cuentas_formateadas_para_flet(ruta_BDapp, grupo_id_buscado):
    """
    Obtiene y formatea de forma jerárquica los subgrupos (nivel 2) y cuentas (nivel 3)
    para un grupo_id específico, retornando una lista de strings lista para Flet.

    Formato:
    01 Titulo (Subgrupo)
        01 Descripción (Cuenta Nivel 3)
        02 Descripción (Cuenta Nivel 3)
    02 Titulo (Subgrupo)
        01 Descripción (Cuenta Nivel 3)
    """
    conn = None # Inicializar conn a None para asegurar que se cierre en caso de error
    output_lines = [] # Lista para almacenar las líneas de texto que se retornarán

    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
        cursor.execute("""
            SELECT
                S.subgrupo_id,
                S.cod_2,
                S.descripcion_subgrupo
            FROM
                SUBGRUPO S
            WHERE
                S.grupo_id = ?
            ORDER BY
                S.subgrupo_id
        """, (grupo_id_buscado,))
        subgrupos = cursor.fetchall()

        if not subgrupos:
            output_lines.append(f"No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.")
            return output_lines # Retorna la lista con el mensaje de no encontrado

        # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
        for i, subgrupo in enumerate(subgrupos):
            subgrupo_id = subgrupo[0]
            # cod_subgrupo = subgrupo[1] # No se usa en el output_lines final, pero se mantiene por si lo necesitas
            descripcion_subgrupo_limpia = subgrupo[2]

            # Añadir la línea del subgrupo a la lista
            output_lines.append(f"{i + 1:02d} {descripcion_subgrupo_limpia}")

            # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
            cursor.execute("""
                SELECT
                    descripcion_n3,
                    cod_3
                FROM
                    CUENTAS
                WHERE
                    grupo_id = ? AND subgrupo_id = ?
                ORDER BY
                    nivel3_id
            """, (grupo_id_buscado, subgrupo_id))
            cuentas_nivel3 = cursor.fetchall()

            if not cuentas_nivel3:
                # Si no hay cuentas de nivel 3, añadir un mensaje a la lista
                output_lines.append(f"       No se encontraron cuentas de nivel 3 para el subgrupo {subgrupo_id}.") # Usamos subgrupo_id, si quieres cod_subgrupo, descomenta la línea de arriba

            # 3. Añadir las cuentas de Nivel 3 a la lista
            for j, cuenta_n3 in enumerate(cuentas_nivel3):
                desc_n3 = cuenta_n3[0]
                # cod_full_n3 = cuenta_n3[1] # No se usa en el output_lines final, pero se mantiene por si lo necesitas

                output_lines.append(f"       {j + 1:02d} {desc_n3}")

    except sqlite3.Error as e:
        # En caso de error, añadir el mensaje de error a la lista de salida
        output_lines.append(f"Error al obtener cuentas por grupo: {e}")
    finally:
        if conn:
            conn.close()

    return output_lines # ¡Esto es lo importante! Retorna la lista de strings.

  
def mostrar_datos_Diario(ruta_BDapp):
    """
    Muestra todos los registros de la tabla DIARIO.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
    """
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DIARIO;")
        
        # Obtener los nombres de las columnas para el encabezado
        column_names = [description[0] for description in cursor.description]
        print("\n--- Datos de la tabla DIARIO ---")
        print(" | ".join(column_names))
        print("-" * (sum(len(name) for name in column_names) + (len(column_names) - 1) * 3)) # Adjust width for separators

        rows = cursor.fetchall()
        if not rows:
            print("No hay registros en la tabla DIARIO.")
        else:
            for row in rows:
                print(" | ".join(map(str, row))) # Convert all elements to string for joining
        print("------------------------------")
    except sqlite3.Error as e:
        print(f"Error al leer datos de DIARIO: {e}")
    finally:
        if conn:
            conn.close()





# ---------------------------------------- FUNCIONES DE ELIMINAR DATOS ----------------------------------------




# ---------------------------------------- FUNCIONES MODIFICAR DATOS ------------------------------


# ---------------------------------------- OTRAS FUNCIONES DATOS ------------------------------

def mostrar_cuentas_por_grupo_flet(ruta_BDapp: str, grupo_id_buscado: int) -> list[ft.Control]:
    """
    Muestra de forma jerárquica los subgrupos (Nivel 2) y cuentas (Nivel 3)
    para un grupo_id específico, formateado para Flet.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        grupo_id_buscado (int): El ID del grupo a buscar.

    Returns:
        list[ft.Control]: Una lista de controles Flet (ft.Text) que representan
                          la jerarquía de subgrupos y cuentas.
    """
    formatted_controls = []
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # Opcional: Obtener la descripción del GRUPO principal para mostrarla al inicio
        cursor.execute("SELECT descripcion_grupo FROM GRUPO WHERE grupo_id = ?", (grupo_id_buscado,))
        grupo_data = cursor.fetchone()
        if grupo_data:
            formatted_controls.append(
                ft.Text(f"{str(grupo_id_buscado).zfill(2)} {grupo_data[0]}",
                        size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
            )
            formatted_controls.append(ft.Divider()) # Separador visual
        else:
            formatted_controls.append(ft.Text(f"No se encontró el Grupo ID: {grupo_id_buscado}",
                                            color=ft.Colors.RED_500, size=16))
            return formatted_controls # Si no hay grupo, salimos.

        # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
        cursor.execute("""
            SELECT
                S.subgrupo_id,
                S.cod_2,
                S.descripcion_subgrupo
            FROM
                SUBGRUPO S
            WHERE
                S.grupo_id = ?
            ORDER BY
                S.subgrupo_id
        """, (grupo_id_buscado,))
        subgrupos = cursor.fetchall()

        if not subgrupos:
            formatted_controls.append(ft.Text(f"    No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.",
                                            size=14, color=ft.colors.GREY_600))
            return formatted_controls

        # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
        for subgrupo in subgrupos:
            subgrupo_id = subgrupo[0]
            cod_subgrupo_completo = subgrupo[1] # Esto es `cod_2` del subgrupo
            descripcion_subgrupo = subgrupo[2]

            # Formato para el título del subgrupo (Nivel 2)
            # Usamos cod_2 (ej. "1.01") para el prefijo si eso es lo que deseas mostrar
            # Si solo quieres el subgrupo_id dentro del grupo, usarías str(subgrupo_id).zfill(2)
            formatted_controls.append(
                ft.Text(f"  {cod_subgrupo_completo} {descripcion_subgrupo}",
                        size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700)
            )

            # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
            cursor.execute("""
                SELECT
                    C.nivel3_id,
                    C.descripcion_n3,
                    C.cod_3
                FROM
                    CUENTAS C
                WHERE
                    C.grupo_id = ? AND C.subgrupo_id = ?
                ORDER BY
                    C.nivel3_id
            """, (grupo_id_buscado, subgrupo_id))
            cuentas_nivel3 = cursor.fetchall()

            if not cuentas_nivel3:
                formatted_controls.append(ft.Text(f"        No hay cuentas para el subgrupo {cod_subgrupo_completo}.",
                                                size=14, color=ft.Colors.GREY_500))

            # 3. Añadir las cuentas de Nivel 3 con su formato
            for cuenta_n3 in cuentas_nivel3:
                nivel3_id = cuenta_n3[0] # No lo usamos en el formato actual, pero lo tenemos
                descripcion_n3 = cuenta_n3[1]
                cod_full_n3 = cuenta_n3[2] # Esto es `cod_3` de la cuenta

                # Formato para la cuenta (Nivel 3)
                # Usamos cod_3 (ej. "1.01.001") para el prefijo de la cuenta
                formatted_controls.append(
                    ft.Text(f"    {cod_full_n3} {descripcion_n3}",
                            size=14, color=ft.Colors.BLUE_GREY_500)
                )
        formatted_controls.append(ft.Divider()) # Separador visual al final de cada grupo
    except sqlite3.Error as e:
        formatted_controls.append(ft.Text(f"Error de base de datos: {e}",
                                        color=ft.Colors.RED_500, size=16))
    finally:
        if conn:
            conn.close()
    return formatted_controls


# ---------------------------------------- FUNCIONES DE INICIO ----------------------------------------

def inicio_Base_datos():
    crear_base_datos()
    crear_tabla_GRUPO(ruta_BDapp)
    crear_tabla_SUBGRUPO(ruta_BDapp)
    #crear_tabla_CUENTAS(ruta_BDapp)
    #crear_tabla_Diario(ruta_BDapp)

def insertar_datos_iniciales():
    # ... (igual que tu función actual, usando ruta_BDapp en todas las llamadas)

    """
    Inserta datos iniciales en la base de datos.
    """

    # Insertar datos en GRUPO (Nivel 1)
    insertar_datos_grupo(ruta_BDapp, "Cuentas Financieras", "Balance")
    insertar_datos_grupo(ruta_BDapp, "Deudas", "Balance")
    insertar_datos_grupo(ruta_BDapp, "Gastos", "PyG")
    insertar_datos_grupo(ruta_BDapp, "Ingresos", "PyG")

    # Insertar datos en SUBGRUPO (Nivel 2)
        # Grupo 1
    insertar_datos_subgrupo(ruta_BDapp, 1, 1, "Efectivo")
    insertar_datos_subgrupo(ruta_BDapp, 1, 2, "Caixa Enginyers")
    insertar_datos_subgrupo(ruta_BDapp, 1, 3, "Self Bank")
    insertar_datos_subgrupo(ruta_BDapp, 1, 4, "DeGiro")
    insertar_datos_subgrupo(ruta_BDapp, 1, 5, "Trade Republic")
    insertar_datos_subgrupo(ruta_BDapp, 1, 6, "Santander")
    insertar_datos_subgrupo(ruta_BDapp, 1, 7, "BBVA")
    insertar_datos_subgrupo(ruta_BDapp, 1, 8, "B.Sabadell")
    insertar_datos_subgrupo(ruta_BDapp, 1, 9, "Civislend")
    insertar_datos_subgrupo(ruta_BDapp, 1, 10, "StockCrowd")
    insertar_datos_subgrupo(ruta_BDapp, 1, 11, "Mintos")
    insertar_datos_subgrupo(ruta_BDapp, 1, 12, "Bestinver")

    # Grupo 2
    insertar_datos_subgrupo(ruta_BDapp, 2, 1, "Deudas Bancarias")
    insertar_datos_subgrupo(ruta_BDapp, 2, 2, "Deudas familiares")
    insertar_datos_subgrupo(ruta_BDapp, 2, 3, "Deudas inversiones")

    # Grupo 3
    insertar_datos_subgrupo(ruta_BDapp, 3, 1, "Gastos fijos")
    insertar_datos_subgrupo(ruta_BDapp, 3, 2, "Gastos Variables")
    insertar_datos_subgrupo(ruta_BDapp, 3, 3, "Otros Gastos")

    # Grupo 4
    insertar_datos_subgrupo(ruta_BDapp, 4, 1, "Salarios")
    insertar_datos_subgrupo(ruta_BDapp, 4, 2, "No Salariales")
    insertar_datos_subgrupo(ruta_BDapp, 4, 3, "Otros Ingresos")

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
    insertar_datos_cuenta(ruta_BDapp, 1, 5, "Cta.Remunerada")
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

# Insertar datos en GRUPO (Nivel 1)
def insertar_datos_iniciales_grupos():
    insertar_datos_grupo(ruta_BDapp, "Cuentas Financieras", "Balance")
    insertar_datos_grupo(ruta_BDapp, "Deudas", "Balance")
    insertar_datos_grupo(ruta_BDapp, "Gastos", "PyG")
    insertar_datos_grupo(ruta_BDapp, "Ingresos", "PyG")

# Insertar datos en SUBGRUPO (Nivel 2)
def insertar_datos_iniciales_subgrupos(ruta_BDapp):
    """
    Inserts initial subgrupo data into the SUBGRUPO table.
    """
    print("\n--- Inserting Initial Subgrupo Data ---")
    
    # Grupo 1
    insertar_datos_subgrupo(ruta_BDapp, 1, 1, "Efectivo")
    insertar_datos_subgrupo(ruta_BDapp, 1, 2, "Caixa Enginyers")
    insertar_datos_subgrupo(ruta_BDapp, 1, 3, "Self Bank")
    insertar_datos_subgrupo(ruta_BDapp, 1, 4, "DeGiro")
    insertar_datos_subgrupo(ruta_BDapp, 1, 5, "Trade Republic")
    insertar_datos_subgrupo(ruta_BDapp, 1, 6, "Santander")
    insertar_datos_subgrupo(ruta_BDapp, 1, 7, "BBVA")
    insertar_datos_subgrupo(ruta_BDapp, 1, 8, "B.Sabadell")
    insertar_datos_subgrupo(ruta_BDapp, 1, 9, "Civislend")
    insertar_datos_subgrupo(ruta_BDapp, 1, 10, "StockCrowd")
    insertar_datos_subgrupo(ruta_BDapp, 1, 11, "Mintos")
    insertar_datos_subgrupo(ruta_BDapp, 1, 12, "Bestinver")

    # Grupo 2
    insertar_datos_subgrupo(ruta_BDapp, 2, 1, "Deudas Bancarias")
    insertar_datos_subgrupo(ruta_BDapp, 2, 2, "Deudas familiares")
    insertar_datos_subgrupo(ruta_BDapp, 2, 3, "Deudas inversiones")

    # Grupo 3
    insertar_datos_subgrupo(ruta_BDapp, 3, 1, "Gastos fijos")
    insertar_datos_subgrupo(ruta_BDapp, 3, 2, "Gastos Variables")
    insertar_datos_subgrupo(ruta_BDapp, 3, 3, "Otros Gastos")

    # Grupo 4
    insertar_datos_subgrupo(ruta_BDapp, 4, 1, "Salarios")
    insertar_datos_subgrupo(ruta_BDapp, 4, 2, "No Salariales")
    insertar_datos_subgrupo(ruta_BDapp, 4, 3, "Otros Ingresos")

# Insertar datos en CUENTAS (Nivel 3)
def insertar_datos_iniciales_cuentas():
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
    insertar_datos_cuenta(ruta_BDapp, 1, 5, "Cta.Remunerada")
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
    #insertar_datos_cuenta(ruta_BDapp, 1, 13, "CapitalCell")
    #insertar_datos_cuenta(ruta_BDapp, 1, 13, "Cebiotec")    
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

# Insertar datos iniciales en el DIARIO
def insertar_datos_iniciales_diario(ruta_BDapp: str):
    """
    Inserta 5 asientos de ejemplo en la tabla DIARIO.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
    """
    print("\n--- Insertando datos iniciales en DIARIO ---")
    asientos_ejemplo = [
        # Asiento 1: Ingreso por ventas
        {
            'fecha': '01/01/24',
            'grupo_balance': 'ACTIVO',
            'subgrupo_balance': 'ACTIVO CORRIENTE',
            'cuenta_balance': 'BANCOS',
            'importe': 1200.50,
            'grupo_PyG': 'INGRESOS',
            'subgrupo_PyG': 'VENTAS',
            'cuenta_PyG': 'VENTAS PRODUCTOS',
            'traspaso': 0,
            'n_traspaso': None,
            'auditado': 0
        },
        # Asiento 2: Gasto por alquiler
        {
            'fecha': '05/01/24',
            'grupo_balance': 'PASIVO',
            'subgrupo_balance': 'DEUDAS C/P',
            'cuenta_balance': 'ACREEDORES',
            'importe': -300.00,
            'grupo_PyG': 'GASTOS',
            'subgrupo_PyG': 'GASTOS OPERACIONALES',
            'cuenta_PyG': 'ALQUILERES',
            'traspaso': 0,
            'n_traspaso': None,
            'auditado': 0
        },
        # Asiento 3: Traspaso entre cuentas de balance
        {
            'fecha': '10/01/24',
            'grupo_balance': 'ACTIVO',
            'subgrupo_balance': 'ACTIVO CORRIENTE',
            'cuenta_balance': 'CAJA',
            'importe': -200.00,
            'grupo_PyG': 'N/A', # No aplica para traspaso directo de balance
            'subgrupo_PyG': 'N/A',
            'cuenta_PyG': 'N/A',
            'traspaso': 1,
            'n_traspaso': 1,
            'auditado': 1
        },
        # Asiento 4: Segundo parte del traspaso anterior
        {
            'fecha': '10/01/24',
            'grupo_balance': 'ACTIVO',
            'subgrupo_balance': 'ACTIVO CORRIENTE',
            'cuenta_balance': 'BANCOS',
            'importe': 200.00,
            'grupo_PyG': 'N/A', # No aplica para traspaso directo de balance
            'subgrupo_PyG': 'N/A',
            'cuenta_PyG': 'N/A',
            'traspaso': 1,
            'n_traspaso': 1,
            'auditado': 1
        },
        # Asiento 5: Ingreso por intereses, ya auditado
        {
            'fecha': '15/01/24',
            'grupo_balance': 'ACTIVO',
            'subgrupo_balance': 'ACTIVO CORRIENTE',
            'cuenta_balance': 'BANCOS',
            'importe': 50.75,
            'grupo_PyG': 'INGRESOS',
            'subgrupo_PyG': 'OTROS INGRESOS',
            'cuenta_PyG': 'INTERESES COBRADOS',
            'traspaso': 0,
            'n_traspaso': None,
            'auditado': 1
        }
    ]

    for i, asiento in enumerate(asientos_ejemplo):
        print(f"Insertando asiento {i+1}...")
        try:
            insertar_datos_diario(
                ruta_BDapp=ruta_BDapp,
                fecha=asiento['fecha'],
                grupo_balance=asiento['grupo_balance'],
                subgrupo_balance=asiento['subgrupo_balance'],
                cuenta_balance=asiento['cuenta_balance'],
                importe=asiento['importe'],
                grupo_PyG=asiento['grupo_PyG'],
                subgrupo_PyG=asiento['subgrupo_PyG'],
                cuenta_PyG=asiento['cuenta_PyG'],
                traspaso=asiento['traspaso'],
                n_traspaso=asiento['n_traspaso'],
                auditado=asiento['auditado']
            )
        except Exception as e:
            print(f"Fallo al insertar asiento {i+1}: {e}")
    print("--- Inserción de datos iniciales en DIARIO completada ---")

# ----- FUNCIONES que CREO que faltarían ----------------------------------------
# una vez creadas, se han de trasladar las funciones donde toque

def eliminar_subgrupo(ruta_BDapp):
    pass

def eliminar_cuenta(ruta_BDapp):
    pass

def eliminar_asiento(ruta_BDapp):
    pass

def modificar_asiento(ruta_BDapp):
    pass

