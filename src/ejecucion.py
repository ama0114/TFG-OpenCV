# coding=utf-8
from webcam_stream import webcam_stream
from binarizar_hsv import binarizar_hsv
from direccion import direccion
from perspectiva import perspectiva
from matplotlib import pyplot as plt

import cv2
import numpy as np
import toolbox

def main():
    """
    Programa principal
    """
    
    stream = get_url_stream()
    persp = perspectiva()
    bin_hsv = binarizar_hsv()

    menu(stream, persp, bin_hsv)

def get_url_stream():
    ex = True
    while ex is True:
        try:
            url = raw_input("Dime la url del servidor de video: ")
            stream = webcam_stream(url + "/shot.jpg")
            stream.get_video_stream(0)
            ex = False
        except:
            print("Error, no se ha podido conectar con la url: " + url)

    return stream

def crear_marco_comparacion(img):
    """
    Crea con matplotlib una ventana para mostrar 4
    imagenes simultaneamente.
    Devuelve los 4 espacios donde se dibujaran las imagenes.
    Parametros
    - img: Imagen de la misma resolución que las imagenes
            que se vayan a dibujar posteriormente.
    """

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

    """
    Recive cuatro espacios de imagenes y cuatro imagenes
    y pinta sobre los espacios las imagenes.
    Parámetros:
    - im_spc1, im_spc2, im_spc3, im_spc4: los cuatro espacios de imagenes.
    - im1, im2, im3, im4: las cuatro imagenes.
    """

    #Asigno las imagenes
    im_spc1.set_data(im1)
    im_spc2.set_data(im2)
    im_spc3.set_data(im3)
    im_spc4.set_data(im4)

    #Tiempo de pausa, lo menor posible para que el video se muestre fluido
    plt.pause(0.001)

def check_num_int(num):
    """Comprueba que una variable es númerica y entera y devuelve
    el numero entero asociado
    Parametros:
    -num: el numero a comprobar
    """
    try:
        num = int(num)
    except ValueError:
        print "Error. Introduce un numero entero\n"

    return num

def check_num_float(num):
    """Comprueba que una variable es númerica y decimal y devuelve
    el numero decimal asociado
    Parametros:
    -num: el numero a comprobar
    """
    try:
        num = float(num)
    except ValueError:
        print "Error. Introduce un numero decimal\n"

    return num

def menu(stream, persp, binarizar_hsv):
    """
    Menú principal de la aplicación.
    """

    opcion = -1
    while opcion is not 0:
        print "******* Menu ***********"

        opcion = raw_input(" 1-Prueba binarizar luminosidad \n" +
                       " 2-Prueba binarizar color \n" +
                       " 3-Muestra proceso \n"+
                       " 4-Ejecucion normal \n"+
                       " 0-Salir \n")
        opcion = check_num_int(opcion)

        print "************************"
        if opcion is 1:
            print "************************"
            print "Prueba binarizar por luminosidad, pulsa 's' para salir."
            print "************************"
            binarizar_luminosidad(stream)
            opcion = -1
        elif opcion is 2:
            print "************************"
            print "Prueba binarizar por color, pulsa 's' para salir."
            print "************************"
            binarizar_color(binarizar_hsv, stream)
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
            print "Error, intentalo de nuevo\n"


