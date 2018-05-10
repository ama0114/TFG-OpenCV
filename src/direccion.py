# coding=utf-8
from scipy import stats
import numpy as np

class direccion:

    f_derecha = None
    f_izquierda = None
    rango_seguro_min = 0
    rango_seguro_max = 0

    def __init__(self, error, tam_horiz_frame):
        self.rango_seguro_min = (tam_horiz_frame/2)-(tam_horiz_frame*error/2)
        x = [0,(self.rango_seguro_min/2),self.rango_seguro_min]
        y = [90,45,0]
        slope_1, intercept_1, _, _, _ = stats.linregress(x, y)
        self.f_derecha = lambda i: float(intercept_1) + float(slope_1)*i

        self.rango_seguro_max = (tam_horiz_frame/2)+(tam_horiz_frame*error/2)
        x = [self.rango_seguro_max,
            self.rango_seguro_max+((tam_horiz_frame-self.rango_seguro_max)/2),
            tam_horiz_frame]
        y = [0,45,90]
        slope_2, intercept_2, _, _, _ = stats.linregress(x, y)
        self.f_izquierda = lambda j: float(intercept_2) + float(slope_2)*j
        

    def obtener_direccion(self, frame):
        angulo = 0
        texto = "R"
        try:
            pos = list(frame[142]).index(255)

            #Girar derecha
            if pos < self.rango_seguro_min:
                angulo = self.f_derecha(pos)
                if angulo > 45:
                    texto = "I"
                else:
                    texto = "RI"
                
            #Girar izquierda
            if pos > self.rango_seguro_max:
                angulo = self.f_izquierda(pos)
                if angulo > 45:
                    texto = "D"
                else:
                    texto = "RD"
        except ValueError:
            texto = "Error"

        return texto, angulo