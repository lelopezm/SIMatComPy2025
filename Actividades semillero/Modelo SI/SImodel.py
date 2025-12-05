import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

#ventana
ax=0
bx=1 
ay=0
by=1

#umbral
w=0.3 # valor de ZETA

# parametros
R0 = 1.5
mu = 0.2    
theta = 0.15
u = 0.1  

# sistema 1 
def sistema1(t, V): #V es el vector de variables dependientes
    x, y = V #x=S y=I
    dxdt = f1_x(x, y)
    dydt = f1_y(x, y)
    return [dxdt, dydt]

# sistema 2
def sistema2(t, V): #V es el vector de variables dependientes
    x, y = V
    dxdt = f2_x(x, y)
    dydt = f2_y(x, y)
    return [dxdt, dydt]

def f1_x(x, y):
    return mu*(1-x) - (mu+theta)*R0*x*y

def f1_y(x, y):
    return (mu+theta)*y*(R0*x - 1)

def f2_x(x, y):
    return mu*(1-x) - (mu+theta)*R0*x*y

def f2_y(x, y):
    return (mu+theta)*y*(R0*x - 1) - u


# CÁLCULO DE ℓ (producto de proyecciones en ∇H)
def calcular_L(x, w):
    """
    Calcula ℓ = ⟨∇H, f⁽¹⁾⟩ * ⟨∇H, f⁽²⁾⟩
    Con H = y - w, entonces ∇H = (0, 1)
    Por lo tanto: ℓ = f1_y(x,w) * f2_y(x,w)
    """
    componente_f1y = f1_y(x, w)
    componente_f2y = f2_y(x, w)
    l = componente_f1y * componente_f2y
    return l, componente_f1y, componente_f2y

# EQUILIBRIO DE f1
xe1 = 1/R0
ye1 = mu*(R0 - 1)/((mu + theta)*R0)

# EQUILIBRIO DE f2
a=mu*R0
b=-(mu+mu*R0-u*R0)
c=mu
discriminante=b**2-4*a*c
if discriminante >= 0:
    xe2_1 = (-b + np.sqrt(discriminante)) / (2*a)
    xe2_2 = (-b - np.sqrt(discriminante)) / (2*a)
    ye2_1 = (mu*(1 - xe2_1)-u)/(mu + theta)
    ye2_2 = (mu*(1 - xe2_2)-u)/(mu + theta)
# PUNTOS TANGENTES
# T₁: donde f1_y(x,w) = 0
t1x = 1/R0
t1y = w

# T₂: donde f2_y(x,w) = 0
t2x = (1/R0)*(1 + u/((mu + theta)*w))
t2y = w

print(f"Puntos tangentes calculados:")
print(f"  T₁ = ({t1x:.6f}, {t1y:.6f})")
print(f"  T₂ = ({t2x:.6f}, {t2y:.6f})")

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

"""Esos eventos sirven exactamente para detectar cuándo la integración 1D sobre
la frontera (y = w) alcanza los puntos tangentes T1 o T2."""
# Evento para la integración 1D en la frontera: detectar llegada a T1 o T2
def evento_llegada_T1(t, x, w):
    # - x: vector estado de la integración 1D (aquí x[0] es la coordenada x)
    return x[0] - t1x # evento: llega a t1x cuando x[0] - t1x == 0
evento_llegada_T1.terminal = True # cuando la función retorna 0 y terminal=True, el integrador se detiene en ese instante
evento_llegada_T1.direction = 0
"""direction = 0 -> detectar ceros en cualquier dirección (subida o bajada)
# (si fuera 1 o -1 se detectaría solo cruces con esa dirección)"""

def evento_llegada_T2(t, x, w):
    # - x: vector estado de la integración 1D (aquí x[0] es la coordenada x)
    return x[0] - t2x # evento: llega a t2x cuando x[0] - t2x == 0
evento_llegada_T2.terminal = True
evento_llegada_T2.direction = 0

# Simulación del sistema 1
def simula_sistema1(x0, y0, tiempo_max):
    sol = solve_ivp(sistema1, [0, tiempo_max], [x0, y0], events=evento_yw_arriba, max_step=0.01)
    return sol

