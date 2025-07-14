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