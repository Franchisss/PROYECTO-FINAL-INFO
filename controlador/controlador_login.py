from modelo.modelo_login import ModeloLogin
from vista.ventana_login import VentanaLogin
from controlador.controlador_selector import ControladorSelector
from PyQt5.QtWidgets import QMessageBox

class ControladorLogin:
    def __init__(self):
        self.modelo = ModeloLogin()
        self.vista = VentanaLogin()
        self.vista.login_btn.clicked.connect(self.verificar)

    def verificar(self):
        # 📥 Obtener datos ingresados por el usuario
        usuario = self.vista.usuario_input.text().strip().lower()
        contrasena = self.vista.contraseña_input.text().strip()

        # 🔐 Verificar credenciales en la base
        rol = self.modelo.verificar_credenciales(usuario, contrasena)

        if rol:
            print(f"✅ Autenticado: {usuario} como {rol}")
            self.vista.close()

            # 🚀 Lanzar el selector con rol ya verificado
            self.selector = ControladorSelector(usuario, rol)
            self.selector.mostrar()
        else:
            print("❌ Usuario o contraseña incorrectos")
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos.")