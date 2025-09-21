import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#Campo rojo
def rojo(V, t): #V es el vector de variables dependientes
    x, y = V
    dxdt = y - x**2 + 2
    dydt = x**2 - x*y
    return [dxdt, dydt]

#Campo azul
def azul(V, t): #V es el vector de variables dependientes
    x, y = V
    dxdt = y**2 - x**2
    dydt = -x*y
    return [dxdt, dydt]

#ventana
ax=-3
bx=3
ay=0
by=3

#umbral
w=1

# Campo vectorial 1 (rojo)
h=0.5 #cantidad de vectores (horizontal como vertical)
X1, Y1 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, w + h, h))
dXdt1 = Y1 - X1**2 + 2
dYdt1 = X1**2 - X1*Y1 

# Campo vectorial 2 (azul)
h=0.5 #cantidad de vectores (horizontal como vertical)
X2, Y2 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(w, by + h, h))
dXdt2 = Y2**2 - X2**2
dYdt2 = -X2*Y2

#SOLUCION DEL SISTEMA
#Condiciones iniciales
x0 = -1.5
y0 = 0

# Vector de tiempo
tf=1 #tiempo final
t = np.linspace(0, tf, 2000)

# Condiciones iniciales como vector
V0 = [x0, y0]




##GRAFICAS
plt.streamplot(X1, Y1, dXdt1, dYdt1, color='red',linewidth=0.6)
plt.streamplot(X2, Y2, dXdt2, dYdt2, color='blue',linewidth=0.6)
plt.grid(True)
plt.show()
