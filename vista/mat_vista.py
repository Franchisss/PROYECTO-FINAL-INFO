from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout,
    QFileDialog, QMessageBox, QLineEdit, QSpinBox, QGroupBox, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BioSignal Explorer")
        self.setStyleSheet("background-color: #f0f4f7; font-family: Arial;")
        self.layout = QVBoxLayout()

        # Botón para cargar archivo MAT
        self.load_btn = QPushButton("Cargar archivo .MAT")
        self.layout.addWidget(self.load_btn)

        # ComboBox para llaves
        self.key_combo = QComboBox()
        self.layout.addWidget(QLabel("Seleccione la llave:"))
        self.layout.addWidget(self.key_combo)

        # Selección de canales e intervalos
        group = QGroupBox("Selección de canales e intervalo")
        group_layout = QHBoxLayout()
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Ej: 0,1,2")
        self.interval_start = QSpinBox()
        self.interval_end = QSpinBox()
        group_layout.addWidget(QLabel("Canales:"))
        group_layout.addWidget(self.channel_input)
        group_layout.addWidget(QLabel("Inicio:"))
        group_layout.addWidget(self.interval_start)
        group_layout.addWidget(QLabel("Fin:"))
        group_layout.addWidget(self.interval_end)
        group.setLayout(group_layout)
        self.layout.addWidget(group)

        # Botón para graficar
        self.plot_btn = QPushButton("Graficar señales")
        self.layout.addWidget(self.plot_btn)

        # Botón para promedio
        self.mean_btn = QPushButton("Promedio eje 1 (stem)")
        self.layout.addWidget(self.mean_btn)

        # --- NUEVO: Botón para cargar CSV y tabla para mostrar datos ---
        self.load_csv_btn = QPushButton("Cargar archivo CSV")
        self.layout.addWidget(self.load_csv_btn)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Área de gráficos
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Botón para graficar dispersión
        self.scatter_btn = QPushButton("Graficar dispersión (scatter)")
        self.layout.addWidget(self.scatter_btn)

        self.scatter_x_combo = QComboBox()
        self.scatter_y_combo = QComboBox()
        self.layout.addWidget(QLabel("Columna X:"))
        self.layout.addWidget(self.scatter_x_combo)
        self.layout.addWidget(QLabel("Columna Y:"))
        self.layout.addWidget(self.scatter_y_combo)

        self.setLayout(self.layout)