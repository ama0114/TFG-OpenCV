# coding=utf-8
# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib
import cv2
import numpy as np
import time

class webcam_stream:

    def __init__(self, url):
        self.url = url
    
    """
    modo es un número entero tal que:
     si modo > 0, nos devuelve la imagen de 3 canales de color.
     si modo = 0, nos devuelve la imagen en escala de grises.
     si modo < 0, nos devuelve la imagen con canal alfa.
    """
    def get_video_stream(self, modo):
        
        #inicio contador de tiempo para ver fps
        t = time.time()

        # Uso urllib para abrir la url
        imgUrl = urllib.urlopen(self.url)
        
        # con numpy recogo el video como array de enteros de 8 bits (256 rangos de color en rgb)
        imgArray = np.array(bytearray(imgUrl.read()),dtype=np.uint8)
        
        # decodificamos la imagen segun el modo requerido
        img = cv2.imdecode(imgArray, modo)
        
        #calculo los fps
        elapsed = time.time() - t
        #Elapsed a veces es 0, si eso pasa uso 0.02 (lo suficiente para obtener 50fps) 
        # para no alterar demasiado la medición, ya que nuestro objetivo son 50 fps.
        if(elapsed != 0):
            f = 1/elapsed
        else:
            f = 1/0.02
        return img, f
        
            


