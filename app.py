from utils import obtener_lista_directorio, agrupar_por_slice, celdas, crear_excel
from Procesamiento import procesar

url_base = "imagenes/"
areas = []
imagenes = []
resultado_archivo = []
titulo = ""
fila = 1
columna_nombre = "A"
columna_area = "B"
columna_porcentaje = "C"
codicion_control = True
dicc_excel = { 
    'A2': 'Canal', 
    'B2': 'superficie',
    'C2': '%',
    'F2': 'Canal', 
    'G2': 'superficie',
    'H2': '%'
}

arbol = obtener_lista_directorio(url_base)

for elementos in arbol:
    fila += 1
    dicc_excel[celdas(columna_nombre, fila)] = elementos["ruta"]    
    if elementos["ruta"] != ".":
        if elementos["carpetas"] != []:
            titulo = elementos["ruta"]
            if codicion_control:
                dicc_excel[celdas(columna_nombre, fila)] = titulo
                fila = 3
                codicion_control = False
            else:
                columna_nombre = "F"                
                columna_area = "G"
                columna_porcentaje = "H"
                dicc_excel[celdas(columna_nombre, 1)] = titulo
                fila = 3

        else:
            # TODO: DAPI should be processed first to take 100% before making calculations with other files
            # Currently, if you put a file with an earlier alphabetical letter it will be processed first 
            # and we will not have the 100% area value.
            url_base = url_base + elementos["ruta"]
            for grupo in agrupar_por_slice(elementos["archivos"]):
                fila += 1
                tempo_area_porcentual = 0
                for nom_archivo in grupo:
                    print("analyzing:" + nom_archivo + " in " + elementos["ruta"])
                    contorno, area_pix = procesar(url_base + "/" + nom_archivo)                    
                    resultado_archivo.append(nom_archivo)
                    resultado_archivo.append(area_pix)
                    resultado_archivo.append(contorno)
                    
                    if resultado_archivo[0][0:4] == "DAPI":
                        tempo_area_porcentual = resultado_archivo[1]  
                    print(f'{resultado_archivo[0]}: {resultado_archivo[1]}, percentage: {round((resultado_archivo[1] * 100) / (tempo_area_porcentual + 1), 2)}%')
                    dicc_excel[celdas(columna_nombre, fila)] = resultado_archivo[0]
                    dicc_excel[celdas(columna_area, fila)] = resultado_archivo[1]
                    dicc_excel[celdas(columna_porcentaje, fila)] = round((resultado_archivo[1] * 100) / tempo_area_porcentual)
                    resultado_archivo.clear()
                    fila += 1

    # Find the position in the string
    posicion = url_base.find(titulo)

    # Keep the part of the string from the beginning to the position of "\\1" (including "\\1")
    url_base = "imagenes/"
       
crear_excel(dicc_excel)
