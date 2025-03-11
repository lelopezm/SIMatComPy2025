import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Función f
def f(x,t):
    return -x + 10

#tiempo
t0=0
tf=10*np.pi

#condición inicial
x0=1

#cantidad de puntos a graficar
n=250

#Solución aproximada 
T=np.linspace(t0,tf,n)
Sol = odeint(f,x0,T) 
X=Sol[:,0]

Xp=f(X,T) #definimos los valores de x prima (derivada)

#gráfica de la solución
plt.subplot(1,2,1)
plt.plot(T,X,'#aa1e0e')
plt.grid()
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Solución con ODEINT')

plt.subplot(1,2,2)
plt.plot(X,Xp,'#aa1e0e')
plt.grid()
plt.xlabel('x(t)')
plt.ylabel('dxdt')
plt.title('Diagrama de fase')
plt.show()


#VERIFICAR RESULTADOS, NO COINCIDEN
