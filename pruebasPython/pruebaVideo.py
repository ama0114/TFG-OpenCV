# coding=utf-8
"""Reproducción de un archivo de video 
    con OpenCV.
    Código obtenido en:
        http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
"""
import cv2

#Abrimos el video
cap = cv2.VideoCapture('recIzq.avi')

#Mientras el video esta abierto
while cap.isOpened():

    #Leemos por fotogramas el video
    ret, frame = cap.read()

    #Interpretamos el video en escala de grises, suficiente para poder detectar la linea
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Visualizamos el video
    cv2.imshow('frame', gray)

    #Lo podemos cerrar presionando la tecla q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
