import sqlite3
import flet as ft

from app import globals
from datetime import date



# ---------------------------------------- FUNCIONES DE CREAR BASE DE DATOS Y TABLAS ----------------------------------------
def crear_base_datos():
    ruta_BDapp = globals.ruta_BD  # Accede a la variable global

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
                    tipo_cuenta TEXT NOT NULL CHECK (tipo_cuenta IN ('BALANCE', 'PyG'))
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

def crear_tabla_Diario(ruta_BDapp):
    """
    Crea la tabla DIARIO si no existe, incluyendo IDs con FOREIGN KEYs para la integridad
    y columnas de descripción para facilitar los informes, y la columna 'traspaso'.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DIARIO (
                    id_asiento INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_operacion TEXT NOT NULL, -- Formato esperado: 'DD/MM/AA'
                    
                    -- **Claves Foráneas para la estructura de Cuentas Contables (Balance)**
                    grupo_id INTEGER NOT NULL,            -- ID del Grupo (referencia a GRUPO)
                    subgrupo_id INTEGER NOT NULL,         -- ID del Subgrupo (referencia a SUBGRUPO)
                    cuenta_id INTEGER NOT NULL,           -- ID de la Cuenta (referencia a CUENTAS)
                    
                    -- **Descripciones de la estructura de Cuentas Contables (para informes directos)**
                    descripcion_grupo_contable TEXT NOT NULL,
                    descripcion_subgrupo_contable TEXT NOT NULL,
                    descripcion_cuenta_contable TEXT NOT NULL,
                    
                    -- **Claves Foráneas para la estructura de Pérdidas y Ganancias (PyG)**
                    PyG_id INTEGER NOT NULL,              -- ID de PyG (referencia a PyG)
                    categoria_id INTEGER NOT NULL,        -- ID de Categoría (referencia a CATEGORIAS)
                    subcategoria_id INTEGER NOT NULL,     -- ID de Subcategoría (referencia a SUBCATEGORIAS)
                    
                    -- **Descripciones de la estructura de Pérdidas y Ganancias (para informes directos)**
                    descripcion_PyG_analitica TEXT NOT NULL,
                    descripcion_categoria_analitica TEXT NOT NULL,
                    descripcion_subcategoria_analitica TEXT NOT NULL,
                    
                    descripcion_asiento TEXT,                  -- Descripción detallada del asiento
                    importe_asiento REAL NOT NULL,             -- Importe del asiento (puede ser negativo)
                    
                    traspaso INTEGER DEFAULT 0,                -- Número sin decimales
                    verificar INTEGER DEFAULT 0,               -- 0 (No) por defecto, 1 (Sí)
                    fecha_registro_asiento TEXT NOT NULL DEFAULT (date('now')), -- Fecha de registro del asiento
                    
                    -- **Definición de las FOREIGN KEYs**
                    FOREIGN KEY (grupo_id) REFERENCES GRUPO (grupo_id), -- Suponiendo GRUPO tiene PK grupo_id
                    FOREIGN KEY (grupo_id, subgrupo_id) REFERENCES SUBGRUPO (grupo_id, subgrupo_id), -- Suponiendo SUBGRUPO tiene PK compuesta
                    FOREIGN KEY (grupo_id, subgrupo_id, cuenta_id) REFERENCES CUENTAS (grupo_id, subgrupo_id, cuenta_id), -- Suponiendo CUENTAS tiene PK compuesta
                    
                    FOREIGN KEY (PyG_id) REFERENCES PyG (grupo_id), -- PyG usa grupo_id como PK
                    FOREIGN KEY (PyG_id, categoria_id) REFERENCES CATEGORIAS (PyG_id, categoria_id),
                    FOREIGN KEY (PyG_id, categoria_id, subcategoria_id) REFERENCES SUBCATEGORIAS (PyG_id, categoria_id, subcategoria_id)
                )
            ''')
            conn.commit()
        print(f"Tabla DIARIO creada exitosamente en {ruta_BDapp} con IDs y descripciones, y FOREIGN KEYs.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla DIARIO: {e}")
        raise





# ---------------------------------------- FUNCIONES DE INSERTAR DATOS ----------------------------------------

        

def insertar_datos_grupo(ruta_BDapp, descripcion_grupo, tipo_cuenta):
    """
    Inserta un nuevo grupo en la tabla GRUPO.

    Args:
        ruta_BDapp (str): La ruta completa al archivo de la base de datos SQLite.
        descripcion_grupo (str): La descripción del grupo (ej. 'ACTIVOS', 'INGRESOS').
                                 Se convertirá automáticamente a mayúsculas.
        tipo_cuenta (str): El tipo de cuenta al que pertenece el grupo ('BALANCE' o 'PyG').
                           Se validará contra estos dos valores.

    Returns:
        bool: True si el grupo se insertó correctamente, False en caso contrario.
    """
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # Convertir la descripción a mayúsculas para cumplir con la restricción CHECK
        descripcion_grupo_upper = descripcion_grupo.upper()

        cursor.execute("""
            INSERT INTO GRUPO (descripcion_grupo, tipo_cuenta)
            VALUES (?, ?)
        """, (descripcion_grupo_upper, tipo_cuenta))
        conn.commit()
        print(f"Grupo '{descripcion_grupo_upper}' ({tipo_cuenta}) insertado correctamente.")
        return True
    except sqlite3.IntegrityError as e:
        # Este error se dispara si UNIQUE o CHECK falla (ej. descripción duplicada, tipo_cuenta inválido)
        print(f"Error de integridad al insertar grupo (podría ser duplicado o tipo_cuenta inválido): {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error al insertar grupo: {e}")
        return False
    finally:
        if conn:
            conn.close()


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




# ---------------------------------------- FUNCIONES OBTENER DATOS ----------------------------------------

def obtener_datos_grupo(ruta_BDapp):
    """
    Obtiene todos los datos de la tabla GRUPO como una lista de listas.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.

    Returns:
        list[list]: Una lista donde cada sublista representa una fila de la tabla GRUPO.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GRUPO")
            registros = cursor.fetchall()
        return registros
    except sqlite3.Error as e:
        print(f"Error al obtener datos de GRUPO: {e}")
        return []

