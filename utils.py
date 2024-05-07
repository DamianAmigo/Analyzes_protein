import tifffile
import cv2
import os 
import openpyxl



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

#obtiene un machote de todas las carpetas y archivos
def obtener_lista_directorio(directorio):
    """Función para obtener recursivamente una lista de carpetas y archivos en un directorio."""
    # Obtener la ruta absoluta del directorio especificado
    ruta_absoluta = os.path.abspath(directorio)

    # Verificar si el directorio es válido
    if not os.path.isdir(ruta_absoluta):
        print(f"Error: El directorio '{directorio}' no es válido.")
        return None

    # Obtener el nombre del directorio base
    nombre_directorio_base = os.path.basename(ruta_absoluta)

    lista_contenido = []

    # Recorrer el directorio y sus subdirectorios de manera recursiva
    for ruta_actual, carpetas, archivos in os.walk(ruta_absoluta):
        # Obtener la ruta relativa del directorio actual con respecto al directorio base
        ruta_relativa = os.path.relpath(ruta_actual, ruta_absoluta)

        contenido_directorio = {
            "ruta": ruta_relativa,
            "carpetas": carpetas,
            "archivos": archivos
        }
        lista_contenido.append(contenido_directorio)

    return lista_contenido

#devuelvo una lista completa con rutas de los archivos CREO QUE NO SE VA A USAR
def recorrer_arbol(arbol, urls="imagenes/"):
    
    lista_ordenada_archivos=[]
    url=urls     
    for elemento in arbol:
        if elemento['ruta']!=".":
            url = elemento['ruta']
        
        
        if elemento['carpetas'] == []:
            for subelemento in elemento['archivos']:
                lista_ordenada_archivos.append(url+"/"+subelemento)
        else:
            print(url)

    return lista_ordenada_archivos

#recibe una lista con todos los archivos de una carpeta y nos devuelve una lista con
#los archivos organizados por slices
def agrupar_por_slice(lista_archivos):
    # Creamos un diccionario para agrupar los archivos por número final
    archivos_por_numero = {}

    for archivo in lista_archivos:
        # Dividimos el nombre del archivo para extraer la parte relevante (el número)
        partes = archivo.split()
        if len(partes) > 1:
            nombre_archivo = partes[-1]  # Esto asume que el número está al final después del último espacio
            numero = nombre_archivo.split('.')[0]  # Eliminamos la extensión .tif para obtener el número
            if numero not in archivos_por_numero:
                archivos_por_numero[numero] = []
            archivos_por_numero[numero].append(archivo)

    # Filtramos y devolvemos solo los archivos con el mismo número final
    archivos_filtrados = [archivos for archivos in archivos_por_numero.values() if len(archivos) > 1]

    return archivos_filtrados

def celdas(columna:str,fila:int ):
    return columna+str(fila)

def crear_excel(dicc_excel):
    # Crear un nuevo libro de Excel
    libro = openpyxl.Workbook()

    # Obtener la hoja activa (por defecto, será la primera hoja del nuevo libro)
    hoja = libro.active
    
    # Iterar sobre las claves y valores del diccionario
    for celda, valor in dicc_excel.items():
        hoja[celda] = valor

    nombre_archivo = 'datos.xlsx'
    libro.save(nombre_archivo)
