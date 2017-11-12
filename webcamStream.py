# coding=utf-8
# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib
import cv2
import numpy as np
import time

class webcamStream:

    def __init__(self, url):
        self.url = url
    
    """
    modo es un número entero tal que:
     si modo > 0, nos devuelve la imagen de 3 canales de color.
     si modo = 0, nos devuelve la imagen en escala de grises.
     si modo < 0, nos devuelve la imagen con canal alfa.
    """
    def getVideoStream(self, modo):    
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
        print(str(1/elapsed) + " fps")

        return img

            


