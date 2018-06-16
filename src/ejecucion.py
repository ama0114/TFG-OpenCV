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
    opcion = -1
    while(opcion is not 0):
        print("******* Menu ***********")
        
        opcion = input(" 1-Prueba binarizar luminosidad \n 2-Prueba binarizar color \n 3-Muestra proceso \n 4-Ejecucion normal \n 0-Salir \n")
        print("************************")
        if opcion is 1:
            print("************************")
            print("Prueba binarizar por luminosidad, pulsa 's' para salir.")
            print("************************")
            binarizar_luminosidad(stream)
            opcion = -1
        elif opcion is 2:
            print("************************")
            print("Prueba binarizar por color, pulsa 's' para salir.")
            print("************************")
            binarizar_color(binarizar_hsv)
            opcion = -1
        elif opcion is 3:
            menu_aux(stream, persp, binarizar_hsv, muestra_proceso) 
            opcion = -1
        elif opcion is 4:
            menu_aux(stream, persp, binarizar_hsv, ejecucion_normal)
            opcion = -1
        elif opcion is 0:
            quit()
        else:
            print("Error, intentalo de nuevo\n")


def binarizar_luminosidad(stream):
    fps_stats = []
    salir = False
    while not salir:
        vid, fps = stream.get_video_stream(0)
        umbral, img_binarizada = toolbox.binarizar_otsu(vid,255,cv2.THRESH_BINARY_INV)
        cv2.imshow('Original', vid)
        cv2.imshow('Bin_Lum', img_binarizada)
        fps_stats.append(fps)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            imprimir_fps_stats(fps_stats)
            print("Umbral de binarizacion: " + str(umbral))
            cv2.destroyAllWindows()
            salir = True

def binarizar_color(binarizar_hsv):
    binarizar_hsv.calibrar_color()

def menu_aux(stream, persp, binarizar_hsv, ejecucion):

    opcion = -1
    while opcion is not 0:
        print("************************")
        opcion = input("1-Binarizar Color\n 2-Binarizar Luminosidad\n 0-Salir\n")
        print("************************")
        if opcion is 1:
            binarizar_color(binarizar_hsv)

            calcular_coef_angulo_interaccion(persp, stream, binarizar_hsv.binarizar_frame, 1)
            
            ejecucion(1, binarizar_hsv.binarizar_frame, stream, persp)

        elif opcion is 2:
            
            def funcion_adaptador(frame):
                umbral, frame = toolbox.binarizar_otsu(frame,255,cv2.THRESH_BINARY_INV)

                return umbral, frame

            calcular_coef_angulo_interaccion(persp, stream, funcion_adaptador, 0)
            
            ejecucion(0, funcion_adaptador, stream, persp)

        elif opcion is 0:
            opcion = -1
            break
        else:
            print("************************")
            print("Error, introduce una opcion correcta\n")
            print("************************")

def pinta_indicadores(frame, dir):
    centro = [len(frame[0])/2,(len(frame[0])/2)-1]
    rango = [int(dir.rango_seguro_min),int(dir.rango_seguro_max)]
    for i in range(len(frame)-1, len(frame)-10, -1):
        for j in centro:
            frame.itemset((i, j, 0),0)
            frame.itemset((i, j, 1),255)
            frame.itemset((i, j, 2),0)
        for j in rango:
            frame.itemset((i, j, 0),0)
            frame.itemset((i, j, 1),0)
            frame.itemset((i, j, 2),255)
    return frame
    
def ejecucion_normal(color_stream, funcion_binarizado, stream, persp):
    fps_stats = []
    rango_seguro = -1
    while rango_seguro > 0.3 or rango_seguro < 0:
        rango_seguro = input("Dime el rango seguro para la direccion\n min=0, max=0.3\n")

    dir = direccion(rango_seguro, len(stream.get_frame(1)[0]))
    while True:
        vid, fps = stream.get_video_stream(1)
        
        umbral = 0

        if color_stream is 0:
            vid_bn = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
            umbral, img_binarizada = funcion_binarizado(vid_bn)
        else:
            img_binarizada = funcion_binarizado(vid)

        #Perspectiva
        img_bin_persp = persp.correjir_distorsion_perspectiva(img_binarizada)
        vid_persp = persp.correjir_distorsion_perspectiva(vid)
        bordes_persp = toolbox.obtener_contornos(img_bin_persp, 50, 200)
        tray_persp = toolbox.obtener_trayectoria(bordes_persp)

        #Normal
        bordes_normal = toolbox.obtener_contornos(img_binarizada, 50, 200)
        tray_normal = toolbox.obtener_trayectoria(bordes_normal)
        texto, angulo = dir.obtener_direccion(tray_normal)

        vid = toolbox.pintar_lineas(vid, tray_normal, [255,0,0])
        vid = pinta_indicadores(vid, dir)

        vid_persp = toolbox.pintar_lineas(vid_persp, bordes_persp, [0,255,0])
        vid_persp = toolbox.pintar_lineas(vid_persp, tray_persp, [255,0,0])

        cv2.putText(vid, texto + "              " + str(round(angulo,2)), 
        (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,255), 1)

        cv2.putText(vid_persp, 
        "Lum:              " + str(round(toolbox.calcular_luminosidad(vid),2)), 
        (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,255), 1)

        cv2.putText(vid_persp, 
        "Fps:              " + str(round(fps,2)), 
        (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,255), 1)

        if color_stream is 0:
            cv2.putText(vid_persp, 
            "Umb:              " + str(round(umbral,2)), 
            (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,255), 1)

        cv2.imshow('Guia', vid)
        cv2.imshow('Tray', vid_persp)

        fps_stats.append(fps)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            imprimir_fps_stats(fps_stats)
            cv2.destroyAllWindows()
            break

def calcular_coef_angulo_interaccion(persp, stream, funcion, color_stream):
    print("************************")
    raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
    print("Coloque la plantilla delante de la camara")
    persp.calcular_coef_angulo(stream, color_stream, funcion)
    print("El coeficiente calculado es: " + str(persp.coef_correcion))
    raw_input("Retira la plantilla, pulsa intro para continuar")
    print("************************")

def imprimir_fps_stats(fps_stats):
    print("************************")
    print("Minimos fps: " + str(min(fps_stats)))
    print("Maximos fps: " + str(max(fps_stats)))
    print("Media fps: " + str(np.average(fps_stats)))
    print("************************")

def muestra_proceso(color_stream, funcion_binarizado, stream, persp):

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

        if color_stream is 0:
            _, img_correjida = funcion_binarizado(vid)
            img_binarizada = persp.correjir_distorsion_perspectiva(img_correjida)
        else:
            img_binarizada = funcion_binarizado(img_correjida)
            img_correjida = persp.correjir_distorsion_perspectiva(vid)

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
            salir_evt[0] = False

if  __name__ =='__main__':
    main()