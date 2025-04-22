import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir la función del SEDO como una función en Python
def lineal(V, t, a, b, c, d): #V es el vector de variables dependientes
    x, y = V
    dxdt = a*x + b*y
    dydt = c*x + d*y
    return [dxdt, dydt]

# Parámetros del Sistema
a = -1
b = -2
c = 1
d = -1


#Condiciones iniciales
x0 = 10
y0 = -30

# Vector de tiempo
tf=8 #tiempo final
t = np.linspace(0, tf, 2000)

# Condiciones iniciales como vector
V0 = [x0, y0]

# Resolver el SEDO con odeint
solution = odeint(lineal, V0, t, args=(a,b,c,d))

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
plt.scatter(x0,y0)
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()