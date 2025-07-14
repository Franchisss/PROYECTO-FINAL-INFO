# from PyQt5.QtWidgets import QApplication
# from controlador.controlador_prelogin import ControladorPreLogin
# import sys

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     prelogin = ControladorPreLogin()
#     prelogin.mostrar()
#     sys.exit(app.exec_())

#-------------------------------------------

# import sys
# from PyQt5.QtWidgets import QApplication
# from vista.ventana_login import VentanaLogin
# from vista.vista_selector import VistaSelector

# app = QApplication(sys.argv)

# # ✅ Crear y mostrar la ventana de login
# login = VentanaLogin()
# login.show()

# # 🧼 Esperar a que se cierre (cuando el usuario inicie sesión)
# app.exec_()

# # 📥 Al cerrar el login, verificar si el usuario inició sesión correctamente
# if hasattr(login, 'rol'):
#     nombre_usuario = login.usuario_input.text()
#     rol = login.rol

#     selector = VistaSelector(nombre_usuario, rol)
#     selector.show()
#     sys.exit(app.exec_())
# else:
#     print("❌ No se inició sesión correctamente")
#     sys.exit()

from PyQt5.QtWidgets import QApplication
import sys
from controlador.controlador_login import ControladorLogin

# 🧪 Crear aplicación gráfica
app = QApplication(sys.argv)

# 🎮 Controlador de login
login = ControladorLogin()

# 🖼️ Mostrar ventana de login
login.vista.setWindowTitle("🔐 Inicio de sesión")
login.vista.move(200, 150)
login.vista.resize(400, 300)
login.vista.show()
login.vista.raise_()
login.vista.activateWindow()

# 🧩 Confirmaciones en consola
print("✅ ControladorLogin creado")
print("✅ VistaLogin mostrada correctamente")

# 🌀 Mantener loop gráfico activo
sys.exit(app.exec_())