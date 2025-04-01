#En este archivo escribir el código para resolver el modelo SI (Susceptible-Infectado)
# S' = -beta*S*I
# I' = beta*S*I - gamma*I
# Toman como condición iniciales: S0=0.9, I0=0.1
# y los valores de beta=0.2 y gamma = 0.1 
# en tiempo t en [0,60]

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Defining the SImodel function
def SEDO(v, t, b, g): # v: vector de variables dependientes
    s, i = v
    dsdt = -b*s*i
    didt = b*s*i - g*i

    return [dsdt, didt]


# Parametros del sistema
b = 0.2 # Tasa de infección
g = 1/7 # Tasa de recuperación

# Condiciones iniciales
s0 = 0.7 # Proporción de la población susceptible
i0 = 0.3 # Proporción de la población infectada


# Vector de tiempo t
t = np.linspace(0, 150, 1000) # 100 puntos entre 0 y 10


# Vector de condiciones iniciales
v0 = [s0, i0]

# Resolviendo el sistema de ecuaciones diferenciales
sol = odeint(SEDO, v0, t, args=(b, g))

s = sol[:, 0]
i = sol[:, 1]

# Graficando los resultados
plt.subplot(1, 2, 1)
plt.plot(t, s, label='x(t)', color='blue')
plt.plot(t, i, label='y(t)', color='red')
plt.title('Solución del sistema de ecuaciones diferenciales')
plt.xlabel('Tiempo')
plt.ylabel('Valores de x y y')
plt.legend()
plt.grid()

# Plano de fase
plt.subplot(1, 2, 2)
plt.plot(s, i, color='green')
plt.title('Plano de fase')
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.grid()


plt.show()
