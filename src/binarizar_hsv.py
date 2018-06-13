# coding=utf-8
from webcam_stream import webcam_stream
import cv2
import numpy as np
from matplotlib import pyplot as plt
import toolbox

class binarizar_hsv:

    color_bin = [[0,0,0]]

    def __init__(self):
        pass

    def binarizar_frame(self, frame):
        """Binariza una imagen mediante HSV
            Paramatros
            - Frame: fotograma a binarizar, en formato RGB
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color = np.array(self.color_bin[0])
        lower_y = color - 20
        upper_y = color + 20

        #Binarizo
        img_binarizada = cv2.inRange(hsv, lower_y, upper_y)

        return img_binarizada

    def calibrar_color(self):
        stream = webcam_stream('http://192.168.1.10:8080/shot.jpg')
        color_bin = [[0,0,0]]
        salir = False

        def on_mouse_click (event, x, y, flags, frame):
            if event == cv2.EVENT_LBUTTONUP:
                #print(frame[y,x].tolist())
                del color_bin[:]
                color_bin.append(frame[y,x].tolist())
        
        while not salir:
            #0 - B/N, 1 - Color RGB
            vid, fps = stream.get_video_stream(1)

            hsv = cv2.cvtColor(vid, cv2.COLOR_BGR2HSV)

            color = np.array(color_bin[0])
            lower_y = color - 20
            upper_y = color + 20

            #Binarizo
            img_binarizada = cv2.inRange(hsv, lower_y, upper_y)

            #Muestro la imagen
            cv2.imshow('Bin_Col', img_binarizada)
            cv2.imshow('Original', vid)

            cv2.setMouseCallback('Original', on_mouse_click, hsv)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print("Color calibrado")
                cv2.destroyAllWindows()
                salir = True

        self.color_bin = color_bin