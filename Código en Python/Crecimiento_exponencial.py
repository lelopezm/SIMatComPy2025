import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def modelo(y, t, k):
    dydt = k * y
    return dydt

# Parámetros
k = 0.5
y0 = 1.0  # Condición inicial
t = np.linspace(0, 10, 100)  # Tiempos de solución

# Resolver la EDO
solucion = odeint(modelo, y0, t, args=(k,))

# Graficar la solución
plt.plot(t, solucion)
plt.xlabel('Tiempo')
plt.ylabel('y(t)')
plt.title('Solución de dy/dt = ky')
plt.grid(True)
plt.show()