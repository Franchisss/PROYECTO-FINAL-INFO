from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QComboBox, QTableView
)

class VistaCSV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📁 Visualizador de Archivos CSV")
        self.resize(900, 600)

        # 👉 Layout principal
        layout_principal = QVBoxLayout(self)

        # 🎯 Barra superior: carga y combos de gráfico
        barra_superior = QHBoxLayout()
        self.boton_cargar = QPushButton("📂 Seleccionar CSV")
        self.boton_grafico = QPushButton("📈 Generar gráfico")
        self.boton_ver_bd = QPushButton("🗃️ Ver archivos guardados")
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()

        for boton in [self.boton_cargar, self.boton_grafico, self.boton_ver_bd]:
            boton.setMinimumWidth(130)

        barra_superior.addWidget(self.boton_cargar)
        barra_superior.addWidget(self.boton_grafico)
        barra_superior.addWidget(self.boton_ver_bd)
        barra_superior.addWidget(QLabel("Eje X:"))
        barra_superior.addWidget(self.combo_x)
        barra_superior.addWidget(QLabel("Eje Y:"))
        barra_superior.addWidget(self.combo_y)
        layout_principal.addLayout(barra_superior)

        # 📋 Tabla principal de CSV cargado
        self.tabla = QTableView()
        layout_principal.addWidget(QLabel("Contenido del archivo CSV:"))
        layout_principal.addWidget(self.tabla)

