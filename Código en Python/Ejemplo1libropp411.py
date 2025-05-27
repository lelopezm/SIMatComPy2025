import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir la función del SEDO como una función en Python
def lineal(V, t, a, b, c, d): #V es el vector de variables dependientes
    x, y = V
    dxdt = a*x + b*y
    dydt = c*x + d*y
    return [dxdt, dydt]

#ventana
ax=-1
bx=1
ay=-1
by=1


# Parámetros
a = -1
b = 1
c = -9 #parametro que varia
d = -1

# Campo vectorial
h=1 #cantidad de vectores (horizontal como vertical)
X, Y = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, by + h, h))
dXdt = a*X + b*Y
dYdt = c*X + d*Y

#plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.xlim([ax,bx])
plt.ylim([ay,by])
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()