# Simulación del sistema 2
def simula_sistema2(x0, y0, tiempo_max):
    sol = solve_ivp(sistema2, [0, tiempo_max], [x0, y0], events=evento_yw_abajo, max_step=0.01)
    return sol


 # ODE: dx/dt = f1_1(x)  (porque f1_1 == f2_1)
def dxdt_1d(t, x, w): #Define una función que calcula la derivada dx/dt requerida por solve_ivp de la funcion integra_deslizamiento.
    xx = x[0]  # x0: posición inicial en la coordenada x (escalar).
    return [f1_x(xx, w)] # <-- usar y = w en la frontera

# Integrador 1D para la dinámica de deslizamiento (x(t) mientras y = w)
def integra_deslizamiento(x0, tiempo_max, w_local=None):
    # usar w_local si se pasa, sino la global w
    w_arg = w_local if w_local is not None else w  # Elige el valor de w que se usará dentro de la integración
    """dxdt_1d: función que calcula dx/dt. Debe tener firma (t, x, w) para recibir el arg adicional.
    args=(w_arg,): argumentos extra que se pasan a dxdt_1d y a las funciones evento; aquí fija y = w_arg."""
    sol = solve_ivp(dxdt_1d, [0, tiempo_max], [x0],
                    args=(w_arg,),
                    events=[evento_llegada_T1, evento_llegada_T2],
                    max_step=0.01)
    return sol


    
# Campo vectorial 1
X = np.linspace(ax, bx, 20)
Y = np.linspace(ay, w, 20)
X1, Y1 = np.meshgrid(X, Y)
U1 = mu*(1-X1) - (mu+theta)*R0*X1*Y1
V1 = (mu+theta)*Y1*(R0*X1 - 1)
N1 = np.sqrt(U1**2 + V1**2)
N1 = np.where(N1 == 0, 1, N1)  # Evitar división por cero
U1, V1 = U1/N1, V1/N1  # Normalizar

# Campo vectorial 2
X = np.linspace(ax, bx, 20)
Y = np.linspace(w, by, 20)
X2, Y2 = np.meshgrid(X, Y)
U2 = mu*(1-X2) - (mu+theta)*R0*X2*Y2
V2 = (mu+theta)*Y2*(R0*X2 - 1) - u
N2 = np.sqrt(U2**2 + V2**2)
N2 = np.where(N2 == 0, 1, N2)  # Evitar división por cero
U2, V2 = U2/N2, V2/N2  # Normalizar 

# Parámetro de simulación
tiempo_max = 500

