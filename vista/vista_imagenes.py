from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from controlador.controlador_imagenes import ControladorImagenes
from controlador.controlador_imagenes import ControladorDICOM
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import cv2
import numpy as np

# ================== MENÚ PRINCIPAL ==================
class InterfazImagenes(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/interfaz_imagenes.ui", self)

        # Botón para seleccionar JPG/PNG
        self.boton_jpgpng = self.findChild(QtWidgets.QPushButton, "JPGPNG")
        self.boton_jpgpng.clicked.connect(self.abrir_explorador)
        #Boton para seleccion DICOM
        self.boton_dicom = self.findChild(QtWidgets.QPushButton, "DICOM")
        self.boton_dicom.clicked.connect(self.abrir_dicom)


    def abrir_explorador(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg)")
        if ruta:
            self.ventana = InterfazJPGPNG(ruta)
            self.ventana.show()
            self.close()
    
    def abrir_dicom(self):
        self.ventana = InterfazDICOM()
        self.ventana.show()
        self.close()


# ================== MENÚ DE OPERACIONES IMAGENES JPG/PNG ==================
class InterfazJPGPNG(QtWidgets.QMainWindow):
    def __init__(self, ruta_imagen):
        super().__init__()
        uic.loadUi("vista/interfaz_JPGPNG.ui", self)
        self.ruta_imagen = ruta_imagen
        self.controlador = ControladorImagenes(self.ruta_imagen)

        # PRUEBA para mostrar todos los objetos cargados
        for widget in self.findChildren(QtWidgets.QPushButton):
            print("BOTÓN DETECTADO:", widget.objectName())

        self.boton_binarizar = self.findChild(QtWidgets.QPushButton, "bnt_binarizar")
        if self.boton_binarizar is None:
            print("NO SE ENCONTRÓ 'bnt_binarizar'")
        else:
            print("Se encontró 'bnt_binarizar'")
            self.boton_binarizar.clicked.connect(self.abrir_binarizacion)

        # Conectar botones por su objectName exacto
        self.boton_binarizar = self.findChild(QtWidgets.QPushButton, "bnt_binarizar")
        self.boton_binarizar.clicked.connect(self.abrir_binarizacion)
        self.findChild(QtWidgets.QPushButton, "bnt_morfologia").clicked.connect(self.abrir_morfologia)
        self.findChild(QtWidgets.QPushButton, "bnt_color").clicked.connect(self.abrir_color)
        self.findChild(QtWidgets.QPushButton, "bnt_ecualizar").clicked.connect(self.abrir_ecualizacion)
        self.findChild(QtWidgets.QPushButton, "bnt_contar").clicked.connect(self.abrir_conteo)
        self.findChild(QtWidgets.QPushButton, "bnt_esquinas").clicked.connect(self.abrir_esquinas)

    def abrir_binarizacion(self):
        self.ventana = InterfazBinarizacion(self.ruta_imagen)
        self.ventana.show()
        self.close()

    def abrir_morfologia(self):
        self.ventana = InterfazMorfologia(self.ruta_imagen)
        self.ventana.show()
        self.close()

    def abrir_color(self):
        self.ventana = InterfazColor(self.ruta_imagen)
        self.ventana.show()
        self.close()

    def abrir_ecualizacion(self):
        self.ventana = InterfazEcualizacion(self.ruta_imagen)
        self.ventana.show()
        self.close()
    
    def abrir_conteo(self):
        resultado = self.controlador.contar_elementos()
        self.ventana = InterfazConteo(resultado)
        self.ventana.show()
        self.close()
    
    def abrir_esquinas(self):
        resultado = self.controlador.detectar_esquinas()
        self.ventana = InterfazImagenEsquina(resultado)
        self.ventana.show()
        self.close()


class InterfazBinarizacion(QtWidgets.QMainWindow):
    def __init__(self, ruta_imagen):
        super().__init__()
        uic.loadUi("vista/interfaz_binarizacion.ui", self)
        self.ruta_imagen = ruta_imagen
        self.controlador = ControladorImagenes(self.ruta_imagen)

        self.spin = self.findChild(QtWidgets.QSpinBox, "numero")
        self.spin.setRange(1, 255)
        self.spin.setSingleStep(2)  # Solo impares

        self.boton_binarizar = self.findChild(QtWidgets.QPushButton, "aceptar")  # Ajusta este nombre según tu .ui
        self.boton_cancelar = self.findChild(QtWidgets.QPushButton, "cancelar")    # Ajusta este nombre también

        if self.boton_binarizar:
            self.boton_binarizar.clicked.connect(self.aplicar_binarizacion)
        if self.boton_cancelar:
            self.boton_cancelar.clicked.connect(self.volver_a_menu)

    def aplicar_binarizacion(self):
        umbral = self.spin.value()
        imagen_binaria = self.controlador.aplicar_binarizacion(umbral)
        self.ventana = InterfazImagenBinarizacion(imagen_binaria)
        self.ventana.show()
        self.close()

    def volver_a_menu(self):
        self.ventana = InterfazJPGPNG(self.ruta_imagen)
        self.ventana.show()
        self.close()

class InterfazImagenBinarizacion(QtWidgets.QMainWindow):
    def __init__(self, imagen_binaria):
        super().__init__()
        uic.loadUi("vista/interfaz_imagen_binarizacion.ui", self)

        self.label = self.findChild(QtWidgets.QLabel, "imagen_binarizacion")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")  # ← busca el botón
        self.imagen_binaria = imagen_binaria

        self.mostrar_imagen()

        if self.boton_guardar:
            self.boton_guardar.clicked.connect(self.guardar_imagen)  # ← lo conecta a la función

    def mostrar_imagen(self):
        if self.imagen_binaria is not None and self.label is not None:
            h, w = self.imagen_binaria.shape
            qimg = QImage(self.imagen_binaria.data, w, h, w, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)
    
    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "guardar", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.imagen_binaria)

