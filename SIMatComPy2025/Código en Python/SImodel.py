#En este archivo escribir el código para resolver el modelo SI (Susceptible-Infectado)
# S' = -beta*S*I
# I' = beta*S*I - gamma*I
# Toman como condición iniciales: S0=0.9, I0=0.1
# y los valores de beta=0.2 y gamma = 0.1 
# en tiempo t en [0,60]

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt