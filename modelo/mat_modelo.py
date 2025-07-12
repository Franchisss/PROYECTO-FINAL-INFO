import numpy as np
import os
from scipy.io import loadmat
import pandas as pd  # <--- Agrega esta línea

class MatModel:
    def __init__(self):
        self.data = None
        self.keys = []
        self.csv_data = None  # <--- Para almacenar el DataFrame

    def load_mat_file(self, filepath):
        import scipy.io
        self.archivo_actual = os.path.basename(filepath)  # ← guarda solo el nombre del archivo
        self.mat_data = scipy.io.loadmat(filepath)
        return list(self.mat_data.keys())


    def get_array(self, key):
        arr = self.data.get(key)
        if isinstance(arr, np.ndarray):
            return arr
        return None

    def get_shape(self, key):
        arr = self.get_array(key)
        if arr is not None:
            return arr.shape
        return None

    def get_segment(self, key, channels=None, interval=None):
        arr = self.get_array(key)
        if arr is None:
            return None
        if channels is not None:
            arr = arr[channels, :]
        if interval is not None:
            arr = arr[:, interval[0]:interval[1]]
        return arr

    def mean_axis1(self, key):
        arr = self.get_array(key)
        if arr is not None and isinstance(arr, np.ndarray):
            if arr.ndim == 1:
                return np.mean(arr)
            elif arr.ndim == 2:
                return np.mean(arr, axis=1)
            elif arr.ndim == 3:
                # Promedio sobre el eje 1 para cada "canal" y "corte"
                return np.mean(arr, axis=1)  # Esto da shape (canales, cortes)
        return None

    def load_csv_file(self, filepath):
        self.csv_data = pd.read_csv(filepath)
        return self.csv_data