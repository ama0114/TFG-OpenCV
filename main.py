# coding=utf-8
from webcamStream import webcamStream
import cv2

def main():
    stream = webcamStream('http://192.168.1.11:8080/shot.jpg')
   
    while True:      
        cv2.imshow('Streaming', stream.getVideoStream(-1))

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

if  __name__ =='__main__':
    main()