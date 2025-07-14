from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import os

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()

        # 📁 Ruta al archivo .ui (ajustada para compatibilidad)
        ruta_ui = os.path.join(os.path.dirname(__file__), "login.ui")
        uic.loadUi(ruta_ui, self)

        # 🎨 Estilos (opcional)
        self.usuario_input.setStyleSheet("color: black; background-color: white;")
        self.contraseña_input.setStyleSheet("color: black; background-color: white;")
        self.login_btn.setStyleSheet("color: white; background-color: #007ACC; font-size: 14px;")

        # ✅ Confirmación en consola
        print("✅ VentanaLogin cargada y lista")