from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QStackedWidget

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Gestor de Archivos Médicos")
        self.setGeometry(100, 100, 1000, 600)

        # Contenedor central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout(central_widget)

        # Navegación
        self.boton_csv = QPushButton("📁 Cargar CSV")
        self.boton_estadisticas = QPushButton("📊 Ver estadísticas")  # para el futuro
        layout.addWidget(self.boton_csv)
        layout.addWidget(self.boton_estadisticas)

        # Contenedor de vistas
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)