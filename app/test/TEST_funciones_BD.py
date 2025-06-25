import sqlite3
import os
from datetime import date
import flet as ft


empresa = "TEST_Empresa_10"
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

def crear_tabla_Diario(ruta_BDapp):
    """
    Crea la tabla DIARIO si no existe, con las columnas especificadas,
    incluyendo IDs con FOREIGN KEYs para la integridad y la columna 'traspaso' y 'Revisado'.
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
                    Grupo_Balance INTEGER NOT NULL,       -- ID del Grupo (referencia a GRUPO)
                    Subgrupo_Balance INTEGER NOT NULL,    -- ID del Subgrupo (referencia a SUBGRUPO)
                    Cuenta_Balance INTEGER NOT NULL,      -- ID de la Cuenta (referencia a CUENTAS)
                    
                    -- Claves Foráneas para la estructura de Pérdidas y Ganancias (PyG)
                    Grupo_PyG INTEGER NOT NULL,           -- ID de PyG (referencia a PyG)
                    Categoria_PyG INTEGER NOT NULL,       -- ID de Categoría (referencia a CATEGORIAS)
                    Subcategoria_PyG INTEGER NOT NULL,    -- ID de Subcategoría (referencia a SUBCATEGORIAS)
                    
                    descripcionDiario TEXT,             -- Descripción detallada del asiento
                    importe REAL NOT NULL,              -- Importe del asiento (puede ser negativo, formato con separador de miles y 2 decimales se maneja en la aplicación)
                    
                    traspaso INTEGER DEFAULT 0,           -- Número entero para el traspaso
                    Revisado INTEGER DEFAULT 0,           -- 0 (No) por defecto, 1 (Sí)
                    fechaEntrada TEXT NOT NULL DEFAULT (date('now')), -- Fecha de registro del asiento
                    
                    -- Definición de las FOREIGN KEYs
                    FOREIGN KEY (Grupo_Balance) REFERENCES GRUPO (grupo_id),
                    FOREIGN KEY (Grupo_Balance, Subgrupo_Balance) REFERENCES SUBGRUPO (grupo_id, subgrupo_id),
                    FOREIGN KEY (Grupo_Balance, Subgrupo_Balance, Cuenta_Balance) REFERENCES CUENTAS (grupo_id, subgrupo_id, cuenta_id),
                    
                    FOREIGN KEY (Grupo_PyG) REFERENCES PyG (grupo_id), -- Asumiendo que PyG tiene 'grupo_id' como PK
                    FOREIGN KEY (Grupo_PyG, Categoria_PyG) REFERENCES CATEGORIAS (PyG_id, categoria_id),
                    FOREIGN KEY (Grupo_PyG, Categoria_PyG, Subcategoria_PyG) REFERENCES SUBCATEGORIAS (PyG_id, categoria_id, subcategoria_id)
                )
            ''')
            conn.commit()
        print(f"Tabla DIARIO creada/actualizada exitosamente en {ruta_BDapp} con la nueva estructura.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla DIARIO: {e}")
        raise




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

def insertar_datos_Diario(ruta_BDapp, fechaValor, Grupo_Balance, Subgrupo_Balance, Cuenta_Balance,
                          Grupo_PyG, Categoria_PyG, Subcategoria_PyG,
                          descripcionDiario, importe, traspaso=0, Revisado=0):
    """
    Inserta un nuevo registro en la tabla DIARIO.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        fechaValor (str): La fecha de la operación (formato 'DD/MM/AAAA').
        Grupo_Balance (int): ID del Grupo contable.
        Subgrupo_Balance (int): ID del Subgrupo contable.
        Cuenta_Balance (int): ID de la Cuenta contable.
        Grupo_PyG (int): ID del Grupo de Pérdidas y Ganancias.
        Categoria_PyG (int): ID de la Categoría de PyG.
        Subcategoria_PyG (int): ID de la Subcategoría de PyG.
        descripcionDiario (str): Descripción del asiento.
        importe (float): Importe del asiento (puede ser negativo).
        traspaso (int, optional): Número de traspaso. Por defecto es 0.
        Revisado (int, optional): Estado de revisión (0=No, 1=Sí). Por defecto es 0.
    """
    try:
        conn = sqlite3.connect(ruta_BDapp)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO DIARIO (
                    fechaValor, Grupo_Balance, Subgrupo_Balance, Cuenta_Balance,
                    Grupo_PyG, Categoria_PyG, Subcategoria_PyG,
                    descripcionDiario, importe, traspaso, Revisado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fechaValor, Grupo_Balance, Subgrupo_Balance, Cuenta_Balance,
                  Grupo_PyG, Categoria_PyG, Subcategoria_PyG,
                  descripcionDiario, importe, traspaso, Revisado))
            conn.commit()
        print(f"Registro insertado exitosamente en DIARIO para la fecha {fechaValor}.")
    except sqlite3.Error as e:
        print(f"Error al insertar el registro en DIARIO: {e}")
        # Opcional: relanzar la excepción para manejo en un nivel superior
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



def mostrar_cuentas_por_grupo(ruta_BDapp, grupo_id_buscado):
    """
    Muestra de forma jerárquica los subgrupos (nivel 2) y cuentas (nivel 3)
    para un grupo_id específico, siguiendo el formato:
    01 Titulo (Subgrupo)
          01 Descripción (Cuenta Nivel 3)
          02 Descripción (Cuenta Nivel 3)
    02 Titulo (Subgrupo)
          01 Descripción (Cuenta Nivel 3)
    """
    conn = None # Inicializar conn a None para el bloque finally
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
        # Aunque cod_2 y desc_2 vienen de CUENTAS, asumimos que representan
        # el subgrupo. Lo ideal sería usar la tabla SUBGRUPO si existiera con más detalle.
        cursor.execute("""
            SELECT DISTINCT
                subgrupo_id,
                cod_2,
                desc_2
            FROM
                CUENTAS
            WHERE
                grupo_id = ?
            ORDER BY
                subgrupo_id
        """, (grupo_id_buscado,))
        subgrupos = cursor.fetchall()

        if not subgrupos:
            print(f"No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.")
            return

        #print(f"\n--- Cuentas para el Grupo: {grupo_id_buscado} ---")

        # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
        for i, subgrupo in enumerate(subgrupos):
            subgrupo_id = subgrupo[0]
            cod_subgrupo = subgrupo[1] # Esto es cod_2 en tu tabla CUENTAS
            desc_subgrupo = subgrupo[2] # Esto es desc_2 en tu tabla CUENTAS

            # Formato para el título del subgrupo (Nivel 2)
            # Usamos i + 1 para el índice secuencial (01, 02, etc.)
            print(f"{i + 1:02d} {desc_subgrupo}") # O {cod_subgrupo} si prefieres el código

            # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
            cursor.execute("""
                SELECT
                    descripcion_n3, -- O desc_3, elige la que prefieras mostrar
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
                print(f"      No se encontraron cuentas de nivel 3 para el subgrupo {cod_subgrupo}.")

            # 3. Imprimir las cuentas de Nivel 3 con su formato
            for j, cuenta_n3 in enumerate(cuentas_nivel3):
                desc_n3 = cuenta_n3[0] # Usamos descripcion_n3
                cod_full_n3 = cuenta_n3[1] # Esto es cod_3

                # Formato para las cuentas de nivel 3 (con sangría)
                # Usamos j + 1 para el índice secuencial (01, 02, etc.)
                print(f"      {j + 1:02d} {desc_n3}") # O {cod_full_n3} si prefieres el código completo


    except sqlite3.Error as e:
        print(f"Error al mostrar cuentas por grupo: {e}")
        # raise # Puedes descomentar esto si quieres que la excepción se propague

    finally:
        if conn:
            conn.close()



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

