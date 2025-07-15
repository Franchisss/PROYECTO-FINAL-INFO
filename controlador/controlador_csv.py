from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from modelo.conexion_bd import conectar
import os
import mysql.connector
import traceback
import pandas as pd

class ControladorCSV:
    def __init__(self, modelo, vista):
        print("🛠️ Iniciando ControladorCSV...")
        self.modelo = modelo
        self.vista = vista
        self.ruta_csv_actual = None
        self.conectar_eventos()
        print("Eventos conectados correctamente")

    def conectar_eventos(self):
        print("Conectando botones...")
        self.vista.boton_cargar.clicked.connect(self.abrir_csv)
        self.vista.boton_grafico.clicked.connect(self.graficar)
        self.vista.boton_ver_bd.clicked.connect(self.ver_registros_bd)
        self.vista.boton_limpiar_tabla.clicked.connect(self.limpiar_tabla)
        self.vista.boton_recargar_csv.clicked.connect(self.recargar_csv)
        print("Botones conectados")

    def abrir_csv(self):
        print("PASO 0: Usuario activó botón para cargar CSV")

        try:
            ruta, _ = QFileDialog.getOpenFileName(None, "Abrir CSV", "", "CSV files (*.csv)")
            print(f"Ruta seleccionada: {ruta}")
            if not ruta:
                print("Usuario canceló la selección del archivo.")
                return

            print("📥 Llamando a modelo.cargar_archivo...")
            df = self.modelo.cargar_archivo(ruta)
            self.ruta_csv_actual = ruta
            print(f"📊 DataFrame cargado con shape {df.shape}")

            if df.empty:
                print("CSV vacío o ilegible")
                QMessageBox.warning(None, "CSV vacío", "El archivo CSV no contiene datos o tiene formato incorrecto.")
                return

            print("Construyendo modelo de tabla...")
            modelo_tabla = QStandardItemModel()
            modelo_tabla.setHorizontalHeaderLabels(df.columns.tolist())
            for i in range(df.shape[0]):
                fila = [QStandardItem(str(val)) for val in df.iloc[i]]
                modelo_tabla.appendRow(fila)
            self.vista.tabla.setModel(modelo_tabla)
            print("Tabla renderizada correctamente")

            print("Actualizando combos de columnas...")
            self.vista.combo_x.clear()
            self.vista.combo_y.clear()
            self.vista.combo_x.addItems(df.columns.tolist())
            self.vista.combo_y.addItems(df.columns.tolist())
            print("Comboboxes actualizados")

            print("Guardando CSV en base de datos...")
            self.guardar_csv_en_bd(ruta)

        except Exception as e:
            print(f"Error al abrir CSV: {e}")
            QMessageBox.critical(None, "Error al cargar CSV", f"Se produjo un error:\n{e}")

    def graficar(self):
        x_col = self.vista.combo_x.currentText()
        y_col = self.vista.combo_y.currentText()

        if x_col and y_col:
            df = self.modelo.df
            if x_col in df.columns and y_col in df.columns:
                self.vista.figure.clear()  # ← limpia gráficos anteriores
                ax = self.vista.figure.add_subplot(111)
                ax.plot(df[x_col], df[y_col], marker='o')
                ax.set_title(f"{y_col} vs {x_col}")
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.grid(True)
                self.vista.figure.tight_layout()
                self.vista.canvas.draw()  # ← pinta en la interfaz CSV
                print("Gráfico generado en la misma ventana")
            else:
                QMessageBox.warning(None, "Columnas inválidas", "Las columnas seleccionadas no existen.")
        else:
            QMessageBox.warning(None, "Selección incompleta", "Seleccione las columnas X e Y.")
    
    def guardar_csv_en_bd(self, ruta_archivo):
        print("ENTRANDO a guardar_csv_en_bd()")
        print(f"Archivo recibido: {ruta_archivo}")

        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='',  # ← usa la que confirmaste que funciona
                database='proyecto3',
                connection_timeout=5,
                use_pure=True
            )
            print("Conexión establecida desde GUI")

            cursor = conexion.cursor()

            nombre_archivo = os.path.basename(ruta_archivo)
            tipo_archivo = os.path.splitext(nombre_archivo)[1].replace('.', '').upper()

            print(f"Insertando: tipo={tipo_archivo}, nombre={nombre_archivo}, ruta={ruta_archivo}")

            query = """
                INSERT INTO archivos_varios (tipo_archivo, nombre_archivo, ruta_archivo)
                VALUES (%s, %s, %s)
            """
            valores = (tipo_archivo, nombre_archivo, ruta_archivo)
            cursor.execute(query, valores)
            conexion.commit()

            print("Inserción exitosa. ID insertado:", cursor.lastrowid)

            cursor.close()
            conexion.close()
            print("Conexión cerrada correctamente.")

            QMessageBox.information(None, "Éxito", f"El archivo '{nombre_archivo}' fue guardado en la base de datos.")

        except mysql.connector.Error as e:
            print("Error de conexión o inserción:")
            traceback.print_exc()
            QMessageBox.critical(None, "Error BD", f"Error al guardar en la base de datos:\n{e}")

        except Exception as ex:
            print("Error inesperado en guardar_csv_en_bd():")
            traceback.print_exc()
            QMessageBox.critical(None, "Error", f"Error inesperado:\n{ex}")
    
    def ver_registros_bd(self):
        print("Consultando registros guardados en la base...")

        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='',  # ← misma clave que ya funciona
                database='proyecto3',
                connection_timeout=5,
                use_pure=True
            )
            print("Conexión establecida para consulta")

            cursor = conexion.cursor()
            cursor.execute("SELECT id, tipo_archivo, nombre_archivo, ruta_archivo FROM archivos_varios")
            registros = cursor.fetchall()

            if not registros:
                print("No hay archivos guardados aún.")
                QMessageBox.information(None, "Sin registros", "Aún no se han insertado archivos.")
                return

            modelo = QStandardItemModel()
            modelo.setHorizontalHeaderLabels(["ID", "Tipo", "Nombre", "Ruta"])
            for fila in registros:
                items = [QStandardItem(str(dato)) for dato in fila]
                modelo.appendRow(items)

            self.vista.tabla.setModel(modelo)
            print(f"{len(registros)} registros cargados en tabla desde la BD")

            cursor.close()
            conexion.close()

        except mysql.connector.Error as e:
            print("Error de conexión o consulta:")
            traceback.print_exc()
            QMessageBox.critical(None, "Error BD", f"No se pudieron obtener los registros:\n{e}")

        except Exception as ex:
            print("Error inesperado en ver_registros_bd():")
            traceback.print_exc()
            QMessageBox.critical(None, "Error", f"No se pudieron obtener los registros:\n{ex}")
    
    def limpiar_tabla(self):
        confirmacion = QMessageBox.question(
            None,
            "Confirmación",
            "¿Eliminar solo los registros duplicados en la base de datos?\nSe conservará la primera ocurrencia de cada archivo.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            try:
                conexion = mysql.connector.connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    password='',
                    database='proyecto3',
                    connection_timeout=5,
                    use_pure=True
                )
                cursor = conexion.cursor()

                # Consulta que elimina duplicados y conserva el primero por combinación clave
                query = """
                    DELETE FROM archivos_varios
                    WHERE id NOT IN (
                        SELECT MIN(id)
                        FROM archivos_varios
                        GROUP BY tipo_archivo, nombre_archivo, ruta_archivo
                    )
                """
                cursor.execute(query)
                conexion.commit()
                print("🧹 Duplicados eliminados correctamente")

                # Limpieza visual
                self.vista.tabla.setModel(QStandardItemModel())
                self.modelo.df = pd.DataFrame()
                self.vista.combo_x.clear()
                self.vista.combo_y.clear()

                QMessageBox.information(None, "Éxito", "Registros duplicados eliminados correctamente.")
                cursor.close()
                conexion.close()

            except Exception as e:
                print(f"Error al eliminar duplicados: {e}")
                QMessageBox.critical(None, "Error BD", f"No se pudieron eliminar los duplicados:\n{e}")
        else:
            print("Cancelado por el usuario")
    
    def actualizar_tabla(self, df):
        modelo_tabla = QStandardItemModel()
        modelo_tabla.setHorizontalHeaderLabels(df.columns.tolist())

        for i in range(df.shape[0]):
            fila = [QStandardItem(str(val)) for val in df.iloc[i]]
            modelo_tabla.appendRow(fila)

        self.vista.tabla.setModel(modelo_tabla)
        print("Tabla actualizada")
    
    def detectar_separador(self, ruta):
        with open(ruta, 'r', encoding='utf-8') as archivo:
            primera_linea = archivo.readline()

        # Detectar si hay más ; o más ,
        if primera_linea.count(';') > primera_linea.count(','):
            return ';'
        else:
            return ','
        
    def recargar_csv(self):
        if self.ruta_csv_actual:
            try:
                separador = self.detectar_separador(self.ruta_csv_actual)
                df = pd.read_csv(self.ruta_csv_actual, sep=separador)
                print(f"CSV recargado con separador '{separador}' — Shape: {df.shape}")

                self.modelo.df = df
                self.actualizar_tabla(df)

                self.vista.combo_x.clear()
                self.vista.combo_y.clear()
                self.vista.combo_x.addItems(df.columns.tolist())
                self.vista.combo_y.addItems(df.columns.tolist())

                print("Recarga completada con éxito")

            except Exception as e:
                print(f"Error al recargar CSV: {e}")
                QMessageBox.critical(None, "Error al recargar", f"No se pudo cargar correctamente:\n{e}")
        else:
            print(" No hay CSV previamente cargado")
            QMessageBox.warning(None, "CSV no disponible", "No hay archivo CSV previamente cargado.")