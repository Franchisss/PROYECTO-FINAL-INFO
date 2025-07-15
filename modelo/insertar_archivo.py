import mysql.connector

# Datos de prueba
tipo = 'CSV'
nombre = 'notas_finales.csv'
ruta = 'C:/Users/adria/Documents/notas_finales.csv'

print("Conectando para insertar...")

try:
    conexion = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='proyecto3',
        connection_timeout=5
    )

    cursor = conexion.cursor()
    query = """
        INSERT INTO archivos_varios (tipo_archivo, nombre_archivo, ruta_archivo)
        VALUES (%s, %s, %s)
    """
    valores = (tipo, nombre, ruta)
    cursor.execute(query, valores)
    conexion.commit()

    print(f"Archivo guardado: {cursor.rowcount} fila(s) insertada(s)")

    cursor.close()
    conexion.close()

except mysql.connector.Error as error:
    print(f"Error MySQL: {error}")

except Exception as ex:
    print(f"Otro error: {ex}")