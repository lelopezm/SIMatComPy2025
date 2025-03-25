import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir la función del SEDO como una función en Python
def SEDO(V, t, a): #V es el vector de variables dependientes
    x, y = V
    dxdt = - y + a * x * (x**2 + y**2)
    dydt = x + a * y * (x**2 + y**2)
    return [dxdt, dydt]

# Parámetros del SEDO
a = -5


#Condiciones iniciales
x0 = 3
y0 = 0.5

# Vector de tiempo
t = np.linspace(0, 200, 5000)

# Condiciones iniciales como vector
V0 = [x0, y0]

# Resolver el SEDO con odeint
solution = odeint(SEDO, V0, t, args=(a,))

# Extraer las soluciones de solution
X, Y = solution.T

# Gráfica de las soluciones
plt.subplot(1,2,1)
plt.plot(t,X, label='Solución x(t)')
plt.plot(t,Y, label='Solución y(t)')
plt.xlabel('tiempo t')
plt.ylabel('Soluciones')
plt.title('Soluciones del SEDO')
plt.legend()
plt.grid()

plt.subplot(1,2,2)
plt.plot(X,Y)
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()