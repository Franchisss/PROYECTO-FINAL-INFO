from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
import numpy as np

class MatController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.load_btn.clicked.connect(self.load_mat)
        self.view.key_combo.currentIndexChanged.connect(self.key_selected)
        self.view.plot_btn.clicked.connect(self.plot_signals)
        self.view.mean_btn.clicked.connect(self.plot_mean)
        self.view.load_csv_btn.clicked.connect(self.load_csv)  # <--- Nuevo

    def load_mat(self):
        fname, _ = QFileDialog.getOpenFileName(self.view, "Abrir archivo MAT", "", "Archivos MAT (*.mat)")
        if fname:
            keys = self.model.load_mat_file(fname)
            self.view.key_combo.clear()
            self.view.key_combo.addItems(keys)

    def key_selected(self):
        key = self.view.key_combo.currentText()
        arr = self.model.get_array(key)
        if arr is None or not isinstance(arr, np.ndarray):
            QMessageBox.warning(self.view, "Error", "No es un arreglo, vuelva a intentarlo.")
        else:
            if arr.ndim == 1:
                self.view.interval_start.setMaximum(arr.shape[0]-1)
                self.view.interval_end.setMaximum(arr.shape[0])
                self.view.interval_end.setValue(arr.shape[0])
            elif arr.ndim == 2:
                self.view.interval_start.setMaximum(arr.shape[1]-1)
                self.view.interval_end.setMaximum(arr.shape[1])
                self.view.interval_end.setValue(arr.shape[1])

    def plot_signals(self):
        key = self.view.key_combo.currentText()
        arr = self.model.get_array(key)
        if arr is None or not isinstance(arr, np.ndarray):
            QMessageBox.warning(self.view, "Error", "No es un arreglo, vuelva a intentarlo.")
            return
        start = self.view.interval_start.value()
        end = self.view.interval_end.value()
        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)
        if arr.ndim == 1:
            ax.plot(arr[start:end], label='Señal')
        else:
            ch_text = self.view.channel_input.text()
            if ch_text:
                try:
                    channels = [int(x) for x in ch_text.split(',')]
                except:
                    QMessageBox.warning(self.view, "Error", "Canales inválidos.")
                    return
            else:
                channels = list(range(arr.shape[0]))
            if start >= end:
                QMessageBox.warning(self.view, "Error", "Intervalo inválido.")
                return
            segment = arr[channels, start:end]
            for idx, ch in enumerate(channels):
                ax.plot(segment[idx], label=f'Canal {ch}')
        ax.set_title(f"Señales - {key}")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Amplitud")
        ax.legend()
        self.view.canvas.draw()

    def plot_mean(self):
        key = self.view.key_combo.currentText()
        mean = self.model.mean_axis1(key)
        if mean is None:
            QMessageBox.warning(self.view, "Error", "No es un arreglo, vuelva a intentarlo.")
            return
        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)
        ax.stem(mean, use_line_collection=True)
        ax.set_title(f"Promedio eje 1 - {key}")
        ax.set_xlabel("Canal")
        ax.set_ylabel("Promedio")
        self.view.canvas.draw()

    def load_csv(self):
        fname, _ = QFileDialog.getOpenFileName(self.view, "Abrir archivo CSV", "", "Archivos CSV (*.csv)")
        if fname:
            df = self.model.load_csv_file(fname)
            self.view.table.setRowCount(df.shape[0])
            self.view.table.setColumnCount(df.shape[1])
            self.view.table.setHorizontalHeaderLabels(df.columns)
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.view.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))