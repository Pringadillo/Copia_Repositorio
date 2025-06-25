import sqlite3



empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"

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

# Ejemplo de uso (descomentar para probar)
if __name__ == "__main__":

    crear_tabla_Diario(ruta_BDapp)
#
#     # Para verificar la estructura de la tabla (opcional)
    conn = sqlite3.connect(ruta_BDapp)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(DIARIO);")
    print("\nEstructura de la tabla DIARIO:")
    for col in cursor.fetchall():
        print(col)
    conn.close()