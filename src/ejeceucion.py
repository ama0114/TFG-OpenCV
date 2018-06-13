# coding=utf-8
from webcam_stream import webcam_stream
from binarizar_hsv import binarizar_hsv
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox
import math
from direccion import direccion
from perspectiva import perspectiva
import os

""" def main():
    dir = direccion(0.02,len(stream.get_frame(1)[0]))
    im_spc1, im_spc2, im_spc3, im_spc4, fig = crear_marco_comparacion(stream.get_frame(1))
    salir = [False]
    umbral = 0
    fpsStats = []
    img = stream.get_frame(1)
    print("Luminosidad " + str(toolbox.calcular_luminosidad(img)))
    raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
    persp.calcular_coef_angulo(stream)
    print("El coeficiente calculado es: " + str(persp.coef_correcion))
    raw_input("Retira la plantilla, pulsa intro para continuar")
    #menu(stream, persp)
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

        
        
        #lineas = toolbox.deteccion_lineas_hough(bordes)

        #borde_izq = toolbox.obtener_unico_borde(bordes,0)
        #borde_der =  toolbox.obtener_unico_borde(bordes,1)

        bordes = toolbox.obtener_contornos(img_correjida, 50, 200)
        tray = toolbox.obtener_trayectoria(bordes)
        bordes_tray = bordes + tray
        texto, angulo = dir.obtener_direccion(tray)
        #pol = toolbox.obtener_polinomio(borde_izq)
        
        #Muestro la imagen
        #cv2.imshow('Binarizada', img_binarizada)
        #cv2.putText(bordes_tray, texto + "              " + str(round(angulo,2)), 
        #(10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        #cv2.putText(vid, texto + "              " + str(round(angulo,2)), 
        #(10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)
        
        #cv2.imshow('Original', vid)
        #cv2.imshow('Trayectoria', bordes_tray)
        
        mostrar_comparacion_imagenes(im_spc1, im_spc2, im_spc3, im_spc4, 
                        img_binarizada, vid, img_correjida, bordes_tray)

        #Funcion auxiliar para capturar el evento de cierre de la figura
        def handle_close(evt):
            del salir[:]
            salir.append(True)
        
        fig.canvas.mpl_connect('close_event', handle_close)
        if salir[0] is True:
            break
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
            break """

def main():

    stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')
    persp = perspectiva(stream.get_frame(1))
    bin_hsv = binarizar_hsv()

    menu(stream, persp, bin_hsv)


def crear_marco_comparacion(img):

    fig, ax = plt.subplots(nrows=2, ncols=2)
    image_spaces = []
    for row in ax:
        for col in row:
            image_spaces.append(col.imshow(img, cmap='gray'))

    """ #Creo subplots
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,2,3)
    ax4 = plt.subplot(2,2,4)

    #Creo espacios para mostrar imagenes
    im_spc1 = ax1.imshow(img, cmap='gray')
    im_spc2 = ax2.imshow(img, cmap='gray')
    im_spc3 = ax3.imshow(img, cmap='gray')
    im_spc4 = ax4.imshow(img, cmap='gray') """

    #Hago el plot dinamico
    plt.ion()

    #return im_spc1, im_spc2, im_spc3, im_spc4
    return image_spaces[0], image_spaces[1], image_spaces[2], image_spaces[3], fig

def mostrar_comparacion_imagenes(im_spc1, im_spc2, im_spc3, im_spc4, im1, im2, im3, im4):

    #Asigno las imagenes
    im_spc1.set_data(im1)
    im_spc2.set_data(im2)
    im_spc3.set_data(im3)
    im_spc4.set_data(im4)

    #Tiempo de pausa, lo menor posible para que el video se muestre fluido
    plt.pause(0.001)

