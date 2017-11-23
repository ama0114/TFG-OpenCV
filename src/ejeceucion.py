# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox

def main():
    stream = webcam_stream('http://192.168.1.11:8080/shot.jpg')
    fpsStats = []
    img = stream.get_frame(1)
    print("Luminosidad " + str(toolbox.calcular_luminosidad(img)))
    while True:
        #0 - B/N, 1 - Color RGB
        vid, fps = stream.get_video_stream(0)

        #Añado los fps a una lista para despues mostrar estadisticas
        fpsStats.append(fps)

        #Binarizo la imagen 
        #Uso cv2.THRESH_BINARY_INV ya que necesito que la linea sea blanca y el resto negro
        #img_binarizada = toolbox.binarizar_umbral_fijo(vid, 147, 255, cv2.THRESH_BINARY_INV)
        umbral, img_binarizada = toolbox.binarizar_otsu(vid,255)
        #Muestro la imagen
        cv2.imshow('Binarizada', img_binarizada)
        cv2.imshow('Original', vid)

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Minimos fps: " + str(min(fpsStats)))
            print("Maximos fps: " + str(max(fpsStats)))
            print("Media fps: " + str(np.average(fpsStats)))
            break

if  __name__ =='__main__':
    main()