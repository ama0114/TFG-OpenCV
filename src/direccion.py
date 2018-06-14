# coding=utf-8
from scipy import stats
import numpy as np

class direccion:

    def __init__(self, error, tam_horiz_frame):
        self.rango_seguro_min = (tam_horiz_frame/2)-(tam_horiz_frame*error/2)
        self.rango_seguro_min_bkp = (tam_horiz_frame/2)-(tam_horiz_frame*error/2)
        self.rango_seguro_max = (tam_horiz_frame/2)+(tam_horiz_frame*error/2)
        self.rango_seguro_max_bkp = (tam_horiz_frame/2)+(tam_horiz_frame*error/2)
        self.f_derecha = self.calcular_fcn_drch()
        self.f_izquierda = self.calcular_fcn_izq(tam_horiz_frame)

    def calcular_fcn_izq(self, tam_horiz_frame):
        x = [self.rango_seguro_max,
            self.rango_seguro_max+((tam_horiz_frame-self.rango_seguro_max)/2),
            tam_horiz_frame]
        y = [0,45,90]
        slope_2, intercept_2, _, _, _ = stats.linregress(x, y)
        return lambda j: float(intercept_2) + float(slope_2)*j

    def calcular_fcn_drch(self):
        x = [0,(self.rango_seguro_min/2),self.rango_seguro_min]
        y = [90,45,0]
        slope_1, intercept_1, _, _, _ = stats.linregress(x, y)
        return lambda i: float(intercept_1) + float(slope_1)*i
        
    def obtener_direccion(self, frame):
        angulo = 0
        texto = "R"
        try:
            pos = list(frame[142]).index(255)

            #Girar derecha
            if pos < self.rango_seguro_min:
                if pos in range(int(len(frame[0])/2)-2, int(len(frame[0])/2)+2):
                    self.rango_seguro_min = self.rango_seguro_min_bkp
                else:
                    self.rango_seguro_min = len(frame[0])/2

                self.f_derecha = self.calcular_fcn_drch()
                angulo = self.f_derecha(pos)
                if angulo > 45:
                    texto = "I"
                else:
                    texto = "RI"
                
            #Girar izquierda
            if pos > self.rango_seguro_max:
                if pos in range(int(len(frame[0])/2)-2, int(len(frame[0])/2)+2):
                    self.rango_seguro_max = self.rango_seguro_max_bkp
                else:
                    self.rango_seguro_max = len(frame[0])/2

                self.f_izquierda = self.calcular_fcn_izq(len(frame[0]))
                angulo = self.f_izquierda(pos)
                if angulo > 45:
                    texto = "D"
                else:
                    texto = "RD"
        except ValueError:
            texto = "Error"

        return texto, angulo