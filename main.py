from PyQt5.QtWidgets import QApplication
from controlador.controlador_prelogin import ControladorPreLogin
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    prelogin = ControladorPreLogin()
    prelogin.mostrar()
    sys.exit(app.exec_())