import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir la función del SEDO como una función en Python
def SEDO(V, t, beta, gamma): #V es el vector de variables dependientes
    S, I = V
    dSdt = -beta*S*I
    dIdt = beta*S*I - gamma*I
    return [dSdt, dIdt]

# Parámetros del SEDO
#a = -5


#Condiciones iniciales
S0 = 0.99
I0 = 0.1

# Vector de tiempo
t = np.linspace(0, 60, 10000)

# Condiciones iniciales como vector
V0 = [S0, I0]
beta = 0.2 # Tasa de infección
gamma = 0.1 # Tasa de recuperación

# Resolver el SEDO con odeint
solution = odeint(SEDO, V0, t, args=(beta,gamma))

# Extraer las soluciones de solution
X, Y = solution.T
print(solution.T)

# Gráfica de las soluciones
plt.subplot(1,2,1)
plt.plot(t,X, label='Solución S(t)')
plt.plot(t,Y, label='Solución I(t)')
plt.xlabel('tiempo t')
plt.ylabel('Soluciones')
plt.title('Soluciones del SEDO')
plt.legend()
plt.grid()

plt.subplot(1,2,2)
plt.plot(X,Y)
plt.xlabel('S(t)')
plt.ylabel('T(t)')
plt.title('Plano de fase')
plt.grid()

plt.show()