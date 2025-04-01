import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Ley de Enfriamiento-Calentamiento de Newton
#t: tiempo en minutos
#x: temperatura (F)
def f(x,t,k,T0,T1,w):
    Tm = T0 + T1*np.cos(w*t) #temperatura ambiente
    dxdt = k*(x-Tm)
    return dxdt

#tiempo final y número de iteraciones 
tf=72
#condiciones iniciales
t0=0
x0=80
#parámetros
k=-0.2
T0=60  
T1=15
w=np.pi/12
#Solución
time=np.linspace(t0,tf,200)
Sol = odeint(f,x0,time,args=(k,T0,T1,w)) 
Temp=Sol[:,0]

#gráfica de la solución
plt.plot(time,Temp,'#aa1e0e')
plt.grid()
plt.xlabel('tiempo')
plt.ylabel('Temperatura')
plt.title('Ley de Newton')
plt.show()