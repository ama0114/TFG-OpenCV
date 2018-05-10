# coding=utf-8
import cv2
import numpy as np

class perspectiva:

    src = None
    dst = None

    def __init__(self, frame, coef):
        g = lambda x: 140.3462 + (101.7432 - 140.3462)/(1 + (x/0.5605076)**64.36072)
        tam_reducido = g(coef)
        

        self.src = np.float32([[0, len(frame)-1], 
                            [len(frame[0])-1, len(frame)-1], 
                            [0, 0], 
                            [len(frame[0])-1, 0]])
                            
        self.dst = np.float32([[tam_reducido/2, len(frame)-1], 
                            [len(frame[0])-tam_reducido/2, len(frame)-1], 
                            [0, 0], 
                            [len(frame[0])-1, 0]])

    def correjir_distorsion_perspectiva(self, frame):
        """
        Permite obtener una vista de pajaro de la imagen de origen.
        Parámetros:
        - frame: imagen de origen
        """

        M = cv2.getPerspectiveTransform(self.src, self.dst) 

        warped_img = cv2.warpPerspective(frame, M, (len(frame[0]), len(frame))) 

        return warped_img