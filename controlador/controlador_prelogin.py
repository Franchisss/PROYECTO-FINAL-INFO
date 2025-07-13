from controlador.controlador_selector import ControladorSelector
from vista.vista_prelogin import VistaPreLogin

class ControladorPreLogin:
    def __init__(self):
        self.vista = VistaPreLogin()

        self.vista.boton_imagen.clicked.connect(lambda: self.abrir_selector("imagen"))
        self.vista.boton_senal.clicked.connect(lambda: self.abrir_selector("senal"))

    def mostrar(self):
        self.vista.show()

    def abrir_selector(self, rol):
        self.vista.close()
        self.selector = ControladorSelector("UsuarioSimulado", rol)
        self.selector.mostrar()