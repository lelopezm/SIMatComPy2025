#ACTIVIDAD 1 SEMILLER0
#En este código importamos los datos que estan en el archivo datos_efriamiento.xlsx y con ellos ajustamos la EDO del Enfriamiento de Newton
# tomando: T0=72 (temperatura inicial), Tm=20 (temperatura ambiente) y,
#el objetivo es hallar el valor de k (tasa de enfriamiento)
#RESPUESTA: Aproximadamente el valor de k es -0.12


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint