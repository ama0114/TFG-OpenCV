# coding=utf-8
import cv2
import numpy as np

class perspectiva(object):
    """
    Clase de correcion de distorsion por perspectiva.
    Almacena la complejidad de la correcion de este tipo de distorsion.
    Provee metodos para calcular el angulo de la camara y corregir la distorsion.
    """

    def __init__(self):
        #Marco correcion origen
        self.src = None

        #Marco correcion destino
        self.dst = None

        #Coeficiente correcion
        self.coef_correcion = 0

    def deshacer_distorsion_perspectiva(self, frame):
        """
        Permite deshacer la vista de pajaro de una imagen.
        Parámetros:
        - frame: imagen de origen
        """

        M = cv2.getPerspectiveTransform(self.dst, self.src)

        warped_img = cv2.warpPerspective(frame, M, (len(frame[0]), len(frame)))

        return warped_img

    def correjir_distorsion_perspectiva(self, frame):
        """
        Permite obtener una vista de pajaro de la imagen.
        Parámetros:
        - frame: imagen de origen
        """

        M = cv2.getPerspectiveTransform(self.src, self.dst)

        warped_img = cv2.warpPerspective(frame, M, (len(frame[0]), len(frame)))

        return warped_img

    def calcular_coef(self, frame):
        """
        Calcula el coeficiente de reduccion en pixeles de la imagen
        en funcion del angulo que tiene la camara sobre el suelo.
        Se usará una plantilla con un cuadrado de proporciones conocidas.
        La funcion devuelve el coeficiente de reduccion.

        Parámetros:
        - frame: imagen binarizada.
        """
        coef = 0
        bottom_square = 0
        top_square = 0
        min_width = 0
        max_width = 0
        b = True
        t = True

        for i in range(len(frame)-2, -1, -1):
            if frame[i][len(frame[0])/2] == 255 and b:
                #Dejamos 2 pixeles de margen
                bottom_square = i-2
                b = False

            if bottom_square != 0 and frame[i][len(frame[0])/2] == 0 and t:
                #Dejamos 2 pixeles de margen
                top_square = i+2
                t = False

        min_width = sum(frame[top_square] > 0)
        max_width = sum(frame[bottom_square] > 0)
        if float(bottom_square - top_square > 0):
            coef = abs(float(min_width - max_width) / float(bottom_square - top_square))

        return coef

    def calcular_coef_angulo(self, stream, color_stream, funcion_binarizar):
        """
        Permite calcular el coeficiente que forma la camara con el suelo.
        Asigna a los atributos los valores necesarios.
        Parametros:
        - stream: flujo de datos de donde obtenemos la imagen.
        - color_stream: permite saber si la funcion a binarizar
        va a realizar un binarizado por color o por luminosidad.
        - funcion_binarizar: funcion que va a binarizar la imagen.
        """
        while True:
            #0 - B/N, 1 - Color RGB
            vid, fps = stream.get_video_stream(color_stream)

            #Binarizo
            if color_stream is 0:
                _, img_binarizada = funcion_binarizar(vid)
            else:
                img_binarizada = funcion_binarizar(vid)

            #Calculo angulo
            c = self.calcular_coef(img_binarizada)

            #Muestro la imagen
            cv2.imshow('Original', img_binarizada)

            # salimos pulsando s
            if cv2.waitKey(1) & 0xFF == ord('s'):

                cv2.destroyAllWindows()
                break

        self.coef_correcion = c
        self.generar_correctores(stream.get_frame(1))


    def generar_correctores(self, frame):
        """
        Genera los marcos correctores para la distorsion.
        Parametros:
        - frame: usado para obtener sus dimensiones y de ahí los marcos.
        """
        g = lambda x: 140.3462 + (101.7432 - 140.3462)/(1 + (x/0.5605076)**64.36072)
        tam_reducido = g(self.coef_correcion)
        
        self.src = np.float32([[0, len(frame)-1], 
                            [len(frame[0])-1, len(frame)-1], 
                            [0, 0], 
                            [len(frame[0])-1, 0]])
                            
        self.dst = np.float32([[tam_reducido/2, len(frame)-1], 
                            [len(frame[0])-tam_reducido/2, len(frame)-1], 
                            [0, 0], 
                            [len(frame[0])-1, 0]])