from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

class VistaStats(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.boton_actualizar = QPushButton("Actualizar estadísticas")
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

        layout.addWidget(self.boton_actualizar)
        layout.addWidget(self.resultado)