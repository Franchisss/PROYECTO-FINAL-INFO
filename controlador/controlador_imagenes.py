import cv2
import nibabel as nib
import pydicom
import os 
from modelo.procesador_imagenes import (
    aplicar_binarizacion,
    aplicar_morfologia,
    aplicar_todas_morfologias,
    cambiar_espacio_color,
    aplicar_ecualizacion,
    contar_elementos, 
    reconstruir_volumen_dicom, convertir_dicom_a_nifti, insertar_dicom_nifti, detectar_esquinas 
    )

class ControladorImagenes:
    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.imagen_original = cv2.imread(ruta_imagen)

    # ========== BINARIZACIÓN ==========
    def aplicar_binarizacion(self, umbral):
        return aplicar_binarizacion(self.imagen_original, umbral)

    # ========== MORFOLOGÍA ==========
    def aplicar_morfologia(self, tipo, kernel):
        return aplicar_morfologia(self.imagen_original, tipo, kernel)

    def aplicar_todas_morfologias(self, kernel):
        return aplicar_todas_morfologias(self.imagen_original, kernel)

    # ========== ESPACIOS DE COLOR ==========
    def aplicar_espacio_color(self, tipo):
        return cambiar_espacio_color(self.imagen_original, tipo)

    # ========== ECUALIZACIÓN ==========
    def aplicar_ecualizacion(self):
        return aplicar_ecualizacion(self.imagen_original)

    # ========== CONTEO ==========
    def contar_elementos(self):
        return contar_elementos(self.imagen_original)
    
    def detectar_esquinas(self):
        return detectar_esquinas(self.imagen_original)

#---------parte dicom-------------

class ControladorDICOM:
    def __init__(self, carpeta_dicom):
        self.carpeta = carpeta_dicom
        self.volumen = reconstruir_volumen_dicom(carpeta_dicom)
        self.nifti = None
        self.ruta_nifti = None

    def convertir_a_nifti(self):
        self.nifti = convertir_dicom_a_nifti(self.carpeta)
        return self.nifti

    def guardar_nifti(self, ruta):
        import nibabel as nib
        if self.nifti:
            nib.save(self.nifti, ruta)
            self.ruta_nifti = ruta
            self.insertar_en_base_de_datos()

    def insertar_en_base_de_datos(self):
        # Tomamos el primer archivo DICOM para extraer los metadatos
        primer_dcm = None
        for archivo in os.listdir(self.carpeta):
            if archivo.lower().endswith(".dcm"):
                primer_dcm = os.path.join(self.carpeta, archivo)
                break

        if not primer_dcm:
            return

        ds = pydicom.dcmread(primer_dcm)

        datos = {
            "nombre": str(ds.get("PatientName", "Desconocido")),
            "id": str(ds.get("PatientID", "N/A")),
            "edad": int(ds.get("PatientAge", "000Y")[:3]),
            "sexo": str(ds.get("PatientSex", "N")),
            "ruta_dicom": self.carpeta,
            "ruta_nifti": self.ruta_nifti
        }

        insertar_dicom_nifti(datos)

    




