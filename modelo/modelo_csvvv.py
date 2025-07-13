import pandas as pd
import mysql.connector

class ModeloCSV:
    def __init__(self):
        self.df = pd.DataFrame()

    # 📂 Cargar archivo CSV en DataFrame
    def cargar_archivo(self, ruta):
        try:
            self.df = pd.read_csv(ruta, sep=';')
            print(f"📊 DataFrame cargado con shape {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return pd.DataFrame()

    # 📋 Obtener columnas del DataFrame
    def obtener_columnas(self):
        return list(self.df.columns) if not self.df.empty else []

    # 💾 Insertar en base de datos
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
            valores = (tipo, nombre, ruta)
            cursor.execute(query, valores)
            conexion.commit()
            print(f"✅ Archivo guardado: {cursor.rowcount} fila(s) insertada(s)")
            cursor.close()
            conexion.close()
        except mysql.connector.Error as error:
            print(f"❌ Error MySQL: {error}")
        except Exception as ex:
            print(f"🛑 Otro error: {ex}")

    # 📥 Listar archivos guardados
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