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
        vid, fps = stream.get_video_stream(1)

        hsv =  hsv = cv2.cvtColor(vid, cv2.COLOR_BGR2HSV)

        #incremento saturacion
        hsv[:,:,1] += 100
        rgbimg = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # define range of yellow color in HSV
        lower_y = np.array([10,10,60])
        upper_y = np.array([50,255,255])

        #Binarizo
        img_binarizada = cv2.inRange(hsv, lower_y, upper_y)

        #Muestro la imagen
        cv2.imshow('Bin', img_binarizada)
        cv2.imshow('Original', rgbimg)

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

if  __name__ =='__main__':
    main()