class InterfazMorfologia(QtWidgets.QMainWindow):
    def __init__(self, ruta_imagen):
        super().__init__()
        uic.loadUi("vista/interfaz_morfologia.ui", self)
        self.ruta_imagen = ruta_imagen
        self.controlador = ControladorImagenes(ruta_imagen)
        self.kernel_input = self.findChild(QtWidgets.QSpinBox, "numero")
        self.kernel_input.setRange(1, 255)
        self.kernel_input.setSingleStep(2)


        # Lista de botones
        self.botones = {
            "apertura": self.findChild(QtWidgets.QPushButton, "bnt_apertura"),
            "cierre": self.findChild(QtWidgets.QPushButton, "bnt_cierre"),
            "dilatacion": self.findChild(QtWidgets.QPushButton, "bnt_dilatacion"),
            "erosion": self.findChild(QtWidgets.QPushButton, "bnt_erosion"),
            "gradiente": self.findChild(QtWidgets.QPushButton, "bnt_gradiente"),
            "blackhat": self.findChild(QtWidgets.QPushButton, "bnt_blackhat"),
            "tophat": self.findChild(QtWidgets.QPushButton, "bnt_tophat"),
            "todas": self.findChild(QtWidgets.QPushButton, "bnt_todas"),
        }

        self.boton_aceptar = self.findChild(QtWidgets.QPushButton, "aceptar")
        self.boton_cancelar = self.findChild(QtWidgets.QPushButton, "cancelar")

        self.boton_seleccionado = None

        for nombre, boton in self.botones.items():
            boton.clicked.connect(lambda _, n=nombre: self.seleccionar_boton(n))

        if self.boton_aceptar:
            self.boton_aceptar.clicked.connect(self.aplicar_operacion)

        if self.boton_cancelar:
            self.boton_cancelar.clicked.connect(self.volver)

    def seleccionar_boton(self, nombre_boton):
        if self.boton_seleccionado == nombre_boton:
            self.boton_seleccionado = None
            self.botones[nombre_boton].setStyleSheet("")
        else:
            self.boton_seleccionado = nombre_boton
            for nombre, boton in self.botones.items():
                if nombre == nombre_boton:
                    boton.setStyleSheet("background-color: green")
                else:
                    boton.setStyleSheet("")

    def aplicar_operacion(self):
        if self.boton_seleccionado is None:
            return

        kernel = self.kernel_input.value()

        if self.boton_seleccionado == "todas":
            resultado = self.controlador.aplicar_todas_morfologias(kernel)
        else:
            resultado = self.controlador.aplicar_morfologia(self.boton_seleccionado, kernel)

        self.ventana = InterfazImagenMorfologia(resultado)
        self.ventana.show()
        self.close()

    def volver(self):
        self.ventana = InterfazJPGPNG(self.ruta_imagen)
        self.ventana.show()
        self.close()

