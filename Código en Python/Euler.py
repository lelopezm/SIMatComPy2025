import numpy as np
import matplotlib.pyplot as plt

#Función f(t,x)
def f(t,x):
    return -x + np.sin(t)

#Definimos condición inicial y final
t0=0
tf=20
x0=5
n=2000 #cantidad de puntos
h=(tf-t0)/n
#Vectores de la solución aproximada
T=[t0]
X=[x0]
for i in range(1,n+1):
    t1=t0+h
    T.append(t1)
    x1=x0+h*f(t0,x0)
    X.append(x1)
    t0=t1
    x0=x1

#Grafica de la solución
#solucion exacta
#t0=0
#t=np.linspace(t0,tf,150)
#x=np.sqrt(1-t**2)
#Error final
#Ef=X[-1]-x[-1]
#print(Ef)
#plt.plot(t,x,color=(1,0,0),linewidth=1.5)
plt.plot(T,X,color=(0,0,0),linewidth=2)
plt.grid()
#plt.axis([0,1,0,1])
plt.show()


