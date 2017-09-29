"""Reproducción de un archivo de video 
    con OpenCV.
"""
import cv2

#Abrimos el video
cap = cv2.VideoCapture('recIzq.avi')

#Mientras el video esta abierto
while cap.isOpened():
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', gray)

    #Lo podemos cerrar presionando la tecla q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
