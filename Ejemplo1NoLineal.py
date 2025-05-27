import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir la función del SEDO como una función en Python
def lineal(V, t): #V es el vector de variables dependientes
    x, y = V
    dxdt = x - y
    dydt = x**2*y - 4*x
    return [dxdt, dydt]

#ventana
ax=-10
bx=10
ay=-10
by=10


# Campo vectorial
h=0.2 #cantidad de vectores (horizontal como vertical)
X, Y = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, by + h, h))
dXdt = X - Y
dYdt = X**2*Y - 4*X

#plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.scatter(-2,-2) #Punto de equilibrio 1
plt.scatter(0,0) #Punto de equilibrio 2
plt.scatter(2,2) #Punto de equilibrio 3
plt.xlim([ax,bx])
plt.ylim([ay,by])
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()