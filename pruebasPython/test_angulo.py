# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox

def main():
    stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')
    
    while True:
        #0 - B/N, 1 - Color RGB
        vid, fps = stream.get_video_stream(0)

        #Binarizo
        umbral, img_binarizada = toolbox.binarizar_otsu(vid,255,cv2.THRESH_BINARY_INV)

        #Calculo angulo
        c = toolbox.calcular_angulo_coef(img_binarizada)

        #Muestro la imagen
        cv2.imshow('Original', img_binarizada)

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print(c)
            break

if  __name__ =='__main__':
    main()