import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#ventana
ax=-15
bx=20
ay=0
by=6

#umbral
w=3

# sistema 1 (inestable) ROJO matriz A
a1 = 2
b1 = -1
c1 = 1
d1 = 4

# sistema 2 (estable) VERDE matriz B
a2 = 1
b2 = 2
c2 = -1
d2 = 1

""" a2 = -1
b2 = -2
c2 = 1
d2 = -1 """

def sistema1(t, V):
    x, y = V
    dxdt = a1 * x + b1 * y
    dydt = c1 * x + d1 * y
    return [dxdt, dydt]

def sistema2(t, V):
    x, y = V
    dxdt = a2 * x + b2 * y
    dydt = c2 * x + d2 * y
    return [dxdt, dydt]


def evento_y3_arriba(t, V):
    return V[1] - w
evento_y3_arriba.terminal = True
evento_y3_arriba.direction = 1  # Solo cuando cruza hacia arriba

def evento_y3_abajo(t, V):
    return V[1] - w
evento_y3_abajo.terminal = True
evento_y3_abajo.direction = -1  # Solo cuando cruza hacia abajo


def simula_sistema1(x0, y0, tiempo_max):
    sol = solve_ivp(sistema1, [0, tiempo_max], [x0, y0], events=evento_y3_arriba, max_step=0.01)
    return sol

def simula_sistema2(x0, y0, tiempo_max):
    sol = solve_ivp(sistema2, [0, tiempo_max], [x0, y0], events=evento_y3_abajo, max_step=0.01)
    return sol

# Campo vectorial 1
h = 0.5
X1, Y1 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(ay, w + h, h))
dXdt1 = a1 * X1 + b1 * Y1
dYdt1 = c1 * X1 + d1 * Y1

# Campo vectorial 2
X2, Y2 = np.meshgrid(np.arange(ax, bx + h, h), np.arange(w, by + h, h))
dXdt2 = a2 * X2 + b2 * Y2
dYdt2 = c2 * X2 + d2 * Y2

plt.figure(figsize=(12, 8))
plt.streamplot(X1, Y1, dXdt1, dYdt1, color='red', linewidth=0.6, density=1.2)
plt.streamplot(X2, Y2, dXdt2, dYdt2, color='green', linewidth=0.6, density=1.2)
plt.axhline(y=w, color='black', linestyle='--', linewidth=2, label=f'Frontera y = {w}')

# Puedes probar varios puntos iniciales aquí
puntos_iniciales = [
    (0.5, 0.5)
    
]

for i, (x0, y0) in enumerate(puntos_iniciales):
    print(f"\n--- Trayectoria desde ({x0}, {y0}) ---")
    # Simula sistema 1 hasta cruzar y=3
    sol1 = simula_sistema1(x0, y0, tiempo_max=10.5)
    plt.plot(sol1.y[0], sol1.y[1], color='blue', linewidth=2.5, alpha=0.8, label=f'Sistema 1' if i == 0 else "")
    plt.plot(x0, y0, 'o', color='blue', markersize=8, label=f'Inicio {i+1}' if i < 4 else '')

    # Si cruza la frontera, simula sistema 2 desde ese punto
    if sol1.t_events[0].size > 0:
        x_conmutacion, y_conmutacion = sol1.y_events[0][0]
        plt.plot(x_conmutacion, y_conmutacion, 'o', color='purple', markersize=7, label=f'Conmutación {i+1}' if i == 0 else "")
        plt.text(x_conmutacion + 0.1, y_conmutacion + 0.05,f'({x_conmutacion:.2f}, {y_conmutacion:.2f})',fontsize=9, color='black')
        sol2 = simula_sistema2(x_conmutacion, y_conmutacion, tiempo_max=10.5)
        plt.plot(sol2.y[0], sol2.y[1], color='purple', linewidth=2.5, alpha=0.8, label=f'Sistema 2' if i == 0 else "")

plt.xlim(ax, bx)
plt.ylim(ay, by)
plt.grid(True, alpha=0.3)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sistema de Filippov: Campos Vectoriales con Switching en y = 3')
plt.legend(loc='upper right')
plt.text(0.1, 5.7, 'Sistema 2 (Verde): Región y > 3', fontsize=10, color='green', weight='bold')
plt.text(0.1, 0.3, 'Sistema 1 (Rojo): Región y < 3', fontsize=10, color='red', weight='bold')
plt.tight_layout()
plt.show()