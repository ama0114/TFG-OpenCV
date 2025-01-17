# coding=utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt

def binarizar_otsu(frame, valor_por_encima, modo):
    """
    Funcion que permite binarizar una imagen,
    calculando el umbral de binarizacion segun el algoritmo de Otsu.
    parametros:
    - frame: imagen a binarizar
    - valor_por_encima: valor asignados a los pixeles por encima del umbral
    - modo: metodo para binarizar la imagen.
        - cv2.THRESH_BINARY  => binarizacion normal
        - cv2.THRESH_BINARY_INV => binarizacion inversa

    devuelve la imagen binarizada img_binarizada

    En este caso el umbral es relevante, ya que está calculado por la funcion de otsu.
    """
    #El 0 en el umbral de binarizacion, es debido a que se calcula segun la funcion de otsul.
    umbral, img_binarizada = cv2.threshold(frame, 0, valor_por_encima,
                                           cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    return umbral, img_binarizada

def binarizar_umbral_fijo(frame, umbral, valor_por_encima, modo):
    """Funcion para binarizar una imagen segun un umbral fijo.

    Parametros:
    - frame: Imagen de origen
    - umbral: umbral de binarizacion
    - valor_por_encima: Valor asignado a los pixeles por encima del umbral
     - modo: metodo para binarizar la imagen.
        - cv2.THRESH_BINARY  => binarizacion normal
        - cv2.THRESH_BINARY_INV => binarizacion inversa
        - cv2.THRESH_TRUNC => los valores por encima del umbral se binarizan
        con el valor_por_encima, los valores por debajo no
        - cv2.THRESH_TOZERO => los valores por debajo del
        umbral se binarizan a 0, los valores por encima no
        - cv2.THRESH_TOZERO_INV => los valores por encima
        del umbral se binarizan a 0, los valores por debajo no

     Devuelve la imagen binarizada img_binarizada

     **El valor devuelto umbral, nos indica el umbral,
    como en este caso lo ponemos nosotros manualmente, es irrelevante, por lo que no lo devolvemos**
"""
    umbral, img_binarizada = cv2.threshold(frame, umbral, valor_por_encima, modo)
    return img_binarizada

def binarizar_umbral_adaptativo(frame, valor_por_encima, metodo, modo, tam_vecindario, constante):
    """
    Llamamos umbral adaptativo cuando este cambia para pequeñas zonas de la imagen.
    Se calcula este umbral en funcion de los pixeles que rodean a un pixel (vecindario).
    Mejora respecto del umbral fijo ya que no siempre tenemos que tener la misma luminosidad
    en toda una imagen, de hecho es que una imagen tenga la misma luminosidad es un entorno ideal
    y que nunca o casi nunca se puede obtener.

    Parametros:

    - frame: Imagen de origen
    - valor_por_encima: Valor asignado a los pixeles por encima del umbral
    - metodo: metodo para calcular el umbral, hay dos tipos:
        - cv2.ADAPTIVE_THRESH_MEAN_C:  Permite binarizar la imagen adaptando el valor umbral
        a cada distinta zona de la imagen.
        El umbral lo calcula segun la media de los vecinos del pixel

        - cv2.ADAPTIVE_THRESH_GAUSSIAN_C: Permite binarizar la imagen adaptando el valor umbral
        a cada distinta zona de la imagen.
        El umbral lo calcula segun la formula de la ventana gaussiana +
        para el vecindario del pixel

    - modo: modo de binarizar la imagen, debe de ser cv2.THRESH_BINARY o cv2.THRESH_BINARY_INV.
    - tam_vecindario_ tamaño del vecindario respecto
    del que se va a calcular el umbral, valor entero positivo.
    - constante: constante para calcular la media o media ponderada.
        Valor entero, normalmente positivo,
        aunque tambien puede ser 0 o negativo.

    Devuelve la imagen binarizada img_binarizada
    """
    img_binarizada = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
    return img_binarizada

def calcular_luminosidad(frame):
    """
    Calcula la luminosidad de un frame
    Los pesos de cada color son en funcion de su luminosidad, ya que
    rojo verde y azul puros de RGB no tienen la misma luminosidad.

    Peso del rojo: 0.299
    Peso del verde: 0.587
    Peso del azul: 0.114

    Lo que hacemos es separar los canales RGB de la imagen,
    calcular la media de cada color del 0 al 255, y sumar esas medias
    por sus correspondientes pesos. Vease que los pesos suman 1, por tanto
    el valor mínimo que puede devolver esta funcion es 0 y el máximo es 255.

    Devuelve un valor entre 0 y 255.
    """
    b, g, r = cv2.split(frame)
    b_avg = np.average(b)
    g_avg = np.average(g)
    r_avg = np.average(r)

    luminosidad = r_avg*0.299 + g_avg*0.587 + b_avg*0.114
    return luminosidad


def calcular_ancho_linea(img_bin, max_line_width, min_line_width,
                         img_height, img_width, real_width, height, crop):
    """
    Calcula el ancho de la linea en cualquier parte de la imágen, resolviendo la
    distorsión por perspectiva.
    Parámetros:
    - img_bin: imagen binarizada
    - max_line_width: ancho máximo de la linea medido en la imagen real (entero positivo)
    - min_line_width: ancho mínimo de la linea medido en la imagen real (entero positivo)
    - img_height: altura de la imagen (entero positivo)
    - img_width: anchura de la imagen (entero positivo)
    - real_width: ancho real de la linea, en cm, metros, unidades ... (float positivo)
    - height: altura de la imagen donde mediremos el ancho (de 1 a img_height)
    - crop: fraccion del ancho de la imagen que se recorta para obtener el ancho de la linea
    """

    import numpy as np

    reduccion_px = max_line_width - min_line_width
    reduccion_fila = float(reduccion_px) / float(img_height)
    anchura_calculada = max_line_width - (height * reduccion_fila)


    anchura_medida = 0
    array = np.array(img_bin[abs(height - img_height)])
    #Información de la parte central de la imagen
    array = array[int(img_width/crop):int(3*(img_width/crop))]
    anchura_medida = sum(array == 255)

    return anchura_calculada, anchura_medida

def obtener_contornos(frame, umbral_bajo, umbral_alto):
    """
    Calcula los contornos de los elementos de la imagen
    Parámetros:
    - frame: imagen de origen
    - umbral_bajo: primer umbral para realizar la histéresis
    - umbral_alto: segundo umbral para realizar la histéresis
    """
    contornos = cv2.Canny(frame, umbral_bajo, umbral_alto)

    for i in range(len(contornos)):
        for j in range(len(contornos[0])):
            if contornos.item(i, j) is 255:
                for k in range(-2, 2):
                    if j-k > 0 and j-k < len(contornos[0]) and j+k < len(contornos[0]) and k is not 0:
                        contornos.itemset((i, j+k), 0)

    return contornos



def deteccion_lineas_hough(frame):
    """
    *Experimental*
    https://docs.opencv.org/3.4.0/d9/db0/tutorial_hough_lines.html
    Detecta lineas en una imagen binarizada y las dibuja sobre la imagen
    Es conveniente que la imagen no solo sea binaria sino que sea un
    "mapa" de bordes de la imagen original. Aplicar algun tipo de fitlrado de
    deteccion de bordes.
    devuelve la imagen con las lineas
    Parámetros:
    - frame: imagen de origen
    """

    retorno = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    linesP = cv2.HoughLinesP(frame, cv2.HOUGH_PROBABILISTIC,
                             np.pi/180, 90, minLineLength=5, maxLineGap=5)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(retorno, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

    return retorno

def obtener_unico_borde(frame, modo):
    """
    Permite obtener el borde derecho o izquierdo de la linea
    Parámetros:
    - frame: imagen binarizada y pasada por un filtro de detección de bordes
    - modo: 0 de izquierda a derecha, 1 de derecha a izquierda
    """

    img_aux = np.zeros((len(frame), len(frame[0])), dtype=np.uint8)

    for i in range(len(frame)):
        aux = True
        if modo is 0:
            for j in range(0, len(frame[0])):
                if frame[i][j] != 0 and aux:
                    img_aux[i][j] = 255
                    aux = False

        if modo is 1:
            for j in range(len(frame[0])-1, -1, -1):
                if frame[i][j] != 0 and aux:
                    img_aux[i][j] = 255
                    aux = False

    return img_aux

def obtener_polinomio(frame):
    """
        *Experimental*
        Recibe una imagen binaria donde los valores
        que no son cero, representan una linea, y
        mediante ajuste de polinomio intenta obtener
        el polinomio asociado a la curva.

        Devuelve la imagen con el polinomio dibujado
    """
    datax = []
    datay = []
    ret = frame
    for i in range(len(frame)):
        aux = True
        for j in range(0, len(frame[0])):
            if frame[i][j] != 0 and aux:
                datay.append(i)
                datax.append(j)
                aux = False

    z = np.polyfit(datax, datay, 5)
    f = np.poly1d(z)
    t = np.arange(min(datax), max(datax), 1)
    for i in range(1, len(t)):
        cv2.line(ret, (int(f(t[i-1])), t[i-1]),
                 (int(f(t[i])), t[i]), (0, 0, 255), 3)

    return ret

def obtener_trayectoria(frame):
    """
    Obtiene la trayectoria calculada a partir de los dos bordes de la línea.
    Parámetros:
    - frame: imagen binarizada donde solo esten los dos bordes de la linea.
        Usar funcion obtener contornos.

    Devuelve la imagen con la trayectoria pintada
    """

    img_aux = np.zeros((len(frame), len(frame[0])), dtype=np.uint8)

    for i in range(len(frame)):
        aux = True
        bordes = 0
        borde_1 = 0
        borde_2 = 0
        for j in range(0, len(frame[0])):
            if frame[i][j] != 0 and aux:
                if bordes is 0:
                    borde_1 = j
                if bordes is 1:
                    borde_2 = j
                    img_aux[i][borde_1+((borde_2-borde_1)/2)] = 255
                    aux = False
                bordes += 1

    return img_aux

def pintar_lineas(frame, lineas, color):
    """
    Pinta lineas en la imagen de origen
    - frame: imagen donde queremos pintar las lineas
    - lineas: imagen binaria donde los pixeles que
            no son 0 se interpretan como linea.
    - color: color en el que se va a pintar la linea
            en BGR (b,g,r)

    Devuelve la imagen con las lineas pintadas
    """
    for i in range(len(frame)):
        for j in range(len(frame[0])):
            if lineas.item(i, j) is not 0:
                for i in range(i-1, i+1):
                    if j-1 > -1 and j+1 < len(frame[0]):
                        frame.itemset((i, j, 0), color[0])
                        frame.itemset((i, j, 1), color[1])
                        frame.itemset((i, j, 2), color[2])

    return frame
    