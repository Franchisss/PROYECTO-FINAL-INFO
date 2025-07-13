from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QStackedWidget
)

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Gestor de Archivos Médicos")
        self.setGeometry(100, 100, 1000, 600)

        # 🧱 Contenedor central (neutro) con layout asignado correctamente
        central_widget = QWidget()
        layout_principal = QHBoxLayout()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # 🎯 Menú lateral con botones
        menu_layout = QVBoxLayout()
        self.boton_csv = QPushButton("📁 Cargar CSV")
        self.boton_estadisticas = QPushButton("📊 Ver estadísticas")
        self.boton_senales = QPushButton("📈 Señales MAT")
        self.boton_imagenes = QPushButton("🖼️ Procesamiento de Imágenes")
        self.boton_salir = QPushButton("🚪 Salir")
        self.boton_salir.clicked.connect(self.close)

        botones = [
            self.boton_csv,
            self.boton_estadisticas,
            self.boton_senales,
            self.boton_imagenes
        ]

        for boton in botones:
            boton.setMinimumHeight(40)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #4285f4;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    margin: 4px;
                }
                QPushButton:hover {
                    background-color: #3367d6;
                }
            """)
            menu_layout.addWidget(boton)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        menu_widget.setFixedWidth(200)

        # 📦 Zona de vistas dinámicas con QStackedWidget
        self.stack = QStackedWidget()

        # ➕ Agregar ambos al layout principal
        layout_principal.addWidget(menu_widget)
        layout_principal.addWidget(self.stack)