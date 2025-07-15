from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox,
    QTableView, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VistaCSV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Archivos CSV")
        self.resize(900, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Barra superior con carga y combos
        barra_superior = QHBoxLayout()
        self.boton_cargar = QPushButton("Seleccionar CSV")
        self.boton_grafico = QPushButton("Generar gráfico")
        self.boton_ver_bd = QPushButton("Ver archivos guardados")
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()

        for boton in [self.boton_cargar, self.boton_grafico, self.boton_ver_bd]:
            boton.setMinimumWidth(130)

        barra_superior.addWidget(self.boton_cargar)
        barra_superior.addWidget(self.boton_grafico)
        barra_superior.addWidget(self.boton_ver_bd)
        barra_superior.addWidget(QLabel("Eje X:"))
        barra_superior.addWidget(self.combo_x)
        barra_superior.addWidget(QLabel("Eje Y:"))
        barra_superior.addWidget(self.combo_y)
        layout.addLayout(barra_superior)

        # Tabla CSV
        self.tabla = QTableView()
        layout.addWidget(QLabel("Contenido del archivo CSV:"))
        layout.addWidget(self.tabla)

        # Área del gráfico
        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)
        group_grafico = QGroupBox("Gráfico generado")
        layout_grafico = QVBoxLayout()
        layout_grafico.addWidget(self.canvas)
        group_grafico.setLayout(layout_grafico)
        layout.addWidget(group_grafico)

        # ⚙️ Grupo de acciones sobre el CSV
        self.boton_recargar_csv = QPushButton("Volver al CSV")
        self.boton_limpiar_tabla = QPushButton("Eliminar archivos duplicados")

        fila_operaciones = QHBoxLayout()
        fila_operaciones.setSpacing(30)
        fila_operaciones.setAlignment(Qt.AlignCenter)
        fila_operaciones.addWidget(self.boton_recargar_csv)
        fila_operaciones.addWidget(self.boton_limpiar_tabla)

        grupo_csv = QGroupBox("Acciones sobre el CSV")
        grupo_csv.setLayout(fila_operaciones)
        layout.addWidget(grupo_csv)

        # Grupo de navegación externa
        self.layout_navegacion = QHBoxLayout()
        self.layout_navegacion.setSpacing(30)
        self.layout_navegacion.setAlignment(Qt.AlignCenter)

        grupo_nav = QGroupBox("Navegación")
        grupo_nav.setLayout(self.layout_navegacion)
        layout.addWidget(grupo_nav)

    def agregar_botones_navegacion(self, boton_volver, boton_salir):
        self.layout_navegacion.addWidget(boton_volver)
        self.layout_navegacion.addWidget(boton_salir)