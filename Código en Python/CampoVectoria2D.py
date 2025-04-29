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
ax=0
bx=500
ay=0
by=500

# Parámetros de competencia
# a = 3
# b = -1
# c = -2
# d = 2

# Parámetros de depredador-presa
a = 2
b = -1
c = 1
d = 4

# Campo vectorial
h=1 #cantidad de vectores (horizontal como vertical)
X, Y = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, by + h, h))
dXdt = a*X + b*Y
dYdt = c*X + d*Y

#plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.grid(True)

#Condiciones iniciales
x0 = 500
y0 = 100

# Solucion con condicion inicial [x0,y0]
tf=5/6 #tiempo final
t = np.linspace(0, tf, 200)

# Condiciones iniciales como vector
V0 = [x0, y0]

# Resolver el SEDO con odeint
solution = odeint(lineal, V0, t, args=(a,b,c,d))

# Extraer las soluciones de solution
Xt, Yt = solution.T

# Gráfica de las soluciones
plt.subplot(1,2,1)
plt.plot(t,Xt, label='Solución x(t)')
plt.plot(t,Yt, label='Solución y(t)')
plt.xlabel('tiempo t')
plt.ylabel('Soluciones')
plt.title('Soluciones del SEDO')
plt.legend()
plt.grid()

plt.subplot(1,2,2)
plt.streamplot(X, Y, dXdt, dYdt, color=(0/255, 180/255, 250/255),linewidth=0.6)
plt.plot(Xt,Yt,color='red',linewidth=2) #solucion particular
plt.scatter(x0,y0)
plt.xlim([ax,bx])
plt.ylim([ay,by])
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()