import sqlite3

DATABASE_NAME = "mi_app.db"
INICIALIZACION_TABLA = "inicializacion"

def verificar_inicializacion_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {INICIALIZACION_TABLA}")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def crear_tablas_iniciales_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Crear la tabla de inicialización si no existe
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {INICIALIZACION_TABLA} (inicializado INTEGER)")
    # Insertar un registro para indicar que la inicialización se completó
    cursor.execute(f"INSERT INTO {INICIALIZACION_TABLA} (inicializado) VALUES (1)")
    conn.commit()
    conn.close()
    print("Inicialización de la base de datos completada.")

def crear_tablacodigos_iniciales():
    print("Creando tablas de códigos iniciales en la base de datos...")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Aquí va tu lógica para crear las tablas y códigos iniciales
    cursor.execute("CREATE TABLE IF NOT EXISTS tabla_codigos (id INTEGER PRIMARY KEY, codigo TEXT)")
    # Insertar algunos códigos iniciales
    cursor.execute("INSERT INTO tabla_codigos (codigo) VALUES ('COD001')")
    cursor.execute("INSERT INTO tabla_codigos (codigo) VALUES ('COD002')")
    conn.commit()
    conn.close()
    print("Tablas de códigos iniciales creadas.")

if __name__ == "__main__":
    if not verificar_inicializacion_db():
        crear_tablas_iniciales_db()
        crear_tablacodigos_iniciales()
    else:
        print("La inicialización de la base de datos ya se ha realizado.")

    # El resto de tu aplicación
    print("Continuando con la ejecución normal de la aplicación.")