def menu(stream, persp, binarizar_hsv):
    opcion = 0
    while(opcion is not 5):
        opcion = input("1-Binarizar luminosidad \n 2-Binarizar color \n 3-Muestra proceso \n 4-Ejecucion normal \n 5-Salir \n")
        if opcion is 1:
            binarizar_luminosidad(stream)
            opcion = 0
        elif opcion is 2:
            binarizar_color(binarizar_hsv)
            opcion = 0
        elif opcion is 3:
            muestra_proceso(stream, persp, binarizar_hsv) 
            opcion = 0
        elif opcion is 4:
            pass
            opcion = 0
        elif opcion is 5:
            quit()
        else:
            print("Error, intentalo de nuevo\n")


def binarizar_luminosidad(stream):
    fps_stats = []
    while True:
        vid, fps = stream.get_video_stream(0)
        umbral, img_binarizada = toolbox.binarizar_otsu(vid,255,cv2.THRESH_BINARY_INV)
        cv2.imshow('Bin_Lum', img_binarizada)
        fps_stats.append(fps)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            imprimir_fps_stats(fps_stats)
            print("Umbral de binarizacion" + str(umbral))
            cv2.destroyAllWindows()
            break

def binarizar_color(binarizar_hsv):
    binarizar_hsv.calibrar_color()

def muestra_proceso(stream, persp, binarizar_hsv):

    opcion = 0
    while opcion is not 3:
        opcion = input("1-Binarizar Color\n 2-Binarizar Luminosidad\n 3-Salir\n")
        if opcion is 1:
            binarizar_color(binarizar_hsv)

            raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
            persp.calcular_coef_angulo(stream, 1, binarizar_hsv.binarizar_frame)
            print("El coeficiente calculado es: " + str(persp.coef_correcion))
            raw_input("Retira la plantilla, pulsa intro para continuar")
            
            muestra_proceso_aux(1, binarizar_hsv.binarizar_frame, stream, persp)

        elif opcion is 2:
            
            def funcion_adaptador(frame):
                umbral, frame = toolbox.binarizar_otsu(frame,255,cv2.THRESH_BINARY_INV)

                return frame

            raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
            persp.calcular_coef_angulo(stream, 0, funcion_adaptador)
            print("El coeficiente calculado es: " + str(persp.coef_correcion))
            raw_input("Retira la plantilla, pulsa intro para continuar")
            
            muestra_proceso_aux(0, funcion_adaptador, stream, persp)

        elif opcion is 3:
            break
        else:
            print("Error, introduce una opción correcta\n")
    
def ejecucion_normal():
    pass

def imprimir_fps_stats(fps_stats):
    print("Minimos fps: " + str(min(fps_stats)))
    print("Maximos fps: " + str(max(fps_stats)))
    print("Media fps: " + str(np.average(fps_stats)))

def muestra_proceso_aux(color_stream, funcion_binarizado, stream, persp):

    salir_evt = [False]
    fps_stats = []
    im_spc1, im_spc2, im_spc3, im_spc4, fig = crear_marco_comparacion(stream.get_frame(1))

    def handle_close(evt):
        del salir_evt[:]
        salir_evt.append(True)

    salir = False
    while not salir:
        #0 - B/N, 1 - Color RGB
        vid, fps = stream.get_video_stream(color_stream)

        #Añado los fps a una lista para despues mostrar estadisticas
        fps_stats.append(fps)

        img_correjida = persp.correjir_distorsion_perspectiva(vid)

        img_binarizada = funcion_binarizado(img_correjida)

        bordes = toolbox.obtener_contornos(img_binarizada, 50, 200)
        tray = toolbox.obtener_trayectoria(bordes)
        bordes_tray = bordes + tray

        fig.canvas.mpl_connect('close_event', handle_close)

        if color_stream is 1:
            vid = cv2.cvtColor(vid, cv2.COLOR_RGB2BGR)
            img_correjida = cv2.cvtColor(img_correjida, cv2.COLOR_RGB2BGR)

        mostrar_comparacion_imagenes(im_spc1, im_spc2, im_spc3, im_spc4, vid, img_correjida, img_binarizada, bordes_tray)

        if salir_evt[0] is True:
            imprimir_fps_stats(fps_stats)
            cv2.destroyAllWindows()
            salir = True
            opcion = 0
            salir_evt[0] = False

if  __name__ =='__main__':
    main()