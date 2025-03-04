import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#definimos f(t,x) de x'=f(t,x)
def f(x,t):
    return -t/x

#tiempo final y número de iteraciones 
tf=1
n=4
#condiciones iniciales
t0=0
x0=1

#Solución aproximada 
T=np.linspace(t0,tf,n)
Sol = odeint(f,x0,T) 
X=Sol[:,0]

#gráfica de la solución
plt.figure(figsize=(10, 6))
plt.plot(T,X,'#12CFE1')
plt.grid()
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Solución de \dot{x}=-t/x, x(0)=1')
plt.show()

#RESULTADOS NUMÉRICOS
h=(tf-t0)/n #tamaño de paso
ve=0 #valor exacto de x(tf)
X_aprox=X[-1] #valor aproximado con odeint
E=abs(X_aprox-ve)
print('Valor exacto: x(%d)=%.6f'%(tf,ve))
print('Valor aproximado: x(%d)=%1.6f'%(tf,X_aprox))
print('Error estimado: E=%1.12f con un tamaño de paso h=%1.3f'%(E,h))