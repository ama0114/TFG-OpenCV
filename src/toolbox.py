# coding=utf-8
import cv2
import numpy as np

def binarizar_otsu(frame):
    pass


def binarizar_umbral_fijo(frame, umbral, valor_por_encima, modo):
    """Funcion para binarizar una imagen
    vid es la imagen a binarizar, umbral el valor umbral, valor_por_encima 
    es el valor que se les dará a los pixels por encima del umbral
    el modo puede ser:
    
    - cv2.THRESH_BINARY  => binarizacion normal

    - cv2.THRESH_BINARY_INV => binarizacion inversa

    - cv2.THRESH_TRUNC => los valores por encima del umbral se binarizan 
    con el valor_por_encima, los valores por debajo no

    - cv2.THRESH_TOZERO => los valores por debajo del 
    umbral se binarizan a 0, los valores por encima no

    - cv2.THRESH_TOZERO_INV => los valores por encima 
    del umbral se binarizan a 0, los valores por debajo no

    El valor devuelto umbral, nos indica el umbral, 
    como en este caso lo ponemos nosotros manualmente, es irrelevante

    img_binarizada es la imagen binarizada
"""
    umbral, img_binarizada = cv2.threshold(frame, umbral, valor_por_encima, modo)
    return img_binarizada

def binarizar_umbral_media(frame):
    pass

def binarizar_umbral_gaussiano(frame):
    pass



def calcular_luminosidad(frame):
    """
    Calcula la luminosidad de un frame
    Los pesos de cada color son en funcion de su luminosidad, ya que
    rojo verde y azul puros de RGB no tienen la misma luminosidad.

    Lo que hacemos es separar los canales RGB de la imagen, 
    calcular la media de cada color, y sumar esas medias
    por sus correspondientes pesos.
    """
    b,g,r = cv2.split(frame)
    b_avg = np.average(b)
    g_avg = np.average(g)
    r_avg = np.average(r)

    luminosidad = r_avg*0.299 + g_avg*0.587 + b_avg*0.114
    return luminosidad

    