def obtener_datos_subgrupo(ruta_BDapp, grupo_id=1):
    """
    Obtiene las columnas cod_2 y desc_2 de la tabla SUBGRUPO
    para un grupo específico, como una lista de tuplas.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int): El ID del grupo para el que se desean obtener los subgrupos.

    Returns:
        list[tuple]: Una lista donde cada tupla contiene (cod_2, desc_2)
                     de los subgrupos pertenecientes al grupo especificado.
                     Retorna una lista vacía en caso de error o si no se
                     encuentran subgrupos para el grupo dado.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_2, desc_2 FROM SUBGRUPO WHERE grupo_id = ?", (grupo_id,))
            registros = cursor.fetchall()
        return registros
    except sqlite3.Error as e:
        print(f"Error al obtener datos de SUBGRUPO para el grupo {grupo_id}: {e}")
        return []

def obtener_datos_cuentas(ruta_BDapp, grupo_id=1, subgrupo_id=1):
    """
    Obtiene las columnas cod_3 y desc_3 de la tabla CUENTAS
    para un grupo y subgrupo específicos.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos.
        grupo_id (int, optional): El ID del grupo para filtrar. Por defecto es 1.
        subgrupo_id (int, optional): El ID del subgrupo para filtrar. Por defecto es 1.

    Returns:
        list[tuple]: Una lista donde cada tupla contiene (cod_3, desc_3)
                     de las cuentas que pertenecen al grupo y subgrupo especificados.
                     Retorna una lista vacía en caso de error o si no se
                     encuentran cuentas para los criterios dados.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cod_3, desc_3
                FROM CUENTAS
                WHERE grupo_id = ? AND subgrupo_id = ?
            """, (grupo_id, subgrupo_id))
            registros = cursor.fetchall()
        return registros
    except sqlite3.Error as e:
        print(f"Error al obtener datos de CUENTAS para el grupo {grupo_id} y subgrupo {subgrupo_id}: {e}")
        return []


def obtener_asientos_diario(ruta_BDapp):
    """
    Obtiene todos los registros de la tabla DIARIO.
    devuelve una lista de diccionarios, donde cada diccionario representa una fila de la tabla DIARIO. 

    """
    datos = []
    try:
        conn = sqlite3.connect(ruta_BDapp)
        conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DIARIO ORDER BY fechaValor DESC, id_diario DESC") # Ordenar por fecha
            datos = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error al obtener datos de DIARIO: {e}")
        # Manejo de errores: por ejemplo, retornar una lista vacía o levantar una excepción
    return datos





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

def ver_tablas_base_datos(ruta_BDapp):
    #ruta_BDapp = globals.ruta_BD  # Accede a la variable global
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
def inicio_Base_datos(ruta_BDapp):
    crear_base_datos(ruta_BDapp)
    crear_tabla_GRUPO(ruta_BDapp)
    crear_tabla_SUBGRUPO(ruta_BDapp)
    crear_tabla_CUENTAS(ruta_BDapp)

    crear_tabla_Diario(ruta_BDapp)
    


def insertar_datos_iniciales(ruta_BDapp):
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





def insertar_asiento_Diario(fecha, grupo1, subgrupo1, cuenta1, descripcion, importe, grupo2, subgrupo2, cuenta2, traspaso, numero_traspaso, fecha_creacion=None):
    """
    Inserta un asiento en la tabla DIARIO.

    Args:
        fecha (str): La fecha del asiento (ej. 'YYYY-MM-DD').
        grupo1 (str): El grupo de la primera cuenta.
        subgrupo1 (str): El subgrupo de la primera cuenta.
        cuenta1 (str): La primera cuenta contable.
        descripcion (str): La descripción del asiento.
        importe (float): El importe del asiento.
        grupo2 (str): El grupo de la segunda cuenta.
        subgrupo2 (str): El subgrupo de la segunda cuenta.
        cuenta2 (str): La segunda cuenta contable.
        traspaso (bool): Indica si es un traspaso (True/False).
        numero_traspaso (str): El número de traspaso, si aplica.
        fecha_creacion (str, opcional): La fecha de creación del registro (ej. 'YYYY-MM-DD HH:MM:SS').
                                        Por defecto, se usa la marca de tiempo actual si no se proporciona.
    Returns:
        bool: True si el asiento se insertó correctamente, False en caso contrario.
    """
    ruta_BDapp = globals.ruta_BD
    conn = None

    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO asientos (fecha, grupo1, subgrupo1, cuenta1, descripcion, importe, grupo2, subgrupo2, cuenta2, traspaso, numero_traspaso, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, grupo1, subgrupo1, cuenta1, descripcion, importe, grupo2, subgrupo2, cuenta2, traspaso, numero_traspaso, fecha_creacion))
        conn.commit()
        print("Asiento guardado en la base de datos.")
        return True
    except sqlite3.Error as e:
        print(f"Error al insertar asiento: {e}")
        return False
    finally:
        if conn:
            conn.close()


def cancelar_asiento_diario():
    """
    Cierra/cancela insertar asiento simple.

    Args:
        asiento_id (int): El ID del asiento a cancelar.

    Returns:
        bool: True si el asiento se canceló correctamente, False en caso contrario.
    """
    pass