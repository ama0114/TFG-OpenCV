# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np

class binarizar_hsv(object):
    """
    Clase de binarizado. Engloba toda la complejidad de
    la binarizacion por color.
    """

    def __init__(self):
        self.color_bin = [[0, 0, 0]]

    def binarizar_frame(self, frame):
        """
        Binariza una imagen mediante HSV
        Devuelve la imagen binarizada.
        Paramatros
        - Frame: fotograma a binarizar, en formato RGB
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_y, upper_y = self.generar_rangos()

        #Binarizo
        img_binarizada = cv2.inRange(hsv, lower_y, upper_y)

        return img_binarizada

    def calibrar_color(self):
        """
        Permite calibrar el color mediante ventanas de opencv.
        """
        stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')
        salir = False

        def on_mouse_click(event, x, y, flags, frame):
            """
            Captura el evento de hacer click con el raton
            en la ventana. Actualiza el color con los valores
            del pixel donde se ha pinchado.
            """
            if event == cv2.EVENT_LBUTTONUP:
                #print(frame[y,x].tolist())
                del self.color_bin[:]
                self.color_bin.append(frame[y, x].tolist())

        while not salir:
            #0 - B/N, 1 - Color RGB
            vid, fps = stream.get_video_stream(1)

            hsv = cv2.cvtColor(vid, cv2.COLOR_BGR2HSV)

            lower_y, upper_y = self.generar_rangos()

            #Binarizo
            img_binarizada = cv2.inRange(hsv, lower_y, upper_y)

            #Muestro la imagen
            cv2.imshow('Bin_Col', img_binarizada)
            cv2.imshow('Original', vid)

            cv2.setMouseCallback('Original', on_mouse_click, hsv)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print "Color calibrado"
                cv2.destroyAllWindows()
                salir = True

    def generar_rangos(self):
        """
        Genera unos rangos de color para llevar a cabo la binarización.
        """

        color = np.array(self.color_bin[0])
        lower_y = np.copy(color)
        upper_y = np.copy(color)

        #Ajustando los rangos de color, saturacion y luminosidad
        #Para captar diferentes variaciones del color
        lower_y[0] = lower_y[0]-20 if lower_y[0]-20 > 0 else 0
        lower_y[1] = lower_y[1]-100 if lower_y[1]-100 > 0 else 0
        lower_y[2] = lower_y[2]-100 if lower_y[2]-100 > 0 else 0

        upper_y[0] = upper_y[0]+20
        upper_y[1] = upper_y[1]+100 if upper_y[1]+100 < 256 else 255
        upper_y[2] = upper_y[2]+100 if upper_y[2]+100 < 256 else 255

        return lower_y, upper_y
