from vista.vista_selector import VistaSelector
from controlador.controlador_csv import ControladorCSV
from modelo.modelo_csv import ModeloCSV
from vista.vista_csv import VistaCSV
from controlador.mat_controlador import MatController
from modelo.mat_modelo import MatModel
from vista.mat_vista import MatView
from vista.vista_imagenes import InterfazImagenes
from PyQt5.QtWidgets import QPushButton

class ControladorSelector:
    def __init__(self, nombre_usuario, rol):
        self.rol = rol.strip().lower().replace("á", "a").replace("é", "e")
        self.vista = VistaSelector(nombre_usuario, self.rol)

        self.vista.boton_modulo_especializado.clicked.connect(self.abrir_especializado)
        self.vista.boton_csv.clicked.connect(self.abrir_csv)

    def mostrar(self):
        self.vista.show()

    def reiniciar_login(self):
        from controlador.controlador_login import ControladorLogin
        self.vista.close()
        self.login = ControladorLogin()

    def abrir_especializado(self):
        self.vista.close()

        if self.rol == "imagenes":
            self.vista_imagenes = InterfazImagenes()
            print("🖼️ Lanzando módulo de imágenes desde ControladorSelector")
            self.vista_imagenes.show()

        elif self.rol == "señales":
            self.vista_senales = MatView()
            self.controlador_senales = MatController(MatModel(), self.vista_senales)
            print("📶 Lanzando módulo de señales desde ControladorSelector")
            self.vista_senales.show()

        else:
            print(f"⚠️ Rol desconocido: '{self.rol}'")
            self.vista.show()

    def abrir_csv(self):
        self.vista.close()

        self.vista_csv = VistaCSV()
        self.controlador_csv = ControladorCSV(ModeloCSV(), self.vista_csv)

        boton_volver = QPushButton("🔙 Volver")
        boton_salir = QPushButton("🚪 Cerrar sesión")

        try:
            self.vista_csv.agregar_botones_navegacion(boton_volver, boton_salir)
        except:
            print("⚠️ VistaCSV no tiene método agregar_botones_navegacion")

        boton_volver.clicked.connect(lambda: (self.vista_csv.close(), self.vista.show()))
        boton_salir.clicked.connect(lambda: (self.vista_csv.close(), self.reiniciar_login()))
        self.vista_csv.show()