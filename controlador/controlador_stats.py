import mysql.connector
import traceback
from vista.vista_stats import VistaStats
from PyQt5.QtWidgets import QMessageBox

class ControladorStats:
    def __init__(self, vista_stats):
        self.vista = vista_stats
        self.vista.boton_actualizar.clicked.connect(self.consultar_estadisticas)

    def consultar_estadisticas(self):
        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='',  # ← ajustalo si usás contraseña
                database='proyecto3',
                connection_timeout=5,
                use_pure=True
            )

            cursor = conexion.cursor()
            cursor.execute("SELECT tipo_archivo, COUNT(*) FROM archivos_varios GROUP BY tipo_archivo")
            resultados = cursor.fetchall()

            texto = "📊 Estadísticas de archivos por tipo:\n\n"
            for tipo, cantidad in resultados:
                texto += f"• {tipo}: {cantidad} archivos\n"

            self.vista.resultado.setPlainText(texto)

            cursor.close()
            conexion.close()

        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(None, "Error", f"No se pudieron obtener estadísticas:\n{e}")