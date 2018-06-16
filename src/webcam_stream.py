# coding=utf-8
# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import time
import urllib
import cv2
import numpy as np

class webcam_stream(object):
    """
    Clase que permite obtener imagenes desde un servidor de video en Lan.
    El constructor recibe la url del servidor de imagenes.
    En este proyecto se ha usado como servidor la aplicación androids
    IPWebcam.
    """
    def __init__(self, url):
        self.url = url

    def get_frame(self, modo):
        """
        Permite obtener un frame, una 'foto'. Para ello primero llena
        el buffer con 10 imagenes, y devuelve la última.
        Parametros:
        - modo: >0 si queremos la imagen en color RGB,
        0 en blanco y negro, <0 para obtener la imagen en canales alfa.
        """
        frames = []
        for i in range(0, 10):

            # Uso urllib para abrir la url
            imgUrl = urllib.urlopen(self.url)

            # con numpy recogo el video como array de enteros de 8 bits (256 rangos de color en rgb)
            imgArray = np.array(bytearray(imgUrl.read()), dtype=np.uint8)

            # decodificamos la imagen segun el modo requerido
            img = cv2.imdecode(imgArray, modo)

            frames.append(img)

        return frames[9]


    def get_video_stream(self, modo):
        """
        Permite obtener un frame, una 'foto'. En este caso lo debemos de usar
        dentro de un bucle, lo que hará que el buffer se llene y podamos obtener
        imagenes de forma continua.
        Parametros:
        - modo: >0 si queremos la imagen en color RGB,
        0 en blanco y negro, <0 para obtener la imagen en canales alfa.
        """

        #inicio contador de tiempo para ver fps
        t = time.time()

        # Uso urllib para abrir la url
        imgUrl = urllib.urlopen(self.url)

        # con numpy recogo el video como array de enteros de 8 bits (256 rangos de color en rgb)
        imgArray = np.array(bytearray(imgUrl.read()), dtype=np.uint8)

        # decodificamos la imagen segun el modo requerido
        img = cv2.imdecode(imgArray, modo)

        #calculo los fps
        elapsed = time.time() - t
        #Elapsed a veces es 0, si eso pasa uso 0.02 (lo suficiente para obtener 50fps)
        # para no alterar demasiado la medición, ya que nuestro objetivo son 50 fps.
        if elapsed != 0:
            f = 1/elapsed
        else:
            f = 1/0.02
        return img, f