class InterfazImagenMorfologia(QtWidgets.QMainWindow):
    def __init__(self, imagen_resultado):
        super().__init__()
        uic.loadUi("vista/interfaz_imagen_morfologia.ui", self)

        self.imagen_resultado = imagen_resultado
        self.label = self.findChild(QtWidgets.QLabel, "imagen")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.mostrar_imagen()
        self.boton_guardar.clicked.connect(self.guardar_imagen)

    def mostrar_imagen(self):
        if self.imagen_resultado is not None and self.label is not None:
            if len(self.imagen_resultado.shape) == 2:  # imagen en escala de grises
                h, w = self.imagen_resultado.shape
                qimg = QImage(self.imagen_resultado.data, w, h, w, QImage.Format_Grayscale8)
            else:  # imagen en color
                h, w, ch = self.imagen_resultado.shape
                bytes_per_line = ch * w
                qimg = QImage(self.imagen_resultado.data, w, h, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.imagen_resultado)

class InterfazColor(QtWidgets.QMainWindow):
    def __init__(self, ruta_imagen):
        super().__init__()
        uic.loadUi("vista/interfaz_color.ui", self)
        self.ruta_imagen = ruta_imagen
        self.controlador = ControladorImagenes(ruta_imagen)

        self.botones = {
            "rgb": self.findChild(QtWidgets.QPushButton, "bnt_rgb"),
            "grises": self.findChild(QtWidgets.QPushButton, "bnt_grises"),
            "hsv": self.findChild(QtWidgets.QPushButton, "bnt_hsv"),
            "lab": self.findChild(QtWidgets.QPushButton, "bnt_lab"),
        }

        self.boton_aceptar = self.findChild(QtWidgets.QPushButton, "aceptar")
        self.boton_cancelar = self.findChild(QtWidgets.QPushButton, "cancelar")

        self.boton_seleccionado = None

        for nombre, boton in self.botones.items():
            boton.clicked.connect(lambda _, n=nombre: self.seleccionar_boton(n))

        if self.boton_aceptar:
            self.boton_aceptar.clicked.connect(self.aplicar_espacio_color)

        if self.boton_cancelar:
            self.boton_cancelar.clicked.connect(self.volver)

    def seleccionar_boton(self, nombre_boton):
        if self.boton_seleccionado == nombre_boton:
            self.boton_seleccionado = None
            self.botones[nombre_boton].setStyleSheet("")
        else:
            self.boton_seleccionado = nombre_boton
            for nombre, boton in self.botones.items():
                if nombre == nombre_boton:
                    boton.setStyleSheet("background-color: green")
                else:
                    boton.setStyleSheet("")

    def aplicar_espacio_color(self):
        if self.boton_seleccionado is None:
            return

        resultado = self.controlador.aplicar_espacio_color(self.boton_seleccionado)
        self.ventana = InterfazImagenColor(resultado)
        self.ventana.show()
        self.close()

    def volver(self):
        self.ventana = InterfazJPGPNG(self.ruta_imagen)
        self.ventana.show()
        self.close()

class InterfazImagenColor(QtWidgets.QMainWindow):
    def __init__(self, imagen_color):
        super().__init__()
        uic.loadUi("vista/interfaz_imagen_color.ui", self)

        self.imagen_color = imagen_color
        self.label = self.findChild(QtWidgets.QLabel, "imagen")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.mostrar_imagen()
        self.boton_guardar.clicked.connect(self.guardar_imagen)

    def mostrar_imagen(self):
        if self.imagen_color is not None and self.label is not None:
            if len(self.imagen_color.shape) == 2:
                h, w = self.imagen_color.shape
                qimg = QImage(self.imagen_color.data, w, h, w, QImage.Format_Grayscale8)
            else:
                h, w, ch = self.imagen_color.shape
                bytes_per_line = ch * w
                qimg = QImage(self.imagen_color.data, w, h, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.imagen_color)