# ----------- SIMULACIÓN CON CONMUTACIÓN MÚLTIPLE -------------
puntos_iniciales = [
    #condicion inicial
    (0.55, 0.4),
    (0.3, 0.4),
    (0.9, 0.1)   # puedes añadir más
]
plt.figure(figsize=(10, 8))
plt.streamplot(X1, Y1, U1, V1, color='red', linewidth=0.6, density=1.2)
plt.streamplot(X2, Y2, U2, V2, color='blue', linewidth=0.6, density=1.2)

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
            # Esta condicion para que al graficar muchas trayectorias no aparezca "Sistema 1"
            # repetido varias veces en la leyenda. El label solo aparece una vez.
            label_traj = f'Sistema 1' if idx == 0 and switch_count == 0 else "" 
        elif y_actual > w:
            print(f"    -> Usando Sistema 2 (y > {w})")
            sol = simula_sistema2(x_actual, y_actual, tiempo_max)
            color_traj = 'darkblue'
            label_traj = f'Sistema 2' if idx == 0 and y_actual >= w and switch_count <= 1 else ""        
        else:
            # Estamos exactamente en la frontera
            print("→ Exactamente en la frontera y = w")
            l, f1y, f2y = calcular_L(x_actual, w)
            print(f"  ℓ = {l:.6e}, f1_y = {f1y:.6e}, f2_y = {f2y:.6e}")

            
        # Verificar que la simulación produjo resultados
        if len(sol.y[0]) <= 1:
            print(f"    -> Simulación no produjo puntos suficientes. Terminando.")
            break
            
        # Graficar segmento de trayectoria
        plt.plot(sol.y[0], sol.y[1], color=color_traj, linewidth=2.5, 
                alpha=0.8, label=label_traj)
        print(f"    -> Graficado segmento con {len(sol.y[0])} puntos")
        
        # Verificar si hubo evento de conmutación (cruce de y = w)
        event_ocurrido = False
        for ev in sol.t_events:
            if len(ev) > 0:
                event_ocurrido = True
                break

        if event_ocurrido:
            # [-1] toma el último punto calculado (si terminal=True y el evento paró la integración, ese último punto corresponde al cruce).
            x_cruce = sol.y[0][-1]
            y_cruce = sol.y[1][-1]
            print(f"  Cruce detectado en ({x_cruce:.6f}, {y_cruce:.6f})")
            x_actual = x_cruce
            y_actual = y_cruce

        # calcular l en ese punto (evaluado en y = w)   
            l, f1y,f2y = calcular_L(x_actual, w)
            print(f"    f1_2(y=w) = {f1y:.6e}, f2_2(y=w) = {f2y:.6e}, l = {l:.6e}")

            plt.scatter(x_actual, y_actual, color='purple', s=80, zorder=7)
            plt.text(x_actual+0.01, y_actual+0.02, f'S{switch_count+1}', color='purple')

            # Caso 1: l > 0 -> crossing (dejar que cruce)
            if l > 0:
                print("    l > 0  -> Cruce. Continuamos en la otra región.")
                # desplazar mínimamente para que integrador continúe en la región destino
                eps = 1e-6
                if y_actual >= w:
                    y_actual = y_actual + eps
                else:
                    y_actual = y_actual - eps
                

            # Caso 2: L < 0 -> sliding (deslizamiento)
            elif l < 0:
                print("    l < 0  -> Zona de deslizamiento. Integro dinámica sobre y = w (1D).")
                # Integrar dx/dt = f1_1(x) con y = w
                sol_slide = integra_deslizamiento(x_actual, tiempo_max=50)
                xs = sol_slide.y[0]
                ts = sol_slide.t

                # graficar la trayectoria sobre la frontera
                plt.plot(xs, [w]*len(xs), color='orange', linewidth=2.5, linestyle='-', alpha=0.9, label='Deslizamiento' if switch_count==0 else "")

                # imprimir detalles
                print(f"    Deslizamiento integrado con {len(xs)} puntos, tiempo final {ts[-1]:.3f}")

                # determinar punto final del deslizamiento
                if sol_slide.t_events[0].size > 0:
                    x_fin = sol_slide.y_events[0][0][0]
                    print(f"    Se alcanzó T1 en x = {x_fin:.6f}")
                elif sol_slide.t_events[1].size > 0:
                    x_fin = sol_slide.y_events[1][0][0]
                    print(f"    Se alcanzó T2 en x = {x_fin:.6f}")
                else:
                    x_fin = xs[-1]
                    print("    Deslizamiento terminó por tiempo/condición (no alcanzó T1/T2)")

                """x_fin es la coordenada x final del deslizamiento sobre la frontera y = w — es el
                punto donde termina la integración 1D (por haber alcanzado T1 o T2, o por terminar por tiempo).
                Después se usa x_fin para continuar la simulación (x_actual = x_fin, y_actual = w)."""
                # actualizar para continuar integración (salida de la frontera)
                x_actual = x_fin
                y_actual = w

                # después de deslizar, debemos comprobar si en x_fin hay tangencia exacta:
               
                l_fin,f1y_fin,f2y_fin = calcular_L(x_fin, w)
                print(f"    En x_fin: f1_2 = {f1y_fin:.6e}, f2_2 = {f2y_fin:.6e}, L_fin = {l_fin:.6e}")

                # si uno de ellos es (casi) cero marcamos tangente
                tol = 1e-8
                if abs(f1y_fin) < tol:
                    print("    Punto tangente T1 alcanzado.")
                    plt.scatter(x_fin, w, color='lime', s=100, edgecolor='k', zorder=9)
                if abs(f2y_fin) < tol:
                    print("    Punto tangente T2 alcanzado.")
                    plt.scatter(x_fin, w, color='lime', s=100, edgecolor='k', zorder=9)

                # Dar un pequeño empujón fuera de la frontera para que la siguiente integración no se quede pegada
                eps = 1e-6
                # decidir a que lado empujar: si f1_2(x_fin) > 0 => f1 apunta hacia arriba entonces empujamos hacia arriba
                if f1y_fin > 0:
                    y_actual = w + eps
                else:
                    y_actual = w - eps

            # Caso 3: l == 0 -> tangencia
                """En un punto tangente una de las proyecciones (f1_y o f2_y) es ~0. Se detecta cuál está más cerca de cero mediante |·| y se usa el signo de la otra para decidir a qué
                lado salir. El empujón evita que el integrador vuelva a
                quedarse exactamente en y=w y permite continuar la simulación en la región adecuada."""
            else:
                print("    l == 0  -> Punto tangente exacto.")
                plt.scatter(x_actual, w, color='yellow', s=120, edgecolor='k', zorder=9)
                # actualizar y dar una pequeña decisión (empujón) para evitar quedarse en la frontera
                eps = 1e-6
                # si f1y == 0 entonces T1, si f2y == 0 entonces T2
                if abs(f1y) < abs(f2y):
                    # asumimos tangencia f1
                    if f2y > 0:
                        y_actual = w + eps
                    else:
                        y_actual = w - eps
                else:
                    if f1y > 0:
                        y_actual = w + eps
                    else:
                        y_actual = w - eps
                
        else:
            # no hay cruce: terminar
            print(f"  {system_name} terminó sin cruzar frontera. Punto final ({sol.y[0][-1]:.6f}, {sol.y[1][-1]:.6f})")
            break

        # si salimos de ventana, terminamos
        if x_actual < ax or x_actual > bx or y_actual < ay or y_actual > by:
            print("  Trayectoria salió de los límites. Terminando.")
            break
        
        
        
        

