import pymysql
import time

print("🔍 Iniciando test con PyMySQL...")

try:
    inicio = time.time()

    conexion = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='proyecto3'
    )

    print(f"✅ ¡Conexión exitosa en {round(time.time() - inicio, 2)} segundos!")
    conexion.close()

except pymysql.MySQLError as err:
    print(f"❌ Error MySQL: {err}")
except Exception as e:
    print(f"🔥 Error inesperado: {e}")