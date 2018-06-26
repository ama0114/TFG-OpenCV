# Seguimiento de lineas basado en OpenCV para AGVs

El objetivo del proyecto es guiar a un robot agv mediante la detección de una linea en el suelo. Se usará una cámara para 
que el robot pueda "ver" esa linea, y se procesará la imagen para dar instrucciónes sobre que dirección debe de tomar.
Para el procesamiento de imagenes usaremos OpenCV en su versión 3.3.0 en conjunto con python 2.7.15.

*********Requisitos Python:************  
OpenCV  
MatPlotLib  
Numpy  
SciPy  
Urllib (incluida con Python)  
Time (incluida con Python)  

***********Creación del ejecutable.***************  
Necesitamos tener instalado en Python pyinstaller  
Nos colocamos sobre la carpeta src y ejecutamos: pyinstaller ejecucion.spec  
Se crearán dos carpetas, build y dist. Nuestro ejecutable es: dist/ejecucion/ejecucion.exe  
Se necesita distribuir tal cual está la carpeta de ejecucion, con todo lo que contiene dentro  
