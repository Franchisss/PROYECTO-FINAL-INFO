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
        self.vista = VistaSelector(nombre_usuario, rol)
        self.rol = rol

        self.vista.boton_modulo_especializado.clicked.connect(self.abrir_especializado)
        self.vista.boton_csv.clicked.connect(self.abrir_csv)

    def mostrar(self):
        self.vista.show()

    def abrir_especializado(self):
        self.vista.close()

        if self.rol == "imagen":
            self.vista_imagenes = InterfazImagenes()
            self.vista_imagenes.show()
        else:
            vista = MatView()
            self.controlador_especializado = MatController(MatModel(), vista)

            # Añadir botones de navegación solo si es QWidget
            boton_volver = QPushButton("🔙 Volver")
            boton_salir = QPushButton("🚪 Cerrar sesión")

            vista.layout.addWidget(boton_volver)
            vista.layout.addWidget(boton_salir)

            boton_volver.clicked.connect(self.mostrar)
            boton_salir.clicked.connect(vista.close)

            vista.show()

    def abrir_csv(self):
        self.vista.close()

        vista = VistaCSV()
        self.controlador_csv = ControladorCSV(ModeloCSV(), vista)

        boton_volver = QPushButton("🔙 Volver")
        boton_salir = QPushButton("🚪 Cerrar sesión")

        vista.layout().addWidget(boton_volver)
        vista.layout().addWidget(boton_salir)

        boton_volver.clicked.connect(self.mostrar)
        boton_salir.clicked.connect(vista.close)

        vista.show()