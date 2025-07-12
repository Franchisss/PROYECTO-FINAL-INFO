from PyQt5.QtWidgets import QWidget, QPushButton, QTableView, QVBoxLayout, QHBoxLayout, QComboBox

class VistaCSV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de CSV")
        self.resize(800, 500)

        # Botones principales
        self.boton_cargar = QPushButton("Seleccionar CSV")
        self.boton_grafico = QPushButton("Generar gráfico")
        self.boton_ver_bd = QPushButton("📂 Ver archivos guardados")  # ← Nuevo botón

        # Controles de columna
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()

        # Tabla
        self.tabla = QTableView()

        # Layout horizontal para botones y combos
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_cargar)
        layout_botones.addWidget(self.boton_grafico)
        layout_botones.addWidget(self.boton_ver_bd)  # ← Aquí lo agregamos al layout
        layout_botones.addWidget(self.combo_x)
        layout_botones.addWidget(self.combo_y)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.tabla)

        self.setLayout(layout_principal)