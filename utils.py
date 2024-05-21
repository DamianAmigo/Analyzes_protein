import tifffile
import cv2
import os 
import openpyxl

def resolucion_espacial(ruta_imagen):
    # Read image metadata
    metadata = tifffile.TiffFile(ruta_imagen).pages[0].tags

    # Get spatial resolution and units of measure
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

    # Print spatial resolution
    if x_res is not None and y_res is not None and res_unit is not None:
        print(f"Each pixel represents {x_res:.2f}x{y_res:.2f} {res_unit}")
    else:
        print("No spatial resolution metadata found")

def resize_image(img, max_width=1500):
    """Resize an image proportionally with a given maximum width."""  
    if img is None:
        print(f"Error: Could not load the image")
        return None
    
    # Get the original dimensions of the image
    height, width = img.shape[:2]
    
    # Calculate the scale factor to adjust the width to max_width
    scale_factor = max_width / width
    
    # Calculate the new proportional height
    new_height = int(height * scale_factor)
    
    # Resize the image with the new height and maximum width
    resized_img = cv2.resize(img, (max_width, new_height))
    
    return resized_img

def es_imagen_valida(nombre_archivo):
    """
    Check if a file name corresponds to a valid image extension.

    Args:
        nombre_archivo (str): File name.

    Returns:
        bool: True if the file extension indicates it is a valid image, False otherwise.
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
    return os.path.splitext(nombre_archivo)[1].lower() in valid_extensions

# Get a template of all folders and files
def obtener_lista_directorio(directorio):
    """Function to recursively obtain a list of folders and files in a directory."""
    # Get the absolute path of the specified directory
    ruta_absoluta = os.path.abspath(directorio)

    # Check if the directory is valid
    if not os.path.isdir(ruta_absoluta):
        print(f"Error: The directory '{directorio}' is not valid.")
        return None

    # Get the name of the base directory
    nombre_directorio_base = os.path.basename(ruta_absoluta)

    lista_contenido = []

    # Traverse the directory and its subdirectories recursively
    for ruta_actual, carpetas, archivos in os.walk(ruta_absoluta):
        # Get the relative path of the current directory with respect to the base directory
        ruta_relativa = os.path.relpath(ruta_actual, ruta_absoluta)

        contenido_directorio = {
            "ruta": ruta_relativa,
            "carpetas": carpetas,
            "archivos": archivos
        }
        lista_contenido.append(contenido_directorio)

    return lista_contenido

# Return a complete list with file paths (I THINK IT WILL NOT BE USED)
def recorrer_arbol(arbol, urls="imagenes/"):
    ordered_file_list = []
    url = urls     
    for elemento in arbol:
        if elemento['ruta'] != ".":
            url = elemento['ruta']
        
        if elemento['carpetas'] == []:
            for subelemento in elemento['archivos']:
                ordered_file_list.append(url + "/" + subelemento)
        else:
            print(url)

    return ordered_file_list

# Receives a list of all files in a folder and returns a list of files organized by slices
def agrupar_por_slice(lista_archivos):
    # Create a dictionary to group files by final number
    archivos_por_numero = {}

    for archivo in lista_archivos:
        # Split the file name to extract the relevant part (the number)
        partes = archivo.split()
        if len(partes) > 1:
            nombre_archivo = partes[-1]  # This assumes that the number is at the end after the last space
            numero = nombre_archivo.split('.')[0]  # Remove the .tif extension to get the number
            if numero not in archivos_por_numero:
                archivos_por_numero[numero] = []
            archivos_por_numero[numero].append(archivo)

    # Filter and return only files with the same final number
    archivos_filtrados = [archivos for archivos in archivos_por_numero.values() if len(archivos) > 1]

    return archivos_filtrados

def celdas(columna: str, fila: int):
    return columna + str(fila)

def crear_excel(dicc_excel):
    # Create a new Excel workbook
    libro = openpyxl.Workbook()

    # Get the active sheet (by default, it will be the first sheet of the new workbook)
    hoja = libro.active
    
    # Iterate over the keys and values of the dictionary
    for celda, valor in dicc_excel.items():
        hoja[celda] = valor

    nombre_archivo = 'datos.xlsx'
    libro.save(nombre_archivo)
