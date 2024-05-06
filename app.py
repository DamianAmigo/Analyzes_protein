import cv2
from utils import resize_image
from Procesamiento import  procesar

rutas=["imagenes/DAPI 1-1.tif", "imagenes/DCX 1-1.tif", "imagenes/MAP2 1-1.tif", "imagenes/SOX2 1-1.tif"]
areas=[]
imagenes=[]

for ruta in rutas:
    
    contorno,_= procesar(ruta)
    areas.append(_)
    imagenes.append(contorno)


print(f'DAPI: {areas[0]}, porcentaje: 100 %')
print(f'MAP2: {areas[2]}, porcentaje: {round((areas[2]*100)/(areas[0]+1), 2)}%')
print(f'DCX:  {areas[1]}, porcentaje: {round((areas[1]*100)/(areas[0]+1), 2)}%')
print(f'SOX2: {areas[3]}, porcentaje: {round((areas[3]*100)/(areas[0]+1), 2)}%')



cv2.imshow("DAPI", resize_image(imagenes[0]))
cv2.imshow("MAP2", resize_image(imagenes[2]))
cv2.imshow("Dcx", resize_image(imagenes[1]))
cv2.imshow("sox2", resize_image(imagenes[3]))
cv2.waitKey(0)
cv2.destroyAllWindows()