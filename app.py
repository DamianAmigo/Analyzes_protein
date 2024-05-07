
from utils import  obtener_lista_directorio, agrupar_por_slice, celdas, crear_excel
from Procesamiento import  procesar

rutas=["imagenes/DAPI 1-1.tif", "imagenes/DCX 1-1.tif", "imagenes/MAP2 1-1.tif", "imagenes/SOX2 1-1.tif"]
url_base="imagenes/"
areas=[]
imagenes=[]
resultado_archivo=[]
titulo=""
fila=1
columna_nombre="A"
columna_area="B"
columna_porcentaje="C"
codicion_control=True
dicc_excel={ 'A2': 'Canal', 
             'B2': 'superficie',
             'C2': '%',
             'F2': 'Canal', 
             'G2': 'superficie',
             'H2': '%'}

arbol=obtener_lista_directorio(url_base)

for elementos in arbol:
    fila=fila+1
    dicc_excel[celdas(columna_nombre,fila)]=elementos["ruta"]    
    if elementos["ruta"] != ".":
        if elementos["carpetas"] !=[]:
            titulo=elementos["ruta"]
            if codicion_control:
                dicc_excel[celdas(columna_nombre,fila)]=titulo
                fila=3
                codicion_control=False
            else:
                columna_nombre="F"                
                columna_area="G"
                columna_porcentaje="H"
                dicc_excel[celdas(columna_nombre,1)]=titulo
                fila=3

        else:
            #TODO se deberia procesar el dAPi primero para tomar el !00% antes de hacer calculos con otros archivos
            #ahora tenemos al deficiencia que si pones un archivo con una letra anterior alfabeticamente se procesara 
            #primero y no tendrimos el valor del 100% del area.
            url_base=url_base+elementos["ruta"]
            for grupo in agrupar_por_slice(elementos["archivos"]):
                fila=fila+1
                tempo_area_porcentual=0
                for nom_archivo in grupo:
                    print("analizando:"+nom_archivo+" en "+elementos["ruta"])
                    contorno,area_pix= procesar(url_base+"/"+nom_archivo)                    
                    resultado_archivo.append(nom_archivo)
                    resultado_archivo.append(area_pix)
                    resultado_archivo.append(contorno)
                    
                    
                    
                    if resultado_archivo[0][0:4]=="DAPI":
                        tempo_area_porcentual=resultado_archivo[1]  
                    print(f'{resultado_archivo[0]}: {resultado_archivo[1]}, porcentaje: {round((resultado_archivo[1]*100)/(tempo_area_porcentual+1), 2)}%')
                    dicc_excel[celdas(columna_nombre,fila)]=resultado_archivo[0]
                    dicc_excel[celdas(columna_area,fila)]=resultado_archivo[1]
                    dicc_excel[celdas(columna_porcentaje,fila)]=round((resultado_archivo[1]*100)/(tempo_area_porcentual))
                    resultado_archivo.clear()
                    fila= fila+1
                

    # Encontrar la posición en la cadena
    posicion = url_base.find(titulo)

    # Mantener la parte de la cadena desde el inicio hasta la posición de "\\1" (incluyendo "\\1")
    url_base="imagenes/"
       

crear_excel(dicc_excel)