class InterfazEcualizacion(QtWidgets.QMainWindow):
    def __init__(self, ruta_imagen):
        super().__init__()
        uic.loadUi("vista/interfaz_ecualizacion.ui", self)

        self.label = self.findChild(QtWidgets.QLabel, "imagen")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.controlador = ControladorImagenes(ruta_imagen)
        self.resultado = self.controlador.aplicar_ecualizacion()

        self.mostrar_imagen()
        self.boton_guardar.clicked.connect(self.guardar_imagen)

    def mostrar_imagen(self):
        if self.resultado is not None and self.label is not None:
            if len(self.resultado.shape) == 2:
                h, w = self.resultado.shape
                qimg = QImage(self.resultado.data, w, h, w, QImage.Format_Grayscale8)
            else:
                h, w, ch = self.resultado.shape
                bytes_per_line = ch * w
                qimg = QImage(self.resultado.data, w, h, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.resultado)

class InterfazConteo(QtWidgets.QMainWindow):
    def __init__(self, imagen_contada):
        super().__init__()
        uic.loadUi("vista/interfaz_conteo.ui", self)

        self.imagen_contada = imagen_contada
        self.label = self.findChild(QtWidgets.QLabel, "imagen")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.mostrar_imagen()
        self.boton_guardar.clicked.connect(self.guardar_imagen)

    def mostrar_imagen(self):
        if self.imagen_contada is not None and self.label is not None:
            h, w, ch = self.imagen_contada.shape
            bytes_per_line = ch * w
            qimg = QImage(self.imagen_contada.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg.rgbSwapped())
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.imagen_contada)

class VentanaAdvertencia(QtWidgets.QMessageBox):
    def __init__(self, mensaje):
        super().__init__()
        self.setWindowTitle("Advertencia")
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.setText(mensaje)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.exec_()

#=================== MENU DE OPERACIONES IMAGENES DICOM ===========================

class InterfazDICOM(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("vista/interfaz_dicom.ui", self)

        self.boton_cargar = self.findChild(QtWidgets.QPushButton, "cargar")
        self.boton_convertir = self.findChild(QtWidgets.QPushButton, "convertir")

        # Conectar acciones
        self.boton_cargar.clicked.connect(self.abrir_y_reconstruir_dicom)
        self.boton_convertir.clicked.connect(self.convertir_a_nifti)

    def abrir_y_reconstruir_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta DICOM")
        if carpeta:
            self.controlador = ControladorDICOM(carpeta)
            cortes = self.controlador.obtener_cortes()
            self.ventana = InterfazSlider(cortes)
            self.ventana.show()
            self.close()
    
    def convertir_a_nifti(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta DICOM")
        if carpeta:
            self.controlador = ControladorDICOM(carpeta)
            self.controlador.convertir_a_nifti()
            self.ventana = InterfazNifti(self.controlador)
            self.ventana.show()
            self.close()

class InterfazSlider(QtWidgets.QMainWindow):
    def __init__(self, volumen_3d):
        super().__init__()
        uic.loadUi("vista/slider.ui", self)

        self.volumen = volumen_3d  # np.ndarray de forma (Z, Y, X)

        self.slider_axial = self.findChild(QtWidgets.QSlider, "axial")
        self.slider_coronal = self.findChild(QtWidgets.QSlider, "coronal")
        self.slider_sagital = self.findChild(QtWidgets.QSlider, "sagital")
        self.label_imagen = self.findChild(QtWidgets.QLabel, "imagen")
        self.label_corte = self.findChild(QtWidgets.QLabel, "corte")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")
        self.boton_cancelar = self.findChild(QtWidgets.QPushButton, "cancelar")

        self.slider_axial.setMaximum(self.volumen.shape[0] - 1)
        self.slider_coronal.setMaximum(self.volumen.shape[1] - 1)
        self.slider_sagital.setMaximum(self.volumen.shape[2] - 1)

        self.slider_axial.valueChanged.connect(lambda: self.mostrar_corte("axial"))
        self.slider_coronal.valueChanged.connect(lambda: self.mostrar_corte("coronal"))
        self.slider_sagital.valueChanged.connect(lambda: self.mostrar_corte("sagital"))
        self.boton_guardar.clicked.connect(self.guardar_corte)
        self.boton_cancelar.clicked.connect(self.volver)

        self.ultimo_plano = "axial"
        self.mostrar_corte("axial")

    def mostrar_corte(self, plano):
        self.ultimo_plano = plano
        if plano == "axial":
            z = self.slider_axial.value()
            corte = self.volumen[z, :, :]
            texto = f"Plano axial: Corte {z + 1} / {self.volumen.shape[0]}"
        elif plano == "coronal":
            y = self.slider_coronal.value()
            corte = self.volumen[:, y, :]
            texto = f"Plano coronal: Corte {y + 1} / {self.volumen.shape[1]}"
        elif plano == "sagital":
            x = self.slider_sagital.value()
            corte = self.volumen[:, :, x]
            texto = f"Plano sagital: Corte {x + 1} / {self.volumen.shape[2]}"
        else:
            return

        # Normalizar corte a 8 bits
        corte = cv2.normalize(corte, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Escalar si es muy pequeño
        if corte.shape[0] < 100 or corte.shape[1] < 100:
            corte = cv2.resize(corte, (corte.shape[1]*6, corte.shape[0]*6), interpolation=cv2.INTER_NEAREST)

        h, w = corte.shape
        qimg = QImage(corte.data, w, h, w, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.label_imagen.setPixmap(pixmap)
        self.label_imagen.setScaledContents(True)
        self.label_corte.setText(texto)

    def guardar_corte(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar corte", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            if self.ultimo_plano == "axial":
                corte = self.volumen[self.slider_axial.value(), :, :]
            elif self.ultimo_plano == "coronal":
                corte = self.volumen[:, self.slider_coronal.value(), :]
            elif self.ultimo_plano == "sagital":
                corte = self.volumen[:, :, self.slider_sagital.value()]
            else:
                return
            corte = cv2.normalize(corte, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            cv2.imwrite(ruta, corte)

    def volver(self):
        self.ventana = InterfazDICOM()
        self.ventana.show()
        self.close()

class InterfazNifti(QtWidgets.QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        uic.loadUi("vista/nifti.ui", self)

        self.controlador = controlador
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.boton_guardar.clicked.connect(self.guardar_archivo)

    def guardar_archivo(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar como NIfTI", "", "NIfTI (*.nii)")
        if ruta:
            self.controlador.guardar_nifti(ruta)
            self.close()

class InterfazImagenEsquina(QtWidgets.QMainWindow):
    def __init__(self, imagen_resultado):
        super().__init__()
        uic.loadUi("vista/interfaz_imagen_esquina.ui", self)

        self.imagen_resultado = imagen_resultado
        self.label = self.findChild(QtWidgets.QLabel, "imagen")
        self.boton_guardar = self.findChild(QtWidgets.QPushButton, "guardar")

        self.mostrar_imagen()
        self.setWindowTitle("Detección de esquinas (Harris)")

        if self.boton_guardar:
            self.boton_guardar.clicked.connect(self.guardar_imagen)

    def mostrar_imagen(self):
        if self.imagen_resultado is not None and self.label is not None:
            if len(self.imagen_resultado.shape) == 2:
                h, w = self.imagen_resultado.shape
                qimg = QImage(self.imagen_resultado.data, w, h, w, QImage.Format_Grayscale8)
            else:
                h, w, ch = self.imagen_resultado.shape
                bytes_per_line = ch * w
                qimg = QImage(self.imagen_resultado.data, w, h, bytes_per_line, QImage.Format_BGR888)

            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

    def guardar_imagen(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "PNG (*.png);;JPG (*.jpg)")
        if ruta:
            cv2.imwrite(ruta, self.imagen_resultado)


