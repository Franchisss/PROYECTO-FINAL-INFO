import sys
from PyQt5 import QtWidgets
from vista.vista_imagenes import InterfazImagenes

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = InterfazImagenes()
    ventana.show()
    sys.exit(app.exec_())
