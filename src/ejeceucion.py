# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox
import math
from direccion import direccion
from perspectiva import perspectiva

coef = 0
stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')



def main():
    dir = direccion(0.02,len(stream.get_frame(1)[0]))
    

    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,2,3)
    ax4 = plt.subplot(2,2,4)
    im1 = ax1.imshow(stream.get_frame(1), cmap='gray')
    im2 = ax2.imshow(stream.get_frame(1), cmap='gray')
    im3 = ax3.imshow(stream.get_frame(1), cmap='gray')
    im4 = ax4.imshow(stream.get_frame(1), cmap='gray')
    plt.ion()

    umbral = 0
    fpsStats = []
    img = stream.get_frame(1)
    print("Luminosidad " + str(toolbox.calcular_luminosidad(img)))
    raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
    coef = calcular_coef_angulo()
    print("El coeficiente calculado es: " + str(coef))
    raw_input("Retira la plantilla, pulsa intro para continuar")
    persp = perspectiva(stream.get_frame(1),coef)
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
        img_correjida = persp.correjir_distorsion_perspectiva(img_binarizada)

        bordes = toolbox.obtener_contornos(img_correjida, 50, 200)
        
        #lineas = toolbox.deteccion_lineas_hough(bordes)

        #borde_izq = toolbox.obtener_unico_borde(bordes,0)
        #borde_der =  toolbox.obtener_unico_borde(bordes,1)

        tray = toolbox.obtener_trayectoria(bordes)
        bordes_tray = bordes + tray
        texto, angulo = dir.obtener_direccion(tray)
        #pol = toolbox.obtener_polinomio(borde_izq)
        
        #Muestro la imagen
        #cv2.imshow('Binarizada', img_binarizada)
        """ cv2.putText(bordes_tray, texto + "              " + str(round(angulo,2)), 
        (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        cv2.putText(vid, texto + "              " + str(round(angulo,2)), 
        (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)
        
        cv2.imshow('Original', vid)
        cv2.imshow('Trayectoria', bordes_tray) """
        
        im1.set_data(img_binarizada)
        im2.set_data(vid)
        im3.set_data(img_correjida)
        im4.set_data(bordes_tray)
        plt.pause(0.001)

        #cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", lineas)
        #cv2.imshow("Borde izquierdo", borde_izq)
        #cv2.imshow("Borde derecho", borde_der)
        #cv2.imshow("Tray", tray)
        #cv2.imshow("Polinomio", pol)
        

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
            cv2.destroyAllWindows()
            break
    return c


if  __name__ =='__main__':
    main()