def binarizar_luminosidad(stream):
    """
    Seccion del menu que permite ejecutar una prueba
    de binarizacion por luminosidad.
    """
    fps_stats = []
    salir = False
    while not salir:
        vid, fps = stream.get_video_stream(0)
        umbral, img_binarizada = toolbox.binarizar_otsu(vid, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow('Original', vid)
        cv2.imshow('Bin_Lum', img_binarizada)
        fps_stats.append(fps)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            imprimir_fps_stats(fps_stats)
            print "Umbral de binarizacion: " + str(umbral)
            cv2.destroyAllWindows()
            salir = True

def binarizar_color(binarizar_hsv, stream):
    """
    Seccion del menu que permite ejecutar una prueba
    de binarizacion por luminosidad.
    """
    binarizar_hsv.calibrar_color(stream)

def menu_aux(stream, persp, binarizar_hsv, ejecucion):
    """
    Sub menu que permite elegir entre dos tipos de binarizacion
    para aplicar posteriormente otros metodos de procesado de imagen.
    """

    opcion = -1
    while opcion is not 0:

        print "************************"
        opcion = raw_input("1-Binarizar Color\n 2-Binarizar Luminosidad\n 0-Salir\n")
        print "************************"
        opcion = check_num_int(opcion)

        if opcion is 1:

            binarizar_color(binarizar_hsv, stream)
            calcular_coef_angulo_interaccion(persp, stream, binarizar_hsv.binarizar_frame, 1)
            ejecucion(1, binarizar_hsv.binarizar_frame, stream, persp)

        elif opcion is 2:

            def funcion_adaptador(frame):
                """
                Adapto la funcion de binarizacion para que solo reciba un parametro.
                Consigo poder pasar esta funcion por parametro.
                """
                umbral, frame = toolbox.binarizar_otsu(frame, 255, cv2.THRESH_BINARY_INV)
                return umbral, frame

            calcular_coef_angulo_interaccion(persp, stream, funcion_adaptador, 0)
            ejecucion(0, funcion_adaptador, stream, persp)

        elif opcion is 0:
            opcion = -1
            break
        else:
            print "************************"
            print "Error, introduce una opcion correcta\n"
            print "************************"

def pinta_indicadores(frame, dir):
    """
    Permite pintar los indicadores de direccion en la imagen.
    Devuelve la imagen con los indicadores pintados.
    Parametros
    - frame: imagen donde vamos a pintar los indicadores.
    - dir: objeto del tipo direccion
    """
    centro = [len(frame[0])/2, (len(frame[0])/2)-1]
    rango = [int(dir.rango_seguro_min), int(dir.rango_seguro_max)]
    for i in range(len(frame)-1, len(frame)-10, -1):
        for j in centro:
            frame.itemset((i, j, 0), 0)
            frame.itemset((i, j, 1), 255)
            frame.itemset((i, j, 2), 0)
        for j in rango:
            frame.itemset((i, j, 0), 0)
            frame.itemset((i, j, 1), 0)
            frame.itemset((i, j, 2), 255)
    return frame

def ejecucion_normal(color_stream, funcion_binarizado, stream, persp):
    """
    Seccion del menu que permite realizar la ejecución normal del programa.
    """
    fps_stats = []

    rango_seguro = -1
    while rango_seguro > 0.3 or rango_seguro < 0:
        rango_seguro = raw_input("Dime el rango seguro para la direccion\n min=0, max=0.3\n")
        rango_seguro = check_num_float(rango_seguro)

    ang_giro_max = -1
    while ang_giro_max > 90 or ang_giro_max < 0:
        ang_giro_max = raw_input("Dime el angulo de giro maximo del vehiculo[Valor entero]: ")
        ang_giro_max = check_num_int(ang_giro_max)

    dir = direccion(rango_seguro, len(stream.get_frame(1)[0]), ang_giro_max)
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

        vid = toolbox.pintar_lineas(vid, tray_normal, [255, 0, 0])
        vid = pinta_indicadores(vid, dir)

        vid_persp = toolbox.pintar_lineas(vid_persp, bordes_persp, [0, 255, 0])
        vid_persp = toolbox.pintar_lineas(vid_persp, tray_persp, [255, 0, 0])

        cv2.putText(vid, texto + "              " + str(round(angulo, 2)),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)

        cv2.putText(vid_persp,
                    "Lum:              " + str(round(toolbox.calcular_luminosidad(vid), 2)),
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)

        cv2.putText(vid_persp, "Fps:              " + str(round(fps, 2)),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)

        if color_stream is 0:
            cv2.putText(vid_persp, "Umb:              " + str(round(umbral, 2)),
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)

        cv2.imshow('Guia', vid)
        cv2.imshow('Tray', vid_persp)

        fps_stats.append(fps)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            imprimir_fps_stats(fps_stats)
            cv2.destroyAllWindows()
            break

def calcular_coef_angulo_interaccion(persp, stream, funcion, color_stream):
    """
    Sub menu que nos permite calibrar el angulo para resolver la distorsion
    por perspectiva.
    Parametros:
    - persp: objeto del tipo perspectiva.
    - stream: objeto del tipo webcam_stream.
    - funcion: funcion de binarizado.
    - color_stream: 0 si es binarizado por luminosidad, 1 binarizado por color.
    """
    print "************************"
    raw_input("Pulsa intro para calcular el coeficiente de correcion de distorsion por perspectiva")
    print "Coloque la plantilla delante de la camara"
    persp.calcular_coef_angulo(stream, color_stream, funcion)
    print "El coeficiente calculado es: " + str(persp.coef_correcion)
    raw_input("Retira la plantilla, pulsa intro para continuar")
    print "************************"

def imprimir_fps_stats(fps_stats):
    """
    Imprime los fps.
    Parametros:
    - fps_stats: array de numeros.
    """
    print "************************"
    print "Minimos fps: " + str(min(fps_stats))
    print "Maximos fps: " + str(max(fps_stats))
    print "Media fps: " + str(np.average(fps_stats))
    print "************************"

def muestra_proceso(color_stream, funcion_binarizado, stream, persp):
    """
    Sub menu que nos permite mostrar el proceso que realiza el programa,
    mostrando como se van procesando las imagenes en las diferentes fases.
    Parametros:
    - color_stream: 0 binarizacion por luminosidad, 1 binarizacion por color.
    - funcion_binarizado: funcion que nos permite realizar la binarizacion.
    - stream: objeto del tipo webcam_stream
    - persp: objeto del tipo perspectiva
    """

    salir_evt = [False]
    fps_stats = []
    im_spc1, im_spc2, im_spc3, im_spc4, fig = crear_marco_comparacion(stream.get_frame(1))

    def handle_close(evt):
        """
        Funcion auxiliar usada para recoger el evento de cierre de la ventana
        de matplotlib
        """
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
            img_correjida = persp.correjir_distorsion_perspectiva(vid)
            img_binarizada = funcion_binarizado(img_correjida)

        bordes = toolbox.obtener_contornos(img_binarizada, 50, 200)
        tray = toolbox.obtener_trayectoria(bordes)
        bordes_tray = bordes + tray

        fig.canvas.mpl_connect('close_event', handle_close)

        if color_stream is 1:
            vid = cv2.cvtColor(vid, cv2.COLOR_RGB2BGR)
            img_correjida = cv2.cvtColor(img_correjida, cv2.COLOR_RGB2BGR)

        mostrar_comparacion_imagenes(im_spc1, im_spc2, im_spc3,
                                     im_spc4, vid, img_correjida,
                                     img_binarizada, bordes_tray)

        if salir_evt[0] is True:
            imprimir_fps_stats(fps_stats)
            cv2.destroyAllWindows()
            salir = True
            salir_evt[0] = False

if  __name__ == '__main__':
    main()
