"""Prevalencia de un brote de gripe en un internado para varones,
    Reino Unido [Centro de Vigilancia de Enfermedades Transmisibles (1978)]. 
    Tamaño total de la población, N = 763, número inicial de susceptibles,
    S0 = 762, y número inicial de infectivos,
    I0 = 1. Estimaciones de los parámetros con un error 
    estándar: βˆ = 1,6682 ± 0,0294 (días-1), γ= 0,4417 ± 0,0177 (días-1).
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd

# MODELO SIR - Brote de gripe 1978 (UK)
def modelo_sir(y, t, beta, gamma):
    S, I, R = y
    N = S + I + R
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

# CARGAR DATOS OBSERVADOS desde CSV
df = pd.read_csv(r"D:\Universidad\Universidad\Semestre_5\Semillero2025\codigosPy\SIMatComPy2025\Actividades semillero\Dylber\influenza_datos_observados.csv")
dias = df["dia"].values
casos_obs = df["Casos"].values

# PARÁMETROS DEL MODELO (estimados)
beta_M = 1.6682
gamma_M = 0.4417
beta_m = 0.0294
gamma_m = 0.0177

# CONDICIONES INICIALES
S0, I0, R0 = 762, 1, 0
y0 = [S0, I0, R0]
N = 763

# TIEMPO DE SIMULACIÓN
t0 = 0
tf = max(dias)
n = 250
T = np.linspace(t0, tf, n)

# SOLUCIÓN POR ODEINT
sol = odeint(modelo_sir, y0, T, args=(beta_M, gamma_M))
S, I, R = sol.T


# INTERPOLAR valores de I(t) del modelo en los días del CSV
I_model = np.interp(dias, T, I)


# GRAFICAR resultados
plt.figure(figsize=(10, 6))
plt.plot(T, I, '#12CFE1', label='Modelo I(t)')
plt.scatter(dias, casos_obs, color='black', zorder=5, label='Datos Observados')
plt.xlabel('t (días)')
plt.ylabel('Infectados')
plt.title('Comparación Modelo SIR vs Datos Observados')
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# RESULTADOS NUMÉRICOS por día
print("Día\tObservado\tModelo\t\tError")
for d, obs, mod in zip(dias, casos_obs, I_model):
    err = abs(obs - mod)
    print(f"{d}\t{obs:.1f}\t\t{mod:.4f}\t\t{err:.4f}")

# EJEMPLO DE ERROR EN t = 14
I_aprox = I_model[-1]
I_obs = casos_obs[-1]
h = (tf - t0) / n
error_final = abs(I_aprox - I_obs)

print("\nResumen:")
print("Valor observado t=%d: %.1f" % (dias[-1], I_obs))
print("Valor aproximado I(t=%d) = %.6f" % (dias[-1], I_aprox))
print("Error estimado = %.12f con tamaño de paso h = %.4f" % (error_final, h))
