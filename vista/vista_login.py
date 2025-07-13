from PyQt5 import QtWidgets, uic
import os

class VistaLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ruta_ui = os.path.join(os.path.dirname(__file__), "login.ui")
        uic.loadUi(ruta_ui, self)

        # Componentes
        self.input_usuario = self.findChild(QtWidgets.QLineEdit, "usuario")
        self.input_contrasena = self.findChild(QtWidgets.QLineEdit, "contrasena")
        self.boton_ingresar = self.findChild(QtWidgets.QPushButton, "botonLogin")