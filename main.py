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