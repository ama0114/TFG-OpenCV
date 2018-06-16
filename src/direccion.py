# coding=utf-8
from scipy import stats

class direccion(object):
    """
    Clase direccion. Implementa un modelo de direccion simple,
    que detecta si nos encontramos a la derecha o a la izquierda
    de la trayectoria ideal generada por la linea.
    Permite guardar un margen de seguridad para no generar correciones
    contiunamente. Si nos salimos de ese marjen de seguridad, nos
    redirecionará al centro de la linea otra vez.

    Se generan unas funciones lambda que permiten corregir el rumbo de
    forma dinamica. Contra más nos alejemos del centro de la linea,
    mas nos mandará el programa corregir el rumbo (más angulo nos mostrará).
    """

    def __init__(self, error, tam_horiz_frame):
        self.rango_seguro_min = (tam_horiz_frame/2)-(tam_horiz_frame*error/2)
        self.rango_seguro_min_bkp = (tam_horiz_frame/2)-(tam_horiz_frame*error/2)
        self.rango_seguro_max = (tam_horiz_frame/2)+(tam_horiz_frame*error/2)
        self.rango_seguro_max_bkp = (tam_horiz_frame/2)+(tam_horiz_frame*error/2)
        self.f_derecha = self.calcular_fcn_drch()
        self.f_izquierda = self.calcular_fcn_izq(tam_horiz_frame)

    def calcular_fcn_izq(self, tam_horiz_frame):
        """
        Calcula la función lambda que se va a usar a la hora de
        tener que girar a la izquierda.
        Devuelve la funcion.
        Parametros:
        - tam_horiz_frame: tamaño horizontal de la imagen.
        """
        x = [self.rango_seguro_max,
             self.rango_seguro_max+((tam_horiz_frame-self.rango_seguro_max)/2),
             tam_horiz_frame]
        y = [0, 45, 90]
        slope_2, intercept_2, _, _, _ = stats.linregress(x, y)
        return lambda j: float(intercept_2) + float(slope_2)*j

    def calcular_fcn_drch(self):
        """
        Calcula la función lambda que se va a usar a la hora de
        tener que girar a la derecha.
        Devuelve la funcion.
        """
        x = [0, (self.rango_seguro_min/2), self.rango_seguro_min]
        y = [90, 45, 0]
        slope_1, intercept_1, _, _, _ = stats.linregress(x, y)
        return lambda i: float(intercept_1) + float(slope_1)*i

    def obtener_direccion(self, frame):
        """
        Obtiene la dirección para guiar al vehiculo.
        Recibe la imagen de la camara.
        Devuelve un texto R(Recto), RI(Recto-Izquierda), 
        RD(Recto-Derecha), I(Izquierda), D(Derecha) o Error.
        RI y RD se mostraran cuando el angulo de giro no sea menor a 45 grados.
        I y D se mostraran cuando el angulo de giro sea mayor a 45 grados.
        Error se mostrara cuando no se encuentre una linea.
        Parametros:
        - frame: imagen con la que se va a calcuar la dirección.
        """
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
