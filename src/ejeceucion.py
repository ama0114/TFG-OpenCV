# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox

coef = 0
stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')

def main():
    umbral = 0
    fpsStats = []
    img = stream.get_frame(1)
    print("Luminosidad " + str(toolbox.calcular_luminosidad(img)))
    raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
    coef = calcular_coef_angulo()
    print("El coeficiente calculado es: " + str(coef))
    raw_input("Retira la plantilla, pulsa intro para continuar")
    while True:
        #0 - B/N, 1 - Color RGB
        vid, fps = stream.get_video_stream(0)

        #Añado los fps a una lista para despues mostrar estadisticas
        fpsStats.append(fps)

        #Binarizo la imagen 
        #Uso cv2.THRESH_BINARY_INV ya que necesito que la linea sea blanca y el resto negro
        #img_binarizada = toolbox.binarizar_umbral_fijo(vid, 147, 255, cv2.THRESH_BINARY_INV)
        umbral, img_binarizada = toolbox.binarizar_otsu(vid,255,cv2.THRESH_BINARY_INV)
        #img_binarizada = toolbox.binarizar_umbral_adaptativo(vid, 255, 
        #cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 20, 7)
        img_correjida = toolbox.correjir_distorsion_perspectiva(img_binarizada, 105)
        
        #Muestro la imagen
        cv2.imshow('Binarizada', img_binarizada)
        cv2.imshow('Original', vid)
        cv2.imshow('Correjida',img_correjida)
        

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Minimos fps: " + str(min(fpsStats)))
            print("Maximos fps: " + str(max(fpsStats)))
            print("Media fps: " + str(np.average(fpsStats)))

            ''' anchura_calculada, anchura_medida = toolbox.calcular_ancho_linea(img_binarizada, 
            56, 13, 144, 176, 1.6, 130, 4)
            print("Anchura calculada " + str(anchura_calculada))
            print("Anchura medida " + str(anchura_medida))
            print("Porcentraje error " + str(abs(100-(anchura_medida/anchura_calculada*100))) + "%") '''

            if umbral > 0:
                print("El umbral calculado mediante el algoritmo de otsu es: " + str(umbral))
            break

def calcular_coef_angulo():
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
            break
    return c


if  __name__ =='__main__':
    main()