print(f"\n=== SIMULACIÓN COMPLETADA ===")

# Graficar
#plt.figure(figsize=(10, 8)) 
plt.streamplot(X1, Y1, U1, V1, color='red', linewidth=0.6, density=1.2)
plt.streamplot(X2, Y2, U2, V2, color='blue', linewidth=0.6, density=1.2)
plt.plot([ax, t1x], [w, w], color='black', linestyle='--', linewidth=2)
plt.plot([t1x, t2x], [w, w], color='black', linestyle='-', linewidth=2)
plt.plot([t2x, bx], [w, w], color='black', linestyle='--', linewidth=2, label=f'Frontera y = {w}')
plt.plot([0,1], [1,0], color='black', linestyle='-', linewidth=2)
plt.scatter([t1x, t2x], [t1y, t2y], color='green', s=140, zorder=3)
plt.plot([xe1], [ye1], marker='o', color='cyan', markersize=10, label='Equilibrio f1', zorder=4)
if discriminante >= 0:
    plt.plot([xe2_1, xe2_2], [ye2_1, ye2_2], marker='o', color='magenta', markersize=10, label='Equilibrio f2', zorder=4)
plt.text(t1x, t1y, 'T1', color='green', fontsize=10, ha='center', va='bottom')
plt.text(t2x, t2y, 'T2', color='green', fontsize=10, ha='center', va='bottom')
plt.scatter(x0, y0, color='black', zorder=3)
plt.text(x0, y0, 'CI', color='black', fontsize=10, ha='right', va='bottom')
plt.xlim(ax, bx)    
plt.ylim(ay, by)
plt.xlabel('Prey Population')
plt.ylabel('Predator Population')   
plt.title('Prey-Predator Model with Filippov Dynamics')
plt.legend(loc='lower left', bbox_to_anchor=(1.02, 0.02), borderaxespad=0, frameon=True)
plt.grid()
# Intentar maximizar la ventana de la figura
mgr = plt.get_current_fig_manager()
try:
    # TkAgg (común en Windows)
    mgr.window.state('zoomed')
except Exception:
    try:
        # Qt backends (PyQt5 / PySide)
        mgr.window.showMaximized()
    except Exception:
        try:
            # wx backend
            mgr.frame.Maximize(True)
        except Exception:
            # si no se pudo maximizar, no hacer nada
            pass
plt.show()