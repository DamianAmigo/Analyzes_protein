import tifffile
import cv2
import os 



def resolucion_espacial(ruta_imagen):

    # Lee los metadatos de la imagen
    metadata = tifffile.TiffFile(ruta_imagen).pages[0].tags

    # Obtiene la resolución espacial y las unidades de medida
    res_unit = None
    x_res = None
    y_res = None
    for tag in metadata:
        if tag.name == 'XResolution':
            x_res = tag.value[0] / tag.value[1]
        elif tag.name == 'YResolution':
            y_res = tag.value[0] / tag.value[1]
        elif tag.name == 'ResolutionUnit':
            res_unit = tifffile.TIFF.RESUNIT(tag.value)

    # Imprime la resolución espacial
    if x_res is not None and y_res is not None and res_unit is not None:
        print(f"Cada pixel representa {x_res:.2f}x{y_res:.2f} {res_unit}")
    else:
        print("No se encontraron metadatos de resolución espacial")



def resize_image(img, max_width=1500):
    """Redimensiona una imagen proporcionalmente con un ancho máximo dado."""  

    if img is None:
        print(f"Error: No se pudo cargar la imagen ")
        return None
    
    # Obtener las dimensiones originales de la imagen
    height, width = img.shape[:2]
    
    # Calcular el factor de escala para ajustar el ancho a max_width
    scale_factor = max_width / width
    
    # Calcular la nueva altura proporcional
    new_height = int(height * scale_factor)
    
    # Redimensionar la imagen con la nueva altura y ancho máximo
    resized_img = cv2.resize(img, (max_width, new_height))
    
    return resized_img

def obtener_rutas_imagenes(directorio):
    """
    Recorre de forma recursiva un directorio y sus subdirectorios para obtener
    las rutas completas de todas las imágenes encontradas.

    Args:
        directorio (str): Ruta del directorio raíz a analizar.

    Returns:
        dict: Diccionario donde las claves son nombres de archivo y los valores son rutas completas.
    """
    diccionario_rutas = {}
    
    # Verificar si el directorio existe
    if not os.path.isdir(directorio):
        print(f"Error: El directorio '{directorio}' no existe.")
        return diccionario_rutas
    
    # Recorrer todos los elementos (archivos y directorios) en el directorio
    for elemento in os.listdir(directorio):
        ruta_elemento = os.path.join(directorio, elemento)
        
        # Si es un archivo y es una imagen válida, agregar al diccionario de rutas
        if os.path.isfile(ruta_elemento) and es_imagen_valida(elemento):
            diccionario_rutas[elemento] = ruta_elemento
        
        # Si es un directorio, llamar recursivamente a la función para explorar subdirectorios
        elif os.path.isdir(ruta_elemento):
            diccionario_rutas.update(obtener_rutas_imagenes(ruta_elemento))
    
    return diccionario_rutas

def es_imagen_valida(nombre_archivo):
    """
    Verifica si un nombre de archivo corresponde a una extensión de imagen válida.

    Args:
        nombre_archivo (str): Nombre del archivo.

    Returns:
        bool: True si la extensión del archivo indica que es una imagen válida, False en caso contrario.
    """
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
    return os.path.splitext(nombre_archivo)[1].lower() in extensiones_validas



