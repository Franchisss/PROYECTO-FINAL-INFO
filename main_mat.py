from PyQt5.QtWidgets import QApplication
from modelo.mat_modelo import MatModel
from vista.mat_vista import MatView
from controlador.mat_controlador import MatController
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = MatModel()
    view = MatView()
    controller = MatController(model, view)
    view.show()
    sys.exit(app.exec_())