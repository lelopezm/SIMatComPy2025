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

# parametros
a = 0.3556
b = 0.33    
d = 0.0444
E = 0.2067  

# sistema 1 
def sistema1(t, V): #V es el vector de variables dependientes
    x, y = V
    dxdt = x*(1-x) - (a*x*y)/(b+x)
    dydt = a*x*y/(b+x) - d*y
    return [dxdt, dydt]

# sistema 2
def sistema2(t, V): #V es el vector de variables dependientes
    x, y = V
    dxdt = x*(1-x) - (a*x*y)/(b+x)
    dydt = a*x*y/(b+x) - d*y - E*y
    return [dxdt, dydt] 


# función de eventos Sistema 1
def evento_yw_arriba(t, V):
    return V[1] - w
evento_yw_arriba.terminal = True
evento_yw_arriba.direction = 1  # Solo cuando cruza hacia arriba

# función de eventos Sistema 2
def evento_yw_abajo(t, V):
    return V[1] - w
evento_yw_abajo.terminal = True
evento_yw_abajo.direction = -1  # Solo cuando cruza hacia abajo

# Simulación del sistema 1
def simula_sistema1(x0, y0, tiempo_max):
    sol = solve_ivp(sistema1, [0, tiempo_max], [x0, y0], events=evento_yw_arriba, max_step=0.01)
    return sol

# Simulación del sistema 2
def simula_sistema2(x0, y0, tiempo_max):
    sol = solve_ivp(sistema2, [0, tiempo_max], [x0, y0], events=evento_yw_abajo, max_step=0.01)
    return sol

# Campo vectorial 1
X = np.linspace(ax, bx, 20)
Y = np.linspace(ay, w, 20)
X1, Y1 = np.meshgrid(X, Y)
U1 = X1*(1-X1) - (a*X1*Y1)/(b+X1)
V1 = (a*X1*Y1)/(b+X1) - d*Y1
N1 = np.sqrt(U1**2 + V1**2)
N1 = np.where(N1 == 0, 1, N1)  # Evitar división por cero
U1, V1 = U1/N1, V1/N1  # Normalizar

# Campo vectorial 2
X = np.linspace(ax, bx, 20)
Y = np.linspace(w, by, 20)
X2, Y2 = np.meshgrid(X, Y)
U2 = X2*(1-X2) - (a*X2*Y2)/(b+X2)
V2 = (a*X2*Y2)/(b+X2) - d*Y2 - E*Y2
N2 = np.sqrt(U2**2 + V2**2)
N2 = np.where(N2 == 0, 1, N2)  # Evitar división por cero
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

# SIMULACIÓN CON CONMUTACIÓN MÚLTIPLE
puntos_iniciales = [
   (x0, y0)
]

for idx, (x0, y0) in enumerate(puntos_iniciales):
    print(f"\n--- Trayectoria {idx+1} desde ({x0:.2f}, {y0:.2f}) ---")
    
    x_actual, y_actual = x0, y0
    tiempo_max = 50
    max_switches = 8  # Máximo número de cambios
    
    # Marcar punto inicial
    plt.scatter(x0, y0, color='black', s=100, zorder=5)
    plt.text(x0+0.02, y0, f'CI{idx+1}', color='black', fontsize=10, ha='left', va='bottom')
    
    # BUCLE DE CONMUTACIÓN
    for switch_count in range(max_switches):
        print(f"  Switch {switch_count+1}: Posición ({x_actual:.4f}, {y_actual:.4f})")
        
        # Determinar qué sistema usar en este caso usamos el sistema 1
        if y_actual < w:
            # Usar sistema 1 (región inferior)
            print(f"    -> Usando Sistema 1 (y < {w})")
            sol = simula_sistema1(x_actual, y_actual, tiempo_max)
            color_traj = 'darkred'
            system_name = 'Sistema 1'
            label_traj = f'Sistema 1' if idx == 0 and switch_count == 0 else ""
        else:
            # Usar sistema 2 (región superior)
            print(f"    -> Usando Sistema 2 (y > {w})")
            sol = simula_sistema2(x_actual, y_actual, tiempo_max)
            color_traj = 'darkblue'
            system_name = 'Sistema 2'
            label_traj = f'Sistema 2' if idx == 0 and y_actual >= w and switch_count <= 2 else ""
            
            
        # Verificar que la simulación produjo resultados
        if len(sol.y[0]) <= 1:
            print(f"    -> Simulación no produjo puntos suficientes. Terminando.")
            break
            
        # Graficar segmento de trayectoria
        plt.plot(sol.y[0], sol.y[1], color=color_traj, linewidth=2.5, 
                alpha=0.8, label=label_traj)
        print(f"    -> Graficado segmento con {len(sol.y[0])} puntos")
        
        # Verificar si hubo evento de conmutación
        if sol.t_events[0].size > 0: #verifica si hubo un cruce de frontera
            # Hubo switching
            x_cambio, y_cambio = sol.y_events[0][0] # toma el primer evento encontrado
            print(f"    -> ¡SWITCHING detectado en ({x_cambio:.4f}, {y_cambio:.4f})!")

            # Marcar punto de conmutación
            plt.scatter(x_cambio, y_cambio, color='purple', s=80, zorder=4, alpha=0.9)
            plt.text(x_cambio+0.01, y_cambio+0.02, f'S{switch_count+1}', 
                    color='purple', fontsize=8, ha='left', va='bottom')
            
            # Actualizar posición para siguiente iteración
            x_actual, y_actual = x_cambio, y_cambio

            """ Le da una “decisión clara” al integrador sobre en qué región continuar. Evita que el modelo se quede indeciso o atrapado justo en y=w. """

            # Pequeño desplazamiento para evitar quedarse pegado en la frontera
            eps = 1e-5
            if y_actual >= w:
                y_actual += eps  # Mover ligeramente hacia arriba
                print(f"    -> Desplazado hacia arriba: y = {y_actual:.6f}")
            else:
                y_actual -= eps  # Mover ligeramente hacia abajo  
                print(f"    -> Desplazado hacia abajo: y = {y_actual:.6f}")

        else:
            # No hubo más switching
            print(f"    -> No más switching detectado. {system_name} terminó sin cruzar frontera.")
            final_x, final_y = sol.y[0][-1], sol.y[1][-1]
            print(f"    -> Punto final: ({final_x:.4f}, {final_y:.4f})")
            break
            
        # Verificar si salió de los límites
        if x_actual < ax or x_actual > bx or y_actual < ay or y_actual > by:
            print(f"    -> Trayectoria salió de los límites. Terminando.")
            break

print(f"\n=== SIMULACIÓN COMPLETADA ===")

# Graficar
#plt.figure(figsize=(10, 8)) 
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