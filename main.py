from PyQt5.QtWidgets import QApplication
from controlador.controlador_principal import ControladorPrincipal
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = ControladorPrincipal()
    control.mostrar()
    sys.exit(app.exec_())