import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Función f(t,x)
def f(t,x):
    return -x + np.sin(t)

#tiempo
t0=0
tf=2*np.pi

#condición inicial
x0=5

#cantidad de puntos a graficar
n=250

#Solución aproximada 
T=np.linspace(t0,tf,n)
Sol = odeint(f,x0,T) 
X=Sol[:,0]

#gráfica de la solución
plt.plot(T,X,'#aa1e0e')
plt.grid()
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Solución con ODEINT')
plt.show()


#VERIFICAR RESULTADOS, NO COINCIDEN
