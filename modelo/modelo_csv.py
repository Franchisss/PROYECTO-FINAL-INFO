# import pandas as pd

# class ModeloCSV:
#     def __init__(self):
#         self.df = pd.DataFrame()

#     def cargar_archivo(self, ruta):
#         try:
#             self.df = pd.read_csv(ruta, sep=';')
#             print(f"📊 DataFrame cargado con shape {self.df.shape}")
#             return self.df
#         except Exception as e:
#             print(f"❌ Error al cargar CSV: {e}")
#             return pd.DataFrame()

#     def obtener_columnas(self):
#         return list(self.df.columns) if not self.df.empty else []

# import pandas as pd
# import mysql.connector

# class ModeloCSV:
#     def __init__(self):
#         self.df = pd.DataFrame()

#     # 📂 Cargar archivo CSV en DataFrame
#     def cargar_archivo(self, ruta):
#         try:
#             self.df = pd.read_csv(ruta, sep=';')
#             print(f"📊 DataFrame cargado con shape {self.df.shape}")
#             return self.df
#         except Exception as e:
#             print(f"❌ Error al cargar CSV: {e}")
#             return pd.DataFrame()

#     # 📋 Obtener columnas del DataFrame
#     def obtener_columnas(self):
#         return list(self.df.columns) if not self.df.empty else []

#     # 💾 Insertar en base de datos
#     def insertar_en_bd(self, tipo, nombre, ruta):
#         try:
#             conexion = mysql.connector.connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 password='',
#                 database='proyecto3'
#             )
#             cursor = conexion.cursor()
#             query = """
#                 INSERT INTO archivos_varios (tipo_archivo, nombre_archivo, ruta_archivo, fecha_subida)
#                 VALUES (%s, %s, %s, NOW())
#             """
#             valores = (tipo, nombre, ruta)
#             cursor.execute(query, valores)
#             conexion.commit()
#             print(f"✅ Archivo guardado: {cursor.rowcount} fila(s) insertada(s)")
#             cursor.close()
#             conexion.close()
#         except mysql.connector.Error as error:
#             print(f"❌ Error MySQL: {error}")
#         except Exception as ex:
#             print(f"🛑 Otro error: {ex}")

#     # 📥 Listar archivos guardados
#     def listar_archivos(self):
#         try:
#             conexion = mysql.connector.connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 password='',
#                 database='proyecto3'
#             )
#             cursor = conexion.cursor()
#             cursor.execute("SELECT id, tipo_archivo, nombre_archivo, ruta_archivo FROM archivos_varios")
#             registros = cursor.fetchall()
#             cursor.close()
#             conexion.close()
#             return registros
#         except Exception as e:
#             print(f"❌ Error al listar archivos: {e}")
#             return []
    
#     #Eliminar registros
#     def eliminar_registro(self, id):
#         try:
#             conexion = mysql.connector.connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 password='',
#                 database='proyecto3'
#             )
#             cursor = conexion.cursor()
#             cursor.execute("DELETE FROM archivos_varios WHERE id = %s", (id,))
#             conexion.commit()
#             print(f"🗑️ Registro eliminado: ID {id}")
#             cursor.close()
#             conexion.close()
#         except Exception as e:
#             print(f"❌ Error al eliminar registro: {e}")
            
#     def contar_por_tipo(self):
#         try:
#             conexion = mysql.connector.connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 password='',
#                 database='proyecto3'
#             )
#             cursor = conexion.cursor()
#             query = "SELECT tipo_archivo, COUNT(*) FROM archivos_varios GROUP BY tipo_archivo"
#             cursor.execute(query)
#             resultados = cursor.fetchall()
#             cursor.close()
#             conexion.close()
#             return resultados
#         except Exception as e:
#             print(f"❌ Error al contar: {e}")
#             return []
        
        
        
import pandas as pd
import mysql.connector

class ModeloCSV:
    def __init__(self):
        self.df = pd.DataFrame()

    def cargar_archivo(self, ruta):
        try:
            self.df = pd.read_csv(ruta, sep=';')
            print(f"📊 DataFrame cargado con shape {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return pd.DataFrame()

    def obtener_columnas(self):
        return list(self.df.columns) if not self.df.empty else []

    def insertar_en_bd(self, tipo, nombre, ruta):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='proyecto3'
            )
            cursor = conexion.cursor()
            query = """
                INSERT INTO archivos_varios (tipo_archivo, nombre_archivo, ruta_archivo, fecha_subida)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (tipo, nombre, ruta))
            conexion.commit()
            print(f"✅ Archivo guardado: {cursor.rowcount} fila(s) insertada(s)")
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"❌ Error al insertar: {e}")

    def listar_archivos(self):
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
            cursor.close()
            conexion.close()
            return registros
        except Exception as e:
            print(f"❌ Error al listar archivos: {e}")
            return []

    def eliminar_registro(self, id):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='proyecto3'
            )
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM archivos_varios WHERE id = %s", (id,))
            conexion.commit()
            print(f"🗑️ Registro eliminado: ID {id}")
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")

    def buscar_por_nombre(self, nombre_parcial):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='proyecto3'
            )
            cursor = conexion.cursor()
            query = "SELECT * FROM archivos_varios WHERE nombre_archivo LIKE %s"
            cursor.execute(query, ('%' + nombre_parcial + '%',))
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()
            return resultados
        except Exception as e:
            print(f"❌ Error al buscar: {e}")
            return []

    def contar_por_tipo(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='proyecto3'
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo_archivo, COUNT(*) FROM archivos_varios GROUP BY tipo_archivo")
            conteo = cursor.fetchall()
            cursor.close()
            conexion.close()
            return conteo
        except Exception as e:
            print(f"❌ Error al contar tipos: {e}")
            return []