import mysql.connector

class ModeloLogin:
    def verificar_credenciales(self, usuario, contrasena):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='proyecto3'
            )
            cursor = conexion.cursor()
            query = "SELECT rol FROM usuarios WHERE nombre = %s AND contrasena = %s"
            cursor.execute(query, (usuario, contrasena))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return None