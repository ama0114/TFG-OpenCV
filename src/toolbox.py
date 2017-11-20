# coding=utf-8
import cv2
import numpy as np

def binarizar_otsu(frame, valor_por_encima):
    """
    Funcion que permite binarizar una imagen, 
    calculando el umbral de binarizacion segun el algoritmo de Otsu.
    parametros:
    - frame: imagen a binarizar
    - valor_por_encima: valor asignados a los pixeles por encima del umbral

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

    