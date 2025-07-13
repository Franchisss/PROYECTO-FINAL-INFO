from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class VistaSelector(QWidget):
    def __init__(self, nombre_usuario, rol):
        super().__init__()
        self.setWindowTitle("👋 Bienvenido")
        self.resize(500, 300)
        layout = QVBoxLayout()

        saludo = QLabel(f"Hola {nombre_usuario}, accediste como experto en {rol}.")
        saludo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(saludo)

        self.boton_modulo_especializado = QPushButton()
        if rol == "imagen":
            self.boton_modulo_especializado.setText("🖼️ Entrar a módulo Imágenes")
        elif rol == "senal":
            self.boton_modulo_especializado.setText("🔬 Entrar a módulo Señales")

        self.boton_csv = QPushButton("📁 Manejar Archivos CSV")

        for b in [self.boton_modulo_especializado, self.boton_csv]:
            b.setStyleSheet("font-size: 16px; padding: 10px;")
            layout.addWidget(b)

        self.setLayout(layout)