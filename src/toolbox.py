# coding=utf-8
import cv2
import numpy as np

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
    umbral, img_binarizada = cv2.threshold(frame,0,valor_por_encima,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
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
        - cv2.ADAPTIVE_THRESH_MEAN_C:  Permite binarizar la imagen adaptando el valor umbral a cada
        distinta zona de la imagen.
        El umbral lo calcula segun la media de los vecinos del pixel

        - cv2.ADAPTIVE_THRESH_GAUSSIAN_C: Permite binarizar la imagen adaptando el valor umbral a cada
        distinta zona de la imagen.
        El umbral lo calcula segun la formula de la ventana gaussiana 
        para el vecindario del pixel

    - modo: modo de binarizar la imagen, debe de ser cv2.THRESH_BINARY o cv2.THRESH_BINARY_INV .
    - tam_vecindario_ tamaño del vecindario respecto del que se va a calcular el umbral, valor entero positivo.
    - constante: constante para calcular la media o media ponderada. valor entero, normalmente positivo, 
    aunque tambien puede ser 0 o negativo.

    Devuelve la imagen binarizada img_binarizada
    """
    img_binarizada = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
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
    b,g,r = cv2.split(frame)
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

def calcular_angulo_coef(frame):
    """
    Calcula el coeficiente de reduccion en pixeles de la imagen
    en funcion del angulo que tiene la camara sobre el suelo.
    Se usará una plantilla con un cuadrado de proporciones conocidas.
    La funcion devuelve el coeficiente de reduccion.
    
    Parámetros: 
    - frame: imagen binarizada.
    """
    coef = 0
    bottom_square = 0
    top_square = 0
    min_width = 0
    max_width = 0
    b = True
    t = True

    for i in range(len(frame)-2,-1,-1):
        if(frame[i][len(frame[0])/2] == 255 and b):
            #Dejamos 2 pixeles de margen
            bottom_square = i-2
            b = False
        
        if(bottom_square != 0 and frame[i][len(frame[0])/2] == 0 and t):
            #Dejamos 2 pixeles de margen
            top_square = i+2
            t = False

    min_width = sum(frame[top_square] > 0)
    max_width = sum(frame[bottom_square] > 0)
    if(float(bottom_square - top_square) > 0):
        coef = abs(float (min_width - max_width) / float(bottom_square - top_square))

    return coef


def correjir_distorsion_perspectiva(frame, coef):
    """
    Permite obtener una vista de pajaro de la imagen de origen.
    Parámetros:
    - frame: imagen de origen
    - coef: coeficiente de correcion para la distorsion por perspectiva
    """
    g = lambda x: 140.3462 + (101.7432 - 140.3462)/(1 + (x/0.5605076)**64.36072)
    tam_reducido = g(coef)
    

    src = np.float32([[0, len(frame)-1], [len(frame[0])-1, len(frame)-1], 
                        [0, 0], [len(frame[0])-1, 0]])
    dst = np.float32([[tam_reducido/2, len(frame)-1], 
                        [len(frame[0])-tam_reducido/2, len(frame)-1], 
                        [0, 0], [len(frame[0])-1, 0]])

    M = cv2.getPerspectiveTransform(src, dst) 

    warped_img = cv2.warpPerspective(frame, M, (len(frame[0]), len(frame))) 

    return warped_img

def obtener_contornos(frame, umbral_bajo, umbral_alto):
    """
    Calcula los contornos de los elementos de la imagen
    Parámetros:
    - frame: imagen de origen
    - umbral_bajo: primer umbral para realizar la histéresis
    - umbral_alto: segundo umbral para realizar la histéresis
    """
    return cv2.Canny(frame, umbral_bajo, umbral_alto)


def deteccion_lineas_hough(frame):
    """
    https://docs.opencv.org/3.4.0/d9/db0/tutorial_hough_lines.html
    Detecta lineas en una imagen binarizada y las dibuja sobre la imagen
    Es conveniente que la imagen no solo sea binaria sino que sea un 
    "mapa" de bordes de la imagen original. Aplicar algun tipo de fitlrado de
    deteccion de bordes.
    devuelve la imagen
    Parámetros: 
    - frame: imagen de origen
    
    """

    cdst = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    
    lines = cv2.HoughLines(frame, 1, np.pi / 180, 150, 10, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    
    
    linesP = cv2.HoughLinesP(frame, 1, np.pi / 180, 50, None, 50, 10)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    
    return cdstP

        


        