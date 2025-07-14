from PyQt5.QtWidgets import QMessageBox, QFileDialog, QInputDialog
import numpy as np

class MatController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.load_btn.clicked.connect(self.load_mat)
        self.view.key_combo.currentIndexChanged.connect(self.key_selected)
        self.view.plot_btn.clicked.connect(self.plot_signals)
        self.view.mean_btn.clicked.connect(self.plot_mean)
        

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
            info = f"Dimensiones: {arr.ndim} | Shape: {arr.shape}"
            QMessageBox.information(self.view, "Información del arreglo", info)
            if arr.ndim == 1:
                self.view.interval_start.setMaximum(arr.shape[0]-1)
                self.view.interval_end.setMaximum(arr.shape[0])
                self.view.interval_end.setValue(arr.shape[0])
            elif arr.ndim == 2:
                self.view.interval_start.setMaximum(arr.shape[1]-1)
                self.view.interval_end.setMaximum(arr.shape[1])
                self.view.interval_end.setValue(arr.shape[1])
            elif arr.ndim == 3:
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
        ch_text = self.view.channel_input.text()
        if arr.ndim == 1:
            if start >= end or end > arr.shape[0]:
                QMessageBox.warning(self.view, "Error", "Intervalo inválido.")
                return
            ax.plot(arr[start:end], label='Señal')
        elif arr.ndim == 2:
            if ch_text:
                try:
                    channels = [int(x) for x in ch_text.split(',')]
                except:
                    QMessageBox.warning(self.view, "Error", "Canales inválidos.")
                    return
            else:
                channels = list(range(arr.shape[0]))
            if any(ch >= arr.shape[0] or ch < 0 for ch in channels):
                QMessageBox.warning(self.view, "Error", "Uno o más canales no existen.")
                return
            if start >= end or end > arr.shape[1]:
                QMessageBox.warning(self.view, "Error", "Intervalo inválido.")
                return
            segment = arr[channels, start:end]
            for idx, ch in enumerate(channels):
                ax.plot(segment[idx], label=f'Canal {ch}')
        elif arr.ndim == 3:
            eje, ok = QInputDialog.getInt(self.view, "Eje para corte", "¿Sobre qué eje quieres hacer el corte? (0, 1 o 2)", 0, 0, 2, 1)
            if not ok:
                return
            idx, ok = QInputDialog.getInt(self.view, "Índice del corte", f"¿Qué índice del eje {eje} quieres visualizar? (0 a {arr.shape[eje]-1})", 0, 0, arr.shape[eje]-1, 1)
            if not ok:
                return
            if eje == 0:
                corte = arr[idx, :, :]
            elif eje == 1:
                corte = arr[:, idx, :]
            elif eje == 2:
                corte = arr[:, :, idx]
            else:
                QMessageBox.warning(self.view, "Error", "Eje inválido.")
                return
            if ch_text:
                try:
                    channels = [int(x) for x in ch_text.split(',')]
                except:
                    QMessageBox.warning(self.view, "Error", "Canales inválidos.")
                    return
            else:
                channels = list(range(corte.shape[0]))
            if any(ch >= corte.shape[0] or ch < 0 for ch in channels):
                QMessageBox.warning(self.view, "Error", "Uno o más canales no existen en el corte.")
                return
            if start >= end or end > corte.shape[1]:
                QMessageBox.warning(self.view, "Error", "Intervalo inválido en el corte.")
                return
            segment = corte[channels, start:end]
            for idx, ch in enumerate(channels):
                ax.plot(segment[idx], label=f'Canal {ch}')
        else:
            QMessageBox.warning(self.view, "Error", "Solo se soportan arreglos 1D, 2D o 3D.")
            return
        ax.set_title(f"Señales - {key}")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Amplitud")
        ax.legend()
        self.view.canvas.draw()

    def plot_mean(self):
        key = self.view.key_combo.currentText()
        arr = self.model.get_array(key)
        mean = self.model.mean_axis1(key)
        if mean is None:
            QMessageBox.warning(self.view, "Error", "No es un arreglo, vuelva a intentarlo.")
            return
        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)
        if isinstance(mean, np.ndarray):
            if mean.ndim == 0:
                ax.stem([mean])
            elif mean.ndim == 1:
                ax.stem(mean)
            elif mean.ndim == 2:
                idx, ok = QInputDialog.getInt(self.view, "Índice del corte", f"¿Qué corte quieres graficar? (0 a {mean.shape[1]-1})", 0, 0, mean.shape[1]-1, 1)
                if not ok:
                    return
                ax.stem(mean[:, idx])
            else:
                QMessageBox.warning(self.view, "Error", "No se puede graficar el promedio para este arreglo.")
                return
        else:
            ax.stem([mean])
        ax.set_title(f"Promedio eje 1 - {key}")
        ax.set_xlabel("Canal")
        ax.set_ylabel("Promedio")
        self.view.canvas.draw()