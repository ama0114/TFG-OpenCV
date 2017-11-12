# coding=utf-8
from webcamStream import webcamStream
import cv2
import numpy as np

def main():
    stream = webcamStream('http://192.168.1.11:8080/shot.jpg')
    fpsStats = []
    while True:
        vid, fps = stream.getVideoStream(-1)
        fpsStats.append(fps)
        cv2.imshow('Streaming', vid)

        # salimos pulsando s
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Minimos fps: " + str(min(fpsStats)))
            print("Maximos fps: " + str(max(fpsStats)))
            print("Media fps: " + str(mean(fpsStats)))
            break

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

if  __name__ =='__main__':
    main()