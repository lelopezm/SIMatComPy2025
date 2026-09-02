# main.py
# ============================================================================
# Este es el punto de entrada del programa. Orquesta todo el pipeline:
#   1. Crea los parametros del modelo
#   2. Ejecuta la simulacion para cada condicion inicial
#   3. Genera la grafica del retrato de fase
#   4. Muestra la ventana maximizada
#
# Para ejecutar: python main.py
# ============================================================================

import matplotlib.pyplot as plt  # Para mostrar la grafica

from parameters import DomainParams, FilippovParams, SolverParams  # Configuracion
from solver import simulate                   # Funcion de simulacion
from visualization import plot_phase_portrait  # Funcion de graficacion


def main():
    # ================================================================
    # PASO 1: Crear instancias de configuracion con valores por defecto
    # ================================================================
    # Cada dataclass se instancia sin argumentos usando los valores
    # definidos en parameters.py. frozen=True impide modificarlos.
    fp = FilippovParams()  # Parametros del modelo (R0, mu, theta, u, w)
    dp = DomainParams()    # Limites del dominio [0,1] x [0,1]
    sp = SolverParams()    # Parametros del integrador

    # ================================================================
    # PASO 2: Definir las condiciones iniciales
    # ================================================================
    # Lista de tuplas (S0, I0). Cada una genera una trayectoria
    # independiente en el plano de fase.
    initial_conditions = [
        (0.55, 0.4),   # CI1: arriba de la frontera (y > w), en sistema 2
        (0.3, 0.4),    # CI2: arriba de la frontera, cerca de T1
        (0.1, 0.5),    # CI3: arriba de la frontera, lejos de T1
        (0.95, 0.28),  # CI4: debajo de la frontera (y < w), pasa por T1
    ]

    # ================================================================
    # PASO 3: Ejecutar la simulacion para cada condicion inicial
    # ================================================================
    trajectories = []  # Lista para almacenar los resultados
    for x0, y0 in initial_conditions:
        # simulate() ejecuta el bucle event-driven de Filippov
        # y retorna un SimulationResult con todos los segmentos
        result = simulate(x0, y0, fp, dp, sp)
        trajectories.append(result)

    # ================================================================
    # PASO 4: Generar la grafica del retrato de fase
    # ================================================================
    # plot_phase_portrait toma todas las trayectorias y genera
    # la figura completa con campos vectoriales, frontera, etc.
    fig = plot_phase_portrait(trajectories, fp, dp, initial_conditions)

    # ================================================================
    # PASO 5: Maximizar la ventana de la grafica
    # ================================================================
    # plt.get_current_fig_manager() obtiene el gestor de la ventana
    # La llamada a window.state("zoomed") depende del backend de matplotlib.
    # Se intentan varios backends en orden de compatibilidad:
    mgr = plt.get_current_fig_manager()
    try:
        mgr.window.state("zoomed")       # TkAgg (comun en Windows)
    except Exception:
        try:
            mgr.window.showMaximized()    # Qt backends (PyQt5/PySide)
        except Exception:
            try:
                mgr.frame.Maximize(True)  # wx backend
            except Exception:
                pass                      # Si ninguno funciona, no hacer nada

    # ================================================================
    # PASO 6: Mostrar la grafica
    # ================================================================
    # plt.show() bloquea la ejecucion hasta que el usuario cierre la ventana
    plt.show()


# ================================================================
# Punto de entrada: solo ejecuta main() si se corre directamente
# ================================================================
# __name__ es "__main__" cuando el archivo se ejecuta directamente
# (python main.py). Si se importa como modulo, __name__ es "main"
# y no se ejecuta automaticamente.
if __name__ == "__main__":
    main()
