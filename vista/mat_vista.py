from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout,
    QFileDialog, QMessageBox, QLineEdit, QSpinBox, QGroupBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatView(QWidget):
    def __init__(self, usuario, rol):
        super().__init__()
        self.usuario = usuario
        self.rol = rol
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

        # Área de gráficos
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # --- Botones de navegación y sesión ---
        nav_layout = QHBoxLayout()
        self.back_btn = QPushButton("🔙 Volver")
        self.logout_btn = QPushButton("🚪 Cerrar sesión")
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.logout_btn)
        self.layout.addLayout(nav_layout)      

        self.setLayout(self.layout)
        
        # Conectar botones a funciones
        self.back_btn.clicked.connect(self.volver)
        self.logout_btn.clicked.connect(self.cerrar_sesion)

    def volver(self):
        self.close()
        from controlador.controlador_selector import ControladorSelector
        self.selector = ControladorSelector(self.usuario, self.rol)
        self.selector.mostrar()

    def cerrar_sesion(self):
        # Lógica para cerrar sesión
        QMessageBox.information(self, "Cerrar sesión", "Sesión cerrada correctamente.")
        self.close()