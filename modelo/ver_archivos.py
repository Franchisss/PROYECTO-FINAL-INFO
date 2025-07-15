import mysql.connector

def listar_archivos():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='proyecto3'
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT id, tipo_archivo, nombre_archivo, ruta_archivo FROM archivos_varios")
        registros = cursor.fetchall()

        print("Archivos almacenados en la base:")
        for fila in registros:
            print(f"ID: {fila[0]}, Tipo: {fila[1]}, Nombre: {fila[2]}, Ruta: {fila[3]}")

        cursor.close()
        conexion.close()

    except Exception as e:
        print(f"Error al listar archivos: {e}")

if __name__ == "__main__":
    listar_archivos()