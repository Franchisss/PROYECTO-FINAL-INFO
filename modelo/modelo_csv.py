import pandas as pd

class ModeloCSV:
    def __init__(self):
        self.df = pd.DataFrame()

    def cargar_archivo(self, ruta):
        try:
            self.df = pd.read_csv(ruta, sep=';')
            print(f"📊 DataFrame cargado con shape {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return pd.DataFrame()

    def obtener_columnas(self):
        return list(self.df.columns) if not self.df.empty else []