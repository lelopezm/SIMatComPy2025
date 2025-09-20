import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Matrices del sistema
A1 = np.array([[2, -1],
               [1,  4]])   # Inestable

A2 = np.array([[-1, -2],
               [ 1, -1]])  # Estable

# Alternancia senoidal
h = 1.0          # Umbral
tol = 0.01       # Tolerancia
T_total = 10     # Tiempo total
dt = 0.01        # Paso de tiempo
t = np.arange(0, T_total, dt)

# Inicialización
estado = 1       # 1: A1 activo, 2: A2 activo
ti = 0           # Tiempo del último cambio
fase = 0         # Fase del seno
estado_por_tiempo = []  # Lista para almacenar el estado usado en cada paso

# Generar la función senoidal que controla el cambio
senal_control = np.zeros_like(t)
for i in range(1, len(t)):
    if estado == 1:
        senal_control[i] = np.sin(t[i] - ti + fase)
        if senal_control[i] >= h - tol:
            estado = 2
            ti = t[i]
            fase = np.arcsin(h)
    else:
        senal_control[i] = -np.sin(t[i] - ti + fase) + 2*h
        if senal_control[i] <= h + tol:
            estado = 1
            ti = t[i]
            fase = np.arcsin(h)
    estado_por_tiempo.append(estado)

# Rellenar para tener misma longitud que t
estado_por_tiempo = [1] + estado_por_tiempo  # mismo largo que t

# Sistema dependiente de la señal senoidal
def sistema(v, t_index):
    x, y = v
    idx = int(t_index / dt)
    A = A1 if estado_por_tiempo[idx] == 1 else A2
    return A @ np.array([x, y])

# Resolver ODE con estado dinámico en el tiempo
v0 = [1, 1]
sol = np.zeros((len(t), 2))
sol[0] = v0

for i in range(1, len(t)):
    # Usar paso de Euler con la matriz actual (más simple que odeint para control puntual)
    A = A1 if estado_por_tiempo[i] == 1 else A2
    sol[i] = sol[i-1] + dt * (A @ sol[i-1])

x, y = sol[:, 0], sol[:, 1]

# Dibujar campos vectoriales
ax, bx = 0, 5
ay, by = 0, 6
w = 3  # Línea de umbral solo como referencia visual
h_grid = 0.5

X1, Y1 = np.meshgrid(np.arange(ax, bx + h_grid, h_grid), np.arange(ay, w + h_grid, h_grid))
U1 = A1[0, 0]*X1 + A1[0, 1]*Y1
V1 = A1[1, 0]*X1 + A1[1, 1]*Y1

X2, Y2 = np.meshgrid(np.arange(ax, bx + h_grid, h_grid), np.arange(w, by + h_grid, h_grid))
U2 = A2[0, 0]*X2 + A2[0, 1]*Y2
V2 = A2[1, 0]*X2 + A2[1, 1]*Y2

plt.figure(figsize=(10,6))
plt.streamplot(X1, Y1, U1, V1, color='red', linewidth=0.6, density=1.0)
plt.streamplot(X2, Y2, U2, V2, color='green', linewidth=0.6, density=1.0)

plt.plot(x, y, 'b', linewidth=2, label='Trayectoria')
plt.axhline(w, color='gray', linestyle='--', label='Referencia w')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Alternancia entre dos sistemas por señal senoidal')
plt.grid(True)
plt.legend()
plt.show()
