# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QPushButton, QComboBox,
#     QTableView, QGroupBox
# )
# from PyQt5.QtCore import Qt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure

# class VistaCSV(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("📁 Visualizador de Archivos CSV")
#         self.resize(900, 600)

#         # ✅ Botones nuevos para duplicados y recarga
#         self.boton_limpiar_tabla = QPushButton("💨 Vaciar tabla")
#         self.boton_recargar_csv = QPushButton("🔄 Volver al CSV")

#         # 👉 Layout principal vertical
#         layout_principal = QVBoxLayout(self)

#         # 🎯 Área para gráfico con matplotlib
#         self.figure = Figure(figsize=(6, 3))
#         self.canvas = FigureCanvas(self.figure)
#         group_grafico = QGroupBox("📊 Gráfico generado")
#         layout_grafico = QVBoxLayout()
#         layout_grafico.addWidget(self.canvas)
#         group_grafico.setLayout(layout_grafico)
#         layout_principal.addWidget(group_grafico)

#         # 🔼 Barra superior con botones principales y comboboxes
#         barra_superior = QHBoxLayout()
#         self.boton_cargar = QPushButton("📂 Seleccionar CSV")
#         self.boton_grafico = QPushButton("📈 Generar gráfico")
#         self.boton_ver_bd = QPushButton("🗃️ Ver archivos guardados")
#         self.combo_x = QComboBox()
#         self.combo_y = QComboBox()

#         for boton in [self.boton_cargar, self.boton_grafico, self.boton_ver_bd]:
#             boton.setMinimumWidth(130)

#         barra_superior.addWidget(self.boton_cargar)
#         barra_superior.addWidget(self.boton_grafico)
#         barra_superior.addWidget(self.boton_ver_bd)
#         barra_superior.addWidget(QLabel("Eje X:"))
#         barra_superior.addWidget(self.combo_x)
#         barra_superior.addWidget(QLabel("Eje Y:"))
#         barra_superior.addWidget(self.combo_y)
#         layout_principal.addLayout(barra_superior)

#         # 📋 Tabla para mostrar contenido CSV
#         self.tabla = QTableView()
#         layout_principal.addWidget(QLabel("Contenido del archivo CSV:"))
#         layout_principal.addWidget(self.tabla)

#         # ✅ Botones adicionales: limpiar tabla y recargar
#         self.boton_limpiar_tabla = QPushButton("💨 Vaciar tabla")
#         self.boton_recargar_csv = QPushButton("🔄 Volver al CSV")

#         layout_botones = QHBoxLayout()
#         layout_botones.setSpacing(20)
#         layout_botones.setAlignment(Qt.AlignCenter)
#         layout_botones.addWidget(self.boton_limpiar_tabla)
#         layout_botones.addWidget(self.boton_recargar_csv)
#         layout_principal.addLayout(layout_botones)


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
        self.setWindowTitle("📁 Visualizador de Archivos CSV")
        self.resize(900, 600)

        # 👉 Layout principal vertical
        layout_principal = QVBoxLayout(self)

        # 🎯 Barra superior con carga y comboboxes
        barra_superior = QHBoxLayout()
        self.boton_cargar = QPushButton("📂 Seleccionar CSV")
        self.boton_grafico = QPushButton("📈 Generar gráfico")
        self.boton_ver_bd = QPushButton("🗃️ Ver archivos guardados")
        self.boton_recargar_csv = QPushButton("🔄 Volver al CSV")
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
        layout_principal.addLayout(barra_superior)

        # 📋 Tabla para mostrar contenido CSV
        self.tabla = QTableView()
        layout_principal.addWidget(QLabel("Contenido del archivo CSV:"))
        layout_principal.addWidget(self.tabla)

        # 📊 Sección del gráfico debajo de la tabla
        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)
        group_grafico = QGroupBox("📊 Gráfico generado")
        layout_grafico = QVBoxLayout()
        layout_grafico.addWidget(self.canvas)
        group_grafico.setLayout(layout_grafico)
        layout_principal.addWidget(group_grafico)

        # ✅ Botones adicionales: limpiar tabla y recargar
        self.boton_limpiar_tabla = QPushButton("💨 Eliminar archivos duplicados")
        self.boton_recargar_csv = QPushButton("🔄 Volver al CSV")

        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(20)
        layout_botones.setAlignment(Qt.AlignCenter)
        layout_botones.addWidget(self.boton_limpiar_tabla)
        layout_botones.addWidget(self.boton_recargar_csv)
        layout_principal.addLayout(layout_botones)