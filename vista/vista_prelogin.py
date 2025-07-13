from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class VistaPreLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simular usuario")
        self.resize(400, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("¿Con qué rol querés entrar hoy?"))

        self.boton_imagen = QPushButton("🖼️ Experto en Imágenes")
        self.boton_senal = QPushButton("🔬 Experto en Señales")

        layout.addWidget(self.boton_imagen)
        layout.addWidget(self.boton_senal)

        self.setLayout(layout)