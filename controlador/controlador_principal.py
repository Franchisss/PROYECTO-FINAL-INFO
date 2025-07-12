from vista.vista_principal import VistaPrincipal
from vista.vista_csv import VistaCSV
from vista.vista_stats import VistaStats

from controlador.controlador_csv import ControladorCSV
from controlador.controlador_stats import ControladorStats

from modelo.modelo_csv import ModeloCSV

class ControladorPrincipal:
    def __init__(self):
        # Vista principal con menú
        self.vista = VistaPrincipal()

        # Módulo CSV
        self.vista_csv = VistaCSV()
        self.modelo_csv = ModeloCSV()
        self.controlador_csv = ControladorCSV(self.modelo_csv, self.vista_csv)
        self.vista.stack.addWidget(self.vista_csv)

        # Módulo Estadísticas
        self.vista_stats = VistaStats()
        self.controlador_stats = ControladorStats(self.vista_stats)
        self.vista.stack.addWidget(self.vista_stats)

        # Conexiones del menú
        self.vista.boton_csv.clicked.connect(lambda: self.vista.stack.setCurrentWidget(self.vista_csv))
        self.vista.boton_estadisticas.clicked.connect(lambda: self.vista.stack.setCurrentWidget(self.vista_stats))

    def mostrar(self):
        self.vista.show()