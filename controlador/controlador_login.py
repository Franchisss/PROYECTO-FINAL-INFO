from vista.vista_login import VistaLogin
from modelo.modelo_login import ModeloLogin
from controlador.controlador_principal import ControladorPrincipal
from PyQt5.QtWidgets import QMessageBox

class ControladorLogin:
    def __init__(self):
        self.modelo = ModeloLogin()
        self.vista = VistaLogin()
        self.vista.boton_ingresar.clicked.connect(self.verificar)

    def mostrar(self):
        self.vista.show()

    def verificar(self):
        usuario = self.vista.input_usuario.text()
        contrasena = self.vista.input_contrasena.text()
        rol = self.modelo.verificar_credenciales(usuario, contrasena)

        if rol:
            print(f"🔐 Acceso concedido. Rol: {rol}")
            self.vista.close()
            principal = ControladorPrincipal(rol)
            principal.mostrar()
        else:
            QMessageBox.warning(self.vista, "Error", "Credenciales incorrectas")