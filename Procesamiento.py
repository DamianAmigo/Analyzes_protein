import cv2
import numpy as np

def procesar(image_path, blockSize=23, C=-1):
    """Aplica procesamiento de umbral adaptativo con GAUSSIAN_C seguido por Otsu y realiza la intersección con la imagen original."""
    
    # Cargar la imagen
    img_original = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convertir la imagen original a escala de grises
    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización adaptativa con GAUSSIAN_C
    adaptive_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)

    # Aplicar umbralización de Otsu al resultado de la umbralización adaptativa
    _, otsu_thresh = cv2.threshold(adaptive_thresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aplicar la máscara otsu_thresh a la imagen original en color
    img_interseccion = cv2.bitwise_and(img_original, img_original, mask=otsu_thresh)

    area_final = cv2.countNonZero(otsu_thresh)

    return img_interseccion, area_final