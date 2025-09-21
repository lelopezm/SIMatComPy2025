import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#ventana
ax=-10
bx=10
ay=-5
by=5

#umbral
w=0

# sistema 1 (inestable) ROJO matriz A
a1 = 1
b1 = -1
c1 = 5
d1 = -3

# sistema 2 (estable) VERDE matriz B
a2 = -1
b2 = -2
c2 = 1
d2 = -1

# Campo vectorial 1
h=0.5 #cantidad de vectores (horizontal como vertical)
X1, Y1 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, w + h, h))
dXdt1 = a1*X1 + b1*Y1
dYdt1 = c1*X1 + d1*Y1


# Campo vectorial 2
h=0.5 #cantidad de vectores (horizontal como vertical)
X2, Y2 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(w, by + h, h))
dXdt2 = a2*X2 + b2*Y2
dYdt2 = c2*X2 + d2*Y2

plt.streamplot(X1, Y1, dXdt1, dYdt1, color='red',linewidth=0.6)
plt.streamplot(X2, Y2, dXdt2, dYdt2, color='green',linewidth=0.6)
plt.grid(True)
plt.show()
