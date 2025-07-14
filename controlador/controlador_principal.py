from vista.vista_principal import VistaPrincipal
from vista.vista_csv import VistaCSV
from vista.vista_stats import VistaStats
from vista.vista_imagenes import InterfazImagenes
from vista.mat_vista import MatView

from controlador.controlador_csv import ControladorCSV
from controlador.controlador_stats import ControladorStats
from controlador.mat_controlador import MatController

from modelo.mat_modelo import MatModel
from modelo.modelo_csv import ModeloCSV

class ControladorPrincipal:
    def __init__(self, rol="general", usuario="Usuario"):
        self.vista = VistaPrincipal()
        self.vista.setAttribute(103)  # Qt.WA_QuitOnClose

        # 👋 Saludo visual
        self.vista.saludo_label.setText(
            f"👋 Hola {usuario}, bienvenido al sistema como experto en {rol}.")

        print("🧠 ControladorPrincipal iniciado")
        print(f"→ Rol recibido: {rol}")
        print(f"→ Usuario recibido: {usuario}")
        print(f"→ Vista tipo: {type(self.vista)}")

        # 📁 Módulo CSV
        self.vista_csv = VistaCSV()
        self.modelo_csv = ModeloCSV()
        self.controlador_csv = ControladorCSV(self.modelo_csv, self.vista_csv)
        self.vista.stack.addWidget(self.vista_csv)

        # 📊 Módulo Estadísticas
        self.vista_stats = VistaStats()
        self.controlador_stats = ControladorStats(self.vista_stats)
        self.vista.stack.addWidget(self.vista_stats)

        # 📈 Módulo Señales MAT
        self.vista_mat = MatView()
        self.controlador_mat = MatController(MatModel(), self.vista_mat)
        self.vista.stack.addWidget(self.vista_mat)

        # 🖼️ Módulo Imágenes
        self.vista_imagenes = InterfazImagenes()
        self.vista.stack.addWidget(self.vista_imagenes)

        # 🔗 Conexiones de menú lateral
        self.vista.boton_csv.clicked.connect(
            lambda: self.vista.stack.setCurrentWidget(self.vista_csv))
        self.vista.boton_estadisticas.clicked.connect(
            lambda: self.vista.stack.setCurrentWidget(self.vista_stats))
        self.vista.boton_senales.clicked.connect(
            lambda: self.vista.stack.setCurrentWidget(self.vista_mat))
        self.vista.boton_imagenes.clicked.connect(
            lambda: self.vista.stack.setCurrentWidget(self.vista_imagenes))

        # 🧠 Activación dinámica de módulos según rol
        if rol.strip().lower() == "imagenes":
            self.vista.boton_csv.setVisible(True)
            self.vista.boton_imagenes.setVisible(True)
            self.vista.boton_senales.setVisible(False)
            self.vista.boton_estadisticas.setVisible(False)
            self.vista.stack.setCurrentWidget(self.vista_csv)

        elif rol.strip().lower() == "señales":
            self.vista.boton_csv.setVisible(False)
            self.vista.boton_imagenes.setVisible(False)
            self.vista.boton_senales.setVisible(True)
            self.vista.boton_estadisticas.setVisible(True)
            self.vista.stack.setCurrentWidget(self.vista_mat)

        else:
            self.vista.stack.setCurrentWidget(self.vista_csv)

        # 🧩 Debug visual en consola
        print("🧩 Vistas en el stack:")
        for i in range(self.vista.stack.count()):
            print(f" - {self.vista.stack.widget(i).__class__.__name__}")

        # 💥 MOSTRAR LA VISTA PRINCIPAL 🔥
        print("👀 Mostrando vista principal... FORZADO")
        self.vista.setWindowTitle("👋 Hola Adrián, sistema activo")
        self.vista.move(200, 200)
        self.vista.resize(1000, 600)
        self.vista.show()
        self.vista.raise_()
        self.vista.activateWindow()