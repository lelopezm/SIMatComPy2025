import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Ley de Enfriamiento-Calentamiento de Newton
#t: tiempo en minutos
#x: temperatura (C)
#Tm: temperatura ambiente constante
def f(x,t,k,Tm):
    return k*(x-Tm)

#tiempo final y número de iteraciones 
tf=20
#condiciones iniciales
t0=0
x0=75
#parámetros
k=-0.15  #tasa de enfriamiento
Tm=18

#Solución
time=np.linspace(t0,tf,200)
Sol = odeint(f,x0,time,args=(k,Tm)) 
Temp=Sol[:,0]

#gráfica de la solución
plt.plot(time,Temp,'#aa1e0e')
plt.grid()
plt.xlabel('tiempo')
plt.ylabel('Temperatura')
plt.title('Ley de Newton')
plt.show()