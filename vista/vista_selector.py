from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class VistaSelector(QWidget):
    def __init__(self, nombre_usuario, rol):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.resize(500, 300)
        layout = QVBoxLayout()

        # Mostrar saludo personalizado
        saludo = QLabel(f"Hola {nombre_usuario}, accediste como experto en {rol}.")
        saludo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(saludo)

        # Normalizar rol por si viene con tildes o mayúsculas
        rol = rol.strip().lower().replace("á", "a").replace("é", "e")

        self.boton_modulo_especializado = QPushButton()
        if rol == "imagenes":
            self.boton_modulo_especializado.setText("Entrar a módulo Imágenes")
        elif rol == "señales":
            self.boton_modulo_especializado.setText("Entrar a módulo Señales")
        else:
            self.boton_modulo_especializado.setText("Módulo no identificado")

        self.boton_csv = QPushButton("Manejar Archivos CSV")

        for b in [self.boton_modulo_especializado, self.boton_csv]:
            b.setStyleSheet("font-size: 16px; padding: 10px;")
            layout.addWidget(b)

        self.setLayout(layout)