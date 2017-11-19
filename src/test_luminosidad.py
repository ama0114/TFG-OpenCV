# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox

def main():
    stream = webcam_stream('http://192.168.1.11:8080/shot.jpg')
    
    while True:
        #0 - B/N, 1 - Color RGB
        vid, fps = stream.get_video_stream(1)

        #Muestro la luminosidad
        print("Luminosidad " + str(toolbox.calcular_luminosidad(vid)))

        #Muestro la imagen
        cv2.imshow('Original', vid)

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

if  __name__ =='__main__':
    main()