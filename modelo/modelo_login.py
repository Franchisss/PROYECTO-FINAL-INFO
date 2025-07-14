# import mysql.connector

# class ModeloLogin:
#     def verificar_credenciales(self, usuario, contrasena):
#         print("🌡️ Entrando a verificar_credenciales()...")

#         try:
#             print("🩺 Conectando a la base...")

#             conexion = mysql.connector.connect(
#                 host='localhost',
#                 user='root',
#                 password='',
#                 database='proyecto3'
#             )

#             print("✅ Conexión establecida")

#             cursor = conexion.cursor()
#             print("✅ Cursor creado")

#             # 🔍 Ver todos los usuarios registrados (debug)
#             cursor.execute("SELECT nombre_usuario, password, rol FROM usuarios")
#             print("🧪 Usuarios registrados en base:")
#             for fila in cursor.fetchall():
#                 print(fila)

#             # 🔍 Buscar usuario específico
#             cursor.execute("SELECT nombre_usuario, password, rol FROM usuarios WHERE nombre_usuario = %s", (usuario,))
#             resultado = cursor.fetchone()
#             print(f"→ Resultado parcial: {resultado}")

#             cursor.close()
#             conexion.close()
#             print("✅ Conexión cerrada")

#             if resultado:
#                 db_usuario, db_password, rol = resultado
#                 if db_password == contrasena:
#                     print(f"✔ Contraseña correcta. Rol: {rol}")
#                     return rol
#                 else:
#                     print("❌ Contraseña incorrecta.")
#                     return None
#             else:
#                 print("❌ Usuario no encontrado.")
#                 return None

#         except Exception as e:
#             print(f"🔥 Error al conectar con la base: {e}")
#             return None

# import pymysql

# class ModeloLogin:
#     def __init__(self):
#         try:
#             self.conexion = pymysql.connect(
#                 host="localhost",
#                 user="root",
#                 password="",  # ← tu MySQL no usa contraseña
#                 database="proyecto3"
#             )
#             print("🗄️ Conexión a base de datos (PyMySQL) exitosa")
#         except pymysql.MySQLError as e:
#             print(f"❌ Error de conexión MySQL: {e}")
#             self.conexion = None

#     def verificar_credenciales(self, usuario, contrasena):
#         if not self.conexion:
#             return None

#         try:
#             cursor = self.conexion.cursor()
#             consulta = "SELECT rol FROM usuarios WHERE nombre_usuario = %s AND password = %s"
#             cursor.execute(consulta, (usuario, contrasena))
#             resultado = cursor.fetchone()
#             cursor.close()

#             if resultado:
#                 return resultado[0]
#             return None
#         except Exception as e:
#             print(f"🔥 Error al verificar credenciales: {e}")
#             return None

import pymysql

class ModeloLogin:
    def __init__(self):
        try:
            self.conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",  # Tu MySQL no tiene contraseña
                database="proyecto3"
            )
            print("🗄️ Conexión a base de datos (PyMySQL) exitosa")
        except pymysql.MySQLError as e:
            print(f"❌ Error de conexión MySQL: {e}")
            self.conexion = None

    def verificar_credenciales(self, usuario, contrasena):
        if not self.conexion:
            return None

        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT rol FROM usuarios WHERE nombre_usuario = %s AND password = %s"
            cursor.execute(consulta, (usuario, contrasena))
            resultado = cursor.fetchone()
            cursor.close()

            if resultado:
                rol_raw = resultado[0].strip().lower()
                # 🔄 Normalizar tildes y plural
                rol = rol_raw.replace("á", "a").replace("é", "e")
                print(f"🎯 Rol detectado: {rol}")
                return rol
            return None
        except Exception as e:
            print(f"🔥 Error al verificar credenciales: {e}")
            return None