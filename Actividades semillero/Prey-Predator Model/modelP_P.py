import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#ventana
ax=0
bx=1.2 
ay=0
by=2

#umbral
w=1.625 #alpha

# sistema 1 
def sistema1(V, t, a, b, d): #V es el vector de variables dependientes
    x, y = V
    dxdt = x*(1-x) - (a*x*y)/(b+x)
    dydt = a*x*y/(b+x) - d*y
    return [dxdt, dydt]

# sistema 2
def sistema2(V, t, a, b, d, E): #V es el vector de variables dependientes
    x, y = V
    dxdt = x*(1-x) - (a*x*y)/(b+x)
    dydt = a*x*y/(b+x) - d*y - E*y
    return [dxdt, dydt] 

# parametros
a = 0.3556
b = 0.33    
d = 0.0444
E = 0.2067  

# Campo vectorial 1
X = np.linspace(ax, bx, 20)
Y = np.linspace(ay, w, 20)
X1, Y1 = np.meshgrid(X, Y)
U1 = X1*(1-X1) - (a*X1*Y1)/(b+X1)
V1 = (a*X1*Y1)/(b+X1) - d*Y1
N1 = np.sqrt(U1**2 + V1**2)
U1, V1 = U1/N1, V1/N1  # Normalizar
# Campo vectorial 2
X = np.linspace(ax, bx, 20)
Y = np.linspace(w, by, 20)
X2, Y2 = np.meshgrid(X, Y)
U2 = X2*(1-X2) - (a*X2*Y2)/(b+X2)
V2 = (a*X2*Y2)/(b+X2) - d*Y2 - E*Y2
N2 = np.sqrt(U2**2 + V2**2)
U2, V2 = U2/N2, V2/N2  # Normalizar 

#Puntos tangentes
t1x=d*b/(a-d)
t1y=w
t2x=(d+E)*b/(a-d-E)
t2y=w

#condicion inicial
x0 = 1.1
y0 = 1.5    
tiempo_max = 100



# Graficar
plt.figure(figsize=(10, 8)) 
plt.streamplot(X1, Y1, U1, V1, color='red', linewidth=0.6, density=1.2)
plt.streamplot(X2, Y2, U2, V2, color='blue', linewidth=0.6, density=1.2)
plt.plot([ax, t1x], [w, w], color='black', linestyle='--', linewidth=2)
plt.plot([t1x, t2x], [w, w], color='black', linestyle='-', linewidth=2)
plt.plot([t2x, bx], [w, w], color='black', linestyle='--', linewidth=2, label=f'Frontera y = {w}')
plt.scatter([t1x, t2x], [t1y, t2y], color='green', zorder=3)
plt.text(t1x, t1y, 'T1', color='green', fontsize=10, ha='center', va='bottom')
plt.text(t2x, t2y, 'T2', color='green', fontsize=10, ha='center', va='bottom')
plt.scatter(x0, y0, color='black', zorder=3)
plt.text(x0, y0, 'CI', color='black', fontsize=10, ha='right', va='bottom')
plt.xlim(ax, bx)    
plt.ylim(ay, by)
plt.xlabel('Prey Population')
plt.ylabel('Predator Population')   
plt.title('Prey-Predator Model with Filippov Dynamics')
plt.legend()
plt.grid()
plt.show()