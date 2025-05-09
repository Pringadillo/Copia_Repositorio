import sqlite3

class DatabaseManager:
    def __init__(self, empresa="Test_BD_2"):
        self.empresa = empresa
        self.base_de_datos = f"bd_{self.empresa}.db"
        self.ruta_bd = f"./data/{self.base_de_datos}"

    def _conectar(self):
        return sqlite3.connect(self.ruta_bd)

    def crear_tabla_grupo(self):
        """
        Crea la tabla GRUPO (Nivel 1) si no existe.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GRUPO (
                    grupo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion_grupo TEXT NOT NULL UNIQUE CHECK (descripcion_grupo = UPPER(descripcion_grupo))
                )
            """)
            conn.commit()
        print("Tabla GRUPO (Nivel 1) creada (si no existía).")

    def crear_tabla_subgrupo(self):
        """
        Crea la tabla SUBGRUPO (Nivel 2) si no existe.
        """
        with self._conectar() as conn:
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

    def crear_tabla_cuentas(self):
        """
        Crea la tabla CUENTAS (Nivel 3) si no existe.
        """
        with self._conectar() as conn:
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

    def insertar_datos_grupo(self, descripcion_grupo):
        """
        Inserta datos en la tabla GRUPO (Nivel 1).

        Args:
            descripcion_grupo (str): Descripción del grupo.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO GRUPO (descripcion_grupo) VALUES (?)
                """, (descripcion_grupo,))
                conn.commit()
                print(f"Insertado en GRUPO (Nivel 1): descripcion_grupo='{descripcion_grupo}'")
            except sqlite3.IntegrityError as e:
                print(f"Error al insertar en GRUPO (Nivel 1): {e}")

    def insertar_datos_subgrupo(self, grupo_id, descripcion_subgrupo):
        """
        Inserta datos en la tabla SUBGRUPO (Nivel 2).

        Args:
            grupo_id (int): ID del grupo al que pertenece.
            descripcion_subgrupo (str): Descripción del subgrupo.
        """
        with self._conectar() as conn:
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
            try:
                cursor.execute("""
                    INSERT INTO SUBGRUPO (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (grupo_id, subgrupo_id, cod_2, desc_2, descripcion_grupo, descripcion_subgrupo))
                conn.commit()
                print(f"Insertado en SUBGRUPO (Nivel 2): grupo_id={grupo_id}, subgrupo_id={subgrupo_id}, cod_2={cod_2}, desc_2='{desc_2}', descripcion_grupo='{descripcion_grupo}', descripcion_subgrupo='{descripcion_subgrupo}'")
            except sqlite3.IntegrityError as e:
                print(f"Error al insertar en SUBGRUPO (Nivel 2): {e}")

    def insertar_datos_cuenta(self, grupo_id, subgrupo_id, descripcion_n3):
        """
        Inserta datos en la tabla CUENTAS (Nivel 3).

        Args:
            grupo_id (int): ID del grupo al que pertenece.
            subgrupo_id (int): ID del subgrupo al que pertenece.
            descripcion_n3 (str): Descripción de la cuenta.
        """
        with self._conectar() as conn:
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

    def mostrar_datos_grupo(self):
        """
        Muestra todos los datos de la tabla GRUPO.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GRUPO")
            registros = cursor.fetchall()
        print("\nContenido de la tabla GRUPO (Nivel 1):")
        for registro in registros:
            print(registro)

    def mostrar_datos_subgrupo(self):
        """
        Muestra todos los datos de la tabla SUBGRUPO.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_2, desc_2 FROM SUBGRUPO")
            registros = cursor.fetchall()
        print("\nContenido de la tabla SUBGRUPO (Nivel 2):")
        for registro in registros:
            print(registro)

    def mostrar_datos_cuentas(self):
        """
        Muestra todos los datos de la tabla CUENTAS.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cod_3, desc_3 FROM CUENTAS")
            registros = cursor.fetchall()
        print("\nContenido de la tabla CUENTAS (Nivel 3):")
        for registro in registros:
            print(registro)


    def mostrar_subgrupos_y_cuentas_por_grupo(self, grupo_id):
        """
        Muestra los subgrupos y cuentas asociadas a un grupo específico.

        Args:
            grupo_id (int): ID del grupo para el cual se desean mostrar los subgrupos y cuentas.
        """
        with self._conectar() as conn:
            cursor = conn.cursor()

            # Obtener los subgrupos del grupo solicitado
            cursor.execute("""
                SELECT subgrupo_id, descripcion_subgrupo
                FROM SUBGRUPO
                WHERE grupo_id = ?
            """, (grupo_id,))
            subgrupos = cursor.fetchall()

            if not subgrupos:
                print(f"No se encontraron subgrupos para el grupo con ID {grupo_id}.")
                return

            #print(f"\nSubgrupos y cuentas del grupo con ID {grupo_id}:\n")

            # Iterar sobre los subgrupos y obtener las cuentas asociadas
            for subgrupo_id, descripcion_subgrupo in subgrupos:
                print(f"Subgrupo {subgrupo_id} {descripcion_subgrupo}")

                # Obtener las cuentas asociadas al subgrupo
                cursor.execute("""
                    SELECT cod_3, desc_3
                    FROM CUENTAS
                    WHERE grupo_id = ? AND subgrupo_id = ?
                """, (grupo_id, subgrupo_id))
                cuentas = cursor.fetchall()

                if cuentas:
                    for cod_3, desc_3 in cuentas:
                        print(f"   {cod_3} - {desc_3}")
                else:
                    print("    No hay cuentas asociadas a este subgrupo.")


'''
db_manager = DatabaseManager()
db_manager.mostrar_subgrupos_y_cuentas_por_grupo(4)

'''






'''

if __name__ == "__main__":
    # Crear una instancia de la clase DatabaseManager
    db_manager = DatabaseManager()

    # Crear las tablas
    db_manager.crear_tabla_grupo()
    db_manager.crear_tabla_subgrupo()
    db_manager.crear_tabla_cuentas()

    # Insertar los datos iniciales en GRUPO (Nivel 1)
    db_manager.insertar_datos_grupo("PRODCTOS FINANCIEROS")
    db_manager.insertar_datos_grupo("DEUDAS")
    db_manager.insertar_datos_grupo("GASTOS")
    db_manager.insertar_datos_grupo("INGRESOS")

    # Insertar datos en SUBGRUPO (Nivel 2)
    db_manager.insertar_datos_subgrupo(1, "Caixa Enginyers")
    db_manager.insertar_datos_subgrupo(1, "Self Banc")
    db_manager.insertar_datos_subgrupo(1, "DeGiro")
    db_manager.insertar_datos_subgrupo(1, "Santander")
    db_manager.insertar_datos_subgrupo(1, "Stockcrowd")
    db_manager.insertar_datos_subgrupo(1, "Civislend")
    db_manager.insertar_datos_subgrupo(1, "T.R.Publicidad")
    db_manager.insertar_datos_subgrupo(1, "Bestinver")
    db_manager.insertar_datos_subgrupo(1, "Bufete Perez Pozo")
    db_manager.insertar_datos_subgrupo(1, "Kontactalia")
    db_manager.insertar_datos_subgrupo(1, "Inversiones en empresas")
    db_manager.insertar_datos_subgrupo(1, "Carmon Inversores")
    db_manager.insertar_datos_subgrupo(1, "Trade Republic")
    db_manager.insertar_datos_subgrupo(1, "B Sabadell")
    db_manager.insertar_datos_subgrupo(1, "BBVA")
    db_manager.insertar_datos_subgrupo(1, "Minto")
    db_manager.insertar_datos_subgrupo(2, "Deudas Familiares")
    db_manager.insertar_datos_subgrupo(2, "Deudas Casa")
    db_manager.insertar_datos_subgrupo(2, "Otras Deudas")
    db_manager.insertar_datos_subgrupo(3, "Gastos Fijos")
    db_manager.insertar_datos_subgrupo(3, "Gastos Variables")
    db_manager.insertar_datos_subgrupo(3, "Gastos Extraordinarios")
    db_manager.insertar_datos_subgrupo(4, "Salarios")
    db_manager.insertar_datos_subgrupo(4, "Inversiones")
    db_manager.insertar_datos_subgrupo(4, "Otros Ingresos")

    # Insertar datos en CUENTAS (Nivel 3)
    db_manager.insertar_datos_cuenta(1, 1, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 1, "Depósitos")
    db_manager.insertar_datos_cuenta(1, 1, "Fondos Inv.")
    db_manager.insertar_datos_cuenta(1, 1, "Cta.Cte. $")
    db_manager.insertar_datos_cuenta(1, 1, "Depósitos $")
    db_manager.insertar_datos_cuenta(1, 2, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 2, "Cta. Remunerada")
    db_manager.insertar_datos_cuenta(1, 2, "Depósitos")
    db_manager.insertar_datos_cuenta(1, 2, "Fondos Inv.")
    db_manager.insertar_datos_cuenta(1, 2, "F.Inv. Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 4, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 4, "Renta Variable")
    db_manager.insertar_datos_cuenta(1, 4, "Derivados Financieros")
    db_manager.insertar_datos_cuenta(1, 3, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 3, "Renta Variable")
    db_manager.insertar_datos_cuenta(1, 3, "ETF")
    db_manager.insertar_datos_cuenta(1, 5, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 5, "Crowfunding")
    db_manager.insertar_datos_cuenta(1, 6, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 6, "Crowfunding")
    db_manager.insertar_datos_cuenta(1, 7, "Crowfunding")
    db_manager.insertar_datos_cuenta(1, 8, "Plan Pensiones")
    db_manager.insertar_datos_cuenta(1, 8, "Fondos Inv.")
    db_manager.insertar_datos_cuenta(1, 9, "Crowfunding")
    db_manager.insertar_datos_cuenta(1, 10, "CapitalCell")
    db_manager.insertar_datos_cuenta(1, 10, "Cebiotec")
    db_manager.insertar_datos_cuenta(1, 11, "Crowfunding")
    db_manager.insertar_datos_cuenta(1, 12, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 12, "Depósitos")
    db_manager.insertar_datos_cuenta(1, 13, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 13, "Depósitos")    
    db_manager.insertar_datos_cuenta(1, 14, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 14, "Depósitos")    
    db_manager.insertar_datos_cuenta(1, 15, "Cta.Cte.")
    db_manager.insertar_datos_cuenta(1, 15, "Depósitos") 
    db_manager.insertar_datos_cuenta(1, 16, "Crowfunding")    
    db_manager.insertar_datos_cuenta(2, 1, "Roger")
    db_manager.insertar_datos_cuenta(2, 1, "Enric")
    db_manager.insertar_datos_cuenta(2, 2, "Enaire 0%")
    db_manager.insertar_datos_cuenta(2, 3, "Inversiones JMG")
    db_manager.insertar_datos_cuenta(2, 3, "Avis")
    db_manager.insertar_datos_cuenta(2, 3, "Tata")
    db_manager.insertar_datos_cuenta(2, 3, "Albert")
    db_manager.insertar_datos_cuenta(2, 3, "Joan Moises")
    db_manager.insertar_datos_cuenta(3, 1, "Comida")
    db_manager.insertar_datos_cuenta(3, 1, "Agua")
    db_manager.insertar_datos_cuenta(3, 1, "Luz")
    db_manager.insertar_datos_cuenta(3, 1, "Gas")
    db_manager.insertar_datos_cuenta(3, 1, "Teléfono/Internet")
    db_manager.insertar_datos_cuenta(3, 1, "Limpieza")
    db_manager.insertar_datos_cuenta(3, 1, "Comunidad Vecinos")
    db_manager.insertar_datos_cuenta(3, 1, "Otros Gastos Fijos")
    db_manager.insertar_datos_cuenta(3, 2, "Ropa")
    db_manager.insertar_datos_cuenta(3, 2, "Salud")
    db_manager.insertar_datos_cuenta(3, 2, "Transporte")
    db_manager.insertar_datos_cuenta(3, 2, "Seguros")
    db_manager.insertar_datos_cuenta(3, 2, "Impuestos")
    db_manager.insertar_datos_cuenta(3, 2, "Vacaciones")
    db_manager.insertar_datos_cuenta(3, 2, "Otros Gastos Variables")
    db_manager.insertar_datos_cuenta(3, 3, "Gastos Extraordinarios")
    db_manager.insertar_datos_cuenta(3, 3, "Otros Gastos Extraordinarios")
    db_manager.insertar_datos_cuenta(3, 3, "Cuadrar Saldos")
    db_manager.insertar_datos_cuenta(4, 1, "Montse")
    db_manager.insertar_datos_cuenta(4, 1, "Carlos")
    db_manager.insertar_datos_cuenta(4, 1, "Pensión")
    db_manager.insertar_datos_cuenta(4, 2, "Bancarios")
    db_manager.insertar_datos_cuenta(4, 2, "Renta Fija")
    db_manager.insertar_datos_cuenta(4, 2, "Renta Variable")
    db_manager.insertar_datos_cuenta(4, 2, "Fondos Inv.")
    db_manager.insertar_datos_cuenta(4, 2, "Crowfunding")
    db_manager.insertar_datos_cuenta(4, 3, "Otros Ingresos")

    # Mostrar los datos
    db_manager.mostrar_datos_grupo()
    db_manager.mostrar_datos_subgrupo()
    db_manager.mostrar_datos_cuentas()
    '''