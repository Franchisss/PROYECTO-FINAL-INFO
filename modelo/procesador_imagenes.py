import cv2
import numpy as np
import pydicom 
import os 
import nibabel as nib 
import mysql.connector

# ========== BINARIZACIÓN ==========
def aplicar_binarizacion(imagen_bgr, umbral):
    gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(gris, umbral, 255, cv2.THRESH_BINARY)
    return binaria

# ========== MORFOLOGÍA ==========
def aplicar_morfologia(imagen_bgr, tipo, tamano_kernel):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamano_kernel, tamano_kernel))
    if tipo == "apertura":
        return cv2.morphologyEx(imagen_bgr, cv2.MORPH_OPEN, kernel)
    elif tipo == "cierre":
        return cv2.morphologyEx(imagen_bgr, cv2.MORPH_CLOSE, kernel)
    elif tipo == "dilatacion":
        return cv2.dilate(imagen_bgr, kernel, iterations=1)
    elif tipo == "erosion":
        return cv2.erode(imagen_bgr, kernel, iterations=1)
    elif tipo == "gradiente":
        return cv2.morphologyEx(imagen_bgr, cv2.MORPH_GRADIENT, kernel)
    elif tipo == "blackhat":
        return cv2.morphologyEx(imagen_bgr, cv2.MORPH_BLACKHAT, kernel)
    elif tipo == "tophat":
        return cv2.morphologyEx(imagen_bgr, cv2.MORPH_TOPHAT, kernel)
    else:
        return imagen_bgr

def aplicar_todas_morfologias(imagen_bgr, tamano_kernel):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamano_kernel, tamano_kernel))
    resultado = imagen_bgr.copy()
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_OPEN, kernel)
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_CLOSE, kernel)
    resultado = cv2.dilate(resultado, kernel, iterations=1)
    resultado = cv2.erode(resultado, kernel, iterations=1)
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_GRADIENT, kernel)
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_BLACKHAT, kernel)
    resultado = cv2.morphologyEx(resultado, cv2.MORPH_TOPHAT, kernel)
    return resultado

# ========== ESPACIOS DE COLOR ==========
def cambiar_espacio_color(imagen_bgr, tipo):
    if tipo == "rgb":
        return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    elif tipo == "grises":
        return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
    elif tipo == "hsv":
        return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)
    elif tipo == "lab":
        return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2Lab)
    else:
        return imagen_bgr

# ========== ECUALIZACIÓN ==========
def aplicar_ecualizacion(imagen_bgr):
    img_yuv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    ecualizada = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return ecualizada

# ========== CONTEO ==========
def contar_elementos(imagen_bgr):
    # 1. Escala de grises
    gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

    # 2. Ecualización
    ecualizada = cv2.equalizeHist(gris)

    # 3. Morfología (cierre)
    kernel = np.ones((3, 3), np.uint8)
    morfologica = cv2.dilate(ecualizada, kernel, iterations=2)
    morfologica = cv2.erode(morfologica, kernel, iterations=2)

    # 4. Binarización invertida
    _, binaria = cv2.threshold(morfologica, 125, 255, cv2.THRESH_BINARY_INV)

    # 5. Etiquetado
    num_componentes, etiquetas = cv2.connectedComponents(binaria)

    if num_componentes <= 1:
        return None  # Nada que contar

    # 6. Convertir imagen procesada (morfológica) a BGR para etiquetar en color
    salida = cv2.cvtColor(morfologica, cv2.COLOR_GRAY2BGR)

    # 7. Etiquetar cada componente (excepto fondo)
    for i in range(1, num_componentes):
        mascara = (etiquetas == i).astype(np.uint8) * 255
        M = cv2.moments(mascara)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(salida, str(i), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 1)

    return salida

#--------parte de dicom-------------

def reconstruir_volumen_dicom(carpeta_dicom):
    archivos = [
        os.path.join(carpeta_dicom, f)
        for f in os.listdir(carpeta_dicom)
        if f.lower().endswith(".dcm")
    ]

    dicoms = []

    for archivo in archivos:
        try:
            ds = pydicom.dcmread(archivo)
            if hasattr(ds, "InstanceNumber"):
                dicoms.append((ds.InstanceNumber, ds))
        except:
            continue

    # Ordenar por número de corte
    dicoms.sort(key=lambda x: x[0])

    # Extraer los arrays
    cortes = [ds.pixel_array for _, ds in dicoms]

    if not cortes:
        return None  # si está vacío

    # Convertir lista de cortes a volumen 3D
    volumen = np.stack(cortes)  # forma: (Z, Y, X)
    return volumen

def convertir_dicom_a_nifti(carpeta_dicom):
    archivos = [os.path.join(carpeta_dicom, f) for f in os.listdir(carpeta_dicom) if f.lower().endswith(".dcm")]
    dicoms = []

    for archivo in archivos:
        try:
            ds = pydicom.dcmread(archivo)
            if hasattr(ds, "InstanceNumber"):
                dicoms.append((ds.InstanceNumber, ds))
        except:
            continue

    dicoms.sort(key=lambda x: x[0])
    cortes = [ds.pixel_array for _, ds in dicoms]

    volumen = np.stack(cortes)  # Volumen 3D
    nifti = nib.Nifti1Image(volumen, affine=np.eye(4))  # Se puede ajustar el affine si es necesario
    return nifti

def insertar_dicom_nifti(datos):
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",  # o el que tengas
        password="",  # o tu contraseña
        database="proyecto3"
    )
    cursor = conexion.cursor()

    query = """
        INSERT INTO dicom_nifti (
            nombre_paciente, identificacion, edad, sexo,
            ruta_dicom, ruta_nifti, fecha_subida
        ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """

    valores = (
        datos["nombre"],
        datos["id"],
        datos["edad"],
        datos["sexo"],
        datos["ruta_dicom"],
        datos["ruta_nifti"]
    )

    cursor.execute(query, valores)
    conexion.commit()
    cursor.close()
    conexion.close()