def proves3():
        
    ruta_BDapp = globals.ruta_BD

    # Llama a ver_tabla_nivel1 para obtener los datos
    controles_cuentas1 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 1)
    controles_cuentas2 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 2)
    controles_cuentas3 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 3)
    controles_cuentas4 = mostrar_cuentas_por_grupo_flet(ruta_BDapp, 4)

    texto1 = ft.Container(
        content= ft.Text("TABLA DE CÓDIGOS", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        #bgcolor=ft.Colors.BLUE_GREY_200,
        margin=ft.margin.only(top=20) 
    )
    
    texto2 = ft.Container(
        content=ft.Row(
            controls=[
                # Columna 1: Cuentas Financieras
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas1,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.VerticalDivider(),
                
                # Columna 2: Deudas
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas2,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 3: Gastos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas3,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.ORANGE_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                ft.VerticalDivider(),

                # Columna 4: Ingresos
                ft.Container(
                    content=ft.Column(
                        controls=controles_cuentas4,
                        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO, 
                        expand=True,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.GREEN_100,
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10)
                ),
                
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START,
            wrap=False,
            expand=True

        ),

        padding=10,
        expand=True
        
    )

    # ----------------------  Estructura principal -----------------

    globals.contenido_central_container.content = ft.Container(
        content=ft.Column(
            controls=[
                texto1,
                texto2,

            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical en la parte superior
        ),
        bgcolor=ft.Colors.WHITE,

        )
    
    return globals.contenido_central_container.content
    
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

# ---------------------------------------- FUNCIONES MOPDIFICAR DATOS ------------------------------


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

    
    #print(obtener_datos_grupo(ruta_BDapp))
    #print(obtener_datos_subgrupo(ruta_BDapp, grupo_id=1))
    #print(obtener_datos_cuentas(ruta_BDapp, grupo_id=2, subgrupo_id=1))
    #mostrar_cuentas_por_grupo2(ruta_BDapp, 2)
    #print(obtener_cuentas_formateadas_para_flet(ruta_BDapp, 1))
    #ver_tablas_base_datos()
    
    insertar_datos_Diario(
            ruta_BDapp=ruta_BDapp,
            fechaValor='25/06/2025',
            Grupo_Balance=1,        # Ejemplo de ID de grupo
            Subgrupo_Balance=101,   # Ejemplo de ID de subgrupo
            Cuenta_Balance=10101,   # Ejemplo de ID de cuenta
            Grupo_PyG=1,            # Ejemplo de ID de grupo PyG
            Categoria_PyG=101,      # Ejemplo de ID de categoría PyG
            Subcategoria_PyG=10101, # Ejemplo de ID de subcategoría PyG
            descripcionDiario='Compra de material de oficina',
            importe=-150.75,
            traspaso=0,
            Revisado=0
        )
    insertar_datos_Diario(
            ruta_BDapp=ruta_BDapp,
            fechaValor='25/06/2025',
            Grupo_Balance=2,
            Subgrupo_Balance=201,
            Cuenta_Balance=20101,
            Grupo_PyG=4,
            Categoria_PyG=401,
            Subcategoria_PyG=40101,
            descripcionDiario='Venta de productos',
            importe=500.00,
            traspaso=1,
            Revisado=1
        )
    mostrar_datos_Diario(ruta_BDapp)