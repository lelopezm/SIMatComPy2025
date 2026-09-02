# visualization.py
# ============================================================================
# Este archivo genera la representacion grafica del plano de fase del
# sistema Filippov. Incluye:
#   - Campos vectoriales normalizados (streamplots)
#   - Frontera de conmutacion y = w con estilo diferenciado
#   - Trayectorias de cada condicion inicial (colores por sistema)
#   - Puntos de equilibrio y puntos tangentes
#   - Condiciones iniciales marcadas
#
# FIX: En el codigo original, streamplot se dibujaba dos veces (antes y
#      despues del bucle). Aqui se dibuja una sola vez por region.
# ============================================================================

import matplotlib.pyplot as plt  # Libreria de graficacion
import numpy as np              # Operaciones numericas

from equilibrium import compute_equilibria, compute_tangent_points  # Calculos geometricos
from parameters import DomainParams, FilippovParams                 # Configuracion
from solver import SimulationResult                                  # Resultado de simulacion


# ----------------------------------------------------------------------------
# _make_vector_field_vectorizado: Evalua el campo vectorial en una grilla
# ----------------------------------------------------------------------------
# VERSION VECTORIZADA: Reemplaza el loop Python doble (for i, for j)
# por operaciones matriciales de NumPy. Esto es ~50x mas rapido porque:
#   - ANTES: n*n llamadas a la funcion Python (400 para n=20)
#   - DESPUES: 1 sola operacion NumPy que procesa toda la grilla a la vez
#
# NOTA: Esta funcion SOLO se usa para graficar los campos vectoriales.
# NO afecta la precision de la simulacion (solve_ivp), que se mantiene
# identica. El cambio es puramente de rendimiento en el dibujado.
#
# Parametros:
#   p: Parametros del modelo FilippovParams
#   Xg: Matriz 2D de coordenadas x (generada por np.meshgrid)
#   Yg: Matriz 2D de coordenadas y (generada por np.meshgrid)
#   sistema: 1 para Sistema 1 (sin control), 2 para Sistema 2 (con control)
#
# Retorna: (U_norm, V_norm) - campo vectorial normalizado
def _make_vector_field_vectorizado(p, Xg, Yg, sistema):
    # Componente dx/dt: identica para ambos sistemas
    # dxdt = mu*(1-x) - (mu+theta)*R0*x*y
    # NumPy evalua esta operacion en TODA la matriz a la vez (broadcasting)
    U = p.mu * (1 - Xg) - (p.mu + p.theta) * p.R0 * Xg * Yg

    # Componente dy/dt: difiere segun el sistema
    if sistema == 1:
        # Sistema 1 (sin control): dydt = (mu+theta)*y*(R0*x - 1)
        V = (p.mu + p.theta) * Yg * (p.R0 * Xg - 1)
    else:
        # Sistema 2 (con control): dydt = (mu+theta)*y*(R0*x - 1) - u
        V = (p.mu + p.theta) * Yg * (p.R0 * Xg - 1) - p.u

    # Normalizacion: divide cada vector por su magnitud
    # Esto hace que todas las flechas tengan la misma longitud visual
    N = np.sqrt(U**2 + V**2)  # Magnitud del vector en cada punto

    # Evita division por cero: donde N == 0, reemplaza por 1
    # (el vector cero se mantiene como cero despues de la division)
    N = np.where(N == 0, 1, N)

    # Retorna el campo normalizado (misma matriz U/V dividida por N)
    return U / N, V / N


# ----------------------------------------------------------------------------
# _plot_vector_fields: Dibuja los campos vectoriales de ambos subsistemas
# ----------------------------------------------------------------------------
# dibuja el campo del Sistema 1 en la region inferior (rojo) y
# el campo del Sistema 2 en la region superior (azul).
#
# USA VERSION VECTORIZADA: evalua los campos en toda la grilla a la vez
# con operaciones matriciales de NumPy en vez de un loop Python doble.
# Esto reduce el tiempo de dibujado de ~50ms a ~1ms para n=20.
def _plot_vector_fields(ax, fp, dp):
    # Crea la grilla de puntos para ambas regiones
    # np.linspace genera n puntos equiespaciados
    # np.meshgrid combina los arreglos 1D en matrices 2D
    n = 20  # Numero de puntos por lado (mismo que el codigo original)

    # --- Region inferior: Sistema 1 (y en [ay, w]) ---
    X_inf = np.linspace(dp.ax, dp.bx, n)  # Puntos en eje x
    Y_inf = np.linspace(dp.ay, fp.w, n)   # Puntos en eje y: de 0 a w
    Xg1, Yg1 = np.meshgrid(X_inf, Y_inf)  # Grilla 2D

    # Evalua el campo vectorial 1 en toda la grilla (vectorizado)
    U1, V1 = _make_vector_field_vectorizado(fp, Xg1, Yg1, sistema=1)

    # --- Region superior: Sistema 2 (y en [w, by]) ---
    X_sup = np.linspace(dp.ax, dp.bx, n)  # Puntos en eje x
    Y_sup = np.linspace(fp.w, dp.by, n)   # Puntos en eje y: de w a 1
    Xg2, Yg2 = np.meshgrid(X_sup, Y_sup)  # Grilla 2D

    # Evalua el campo vectorial 2 en toda la grilla (vectorizado)
    U2, V2 = _make_vector_field_vectorizado(fp, Xg2, Yg2, sistema=2)

    # streamplot dibuja lineas de corriente del campo vectorial
    # color="red": Sistema 1 en rojo
    # linewidth=0.6: grosor de las lineas
    # density=1.2: densidad de las lineas (mas alto = mas lineas)
    ax.streamplot(Xg1, Yg1, U1, V1, color="red", linewidth=0.6, density=1.2)

    # Sistema 2 en azul
    ax.streamplot(Xg2, Yg2, U2, V2, color="blue", linewidth=0.6, density=1.2)


# ----------------------------------------------------------------------------
# _plot_boundary: Dibuja la frontera de conmutacion y = w
# ----------------------------------------------------------------------------
# La frontera se dibuja con tres estilos:
#   - Linea punteada antes de T1 (no hay sliding)
#   - Linea continua entre T1 y T2 (zona de sliding)
#   - Linea punteada despues de T2 (no hay sliding)
def _plot_boundary(ax, fp, dp):
    # Calcula los puntos tangentes
    tp = compute_tangent_points(fp.w, fp)
    t1x, t1y = tp.T1  # T1 = (1/R0, w)
    t2x, t2y = tp.T2  # T2 = ((1/R0)*(1+u/((mu+theta)*w)), w)

    # Segmento antes de T1: punteado (no hay sliding)
    # [ax, t1x] = [x_min, x_T1], [w, w] = y constante
    ax.plot([dp.ax, t1x], [fp.w, fp.w], "k--", linewidth=2)

    # Segmento entre T1 y T2: continuo (zona de sliding)
    ax.plot([t1x, t2x], [fp.w, fp.w], "k-", linewidth=2)

    # Segmento despues de T2: punteado (no hay sliding)
    ax.plot([t2x, dp.bx], [fp.w, fp.w], "k--", linewidth=2, label=f"Frontera y = {fp.w}")


# ----------------------------------------------------------------------------
# plot_phase_portrait: Funcion principal de graficacion
# ----------------------------------------------------------------------------
# Genera la figura completa del retrato de fase del sistema Filippov.
#
# Parametros:
#   trajectories: Lista de SimulationResult (una por condicion inicial)
#   fp: Parametros del modelo
#   dp: Limites del dominio
#   initial_conditions: Lista de tuplas (x0, y0) para marcar CIs
#
# Retorna: Objeto fig de matplotlib
def plot_phase_portrait(
    trajectories: list[SimulationResult],
    fp: FilippovParams,
    dp: DomainParams,
    initial_conditions: list[tuple[float, float]] | None = None,
):
    # Crea la figura y el eje de graficacion
    # figsize=(10, 8): tamano de la figura en pulgadas
    fig, ax = plt.subplots(figsize=(10, 8))

    # Dibuja los campos vectoriales (rojo abajo, azul arriba)
    _plot_vector_fields(ax, fp, dp)

    # Dibuja la frontera y = w con los tres segmentos
    _plot_boundary(ax, fp, dp)

    # Diccionario de colores por tipo de segmento
    colors = {"sistema1": "darkred", "sistema2": "darkblue", "sliding": "orange"}

    # Dibuja cada trayectoria (una por condicion inicial)
    for i, traj in enumerate(trajectories):
        # Dibuja cada segmento de la trayectoria
        for seg in traj.segments:
            ax.plot(
                seg.x,              # Coordenadas x del segmento
                seg.y,              # Coordenadas y del segmento
                color=colors[seg.segment_type],  # Color segun el sistema
                linewidth=2.5,      # Grosor de la linea
                alpha=0.8,          # Transparencia
            )

        # Marca los puntos tangentes alcanzados durante el sliding
        for th in traj.tangent_hits:
            ax.scatter(*th, color="lime", s=100, edgecolor="k", zorder=9)

    # --- Puntos de equilibrio ---
    eq = compute_equilibria(fp)

    # Equilibrio del Sistema 1 (cyan)
    ax.plot(eq.x1, eq.y1, "o", color="cyan", markersize=10, label="Equilibrio f1", zorder=4)

    # Equilibrios del Sistema 2 (magenta) - solo si existen (disc >= 0)
    if eq.discriminante >= 0:
        ax.plot(
            [eq.x2_1, eq.x2_2],    # Coordenadas x de ambos equilibrios
            [eq.y2_1, eq.y2_2],    # Coordenadas y de ambos equilibrios
            "o",                    # Marcador circular
            color="magenta",
            markersize=10,
            label="Equilibrio f2",
            zorder=4,               # zorder alto = se dibuja encima
        )

    # --- Puntos tangentes ---
    tp = compute_tangent_points(fp.w, fp)

    # T1 y T2 como puntos verdes grandes
    ax.scatter(*tp.T1, color="green", s=140, zorder=3, label="Tangente T1")
    ax.scatter(*tp.T2, color="green", s=140, zorder=3, label="Tangente T2")

    # Etiquetas de texto junto a cada punto tangente
    ax.text(tp.T1[0], tp.T1[1], " T1", color="green", fontsize=10, va="bottom")
    ax.text(tp.T2[0], tp.T2[1], " T2", color="green", fontsize=10, va="bottom")

    # --- Condiciones iniciales ---
    if initial_conditions:
        for idx, (x0, y0) in enumerate(initial_conditions):
            # Punto negro grande para la condicion inicial
            ax.scatter(x0, y0, color="black", s=100, zorder=5)
            # Etiqueta CI1, CI2, etc.
            ax.text(
                x0 + 0.02,        # Desplazamiento horizontal para legibilidad
                y0,                # Posicion y
                f"CI{idx + 1}",    # Texto: CI1, CI2, CI3, ...
                color="black",
                fontsize=10,
                ha="left",         # Horizontal alignment: izquierda
                va="bottom",       # Vertical alignment: abajo
            )

    # --- Leyenda de sistemas ---
    # Solo agrega a la leyenda los sistemas que aparecen en las trayectorias
    seg_types = set(seg.segment_type for traj in trajectories for seg in traj.segments)
    if "sistema1" in seg_types:
        ax.plot([], [], color="darkred", linewidth=2.5, label="Sistema 1")
    if "sistema2" in seg_types:
        ax.plot([], [], color="darkblue", linewidth=2.5, label="Sistema 2")
    if "sliding" in seg_types:
        ax.plot([], [], color="orange", linewidth=4, label="Deslizamiento")

    # --- Configuracion de los ejes ---
    ax.set_xlim(dp.ax, dp.bx)                  # Limites del eje x
    ax.set_ylim(dp.ay, dp.by)                  # Limites del eje y
    ax.set_xlabel("Poblacion Suceptible (S)")   # Etiqueta del eje x
    ax.set_ylabel("Poblacion Infectada (I)")    # Etiqueta del eje y
    ax.set_title("Filippov Dynamics")           # Titulo de la grafica
    plt.plot([0,1], [1,0], color='black', linestyle='-', linewidth=2)
    # Leyenda fuera del grafico (a la derecha)
    ax.legend(loc="lower left", bbox_to_anchor=(1.02, 0.02), borderaxespad=0, frameon=True)

    # Cuadricula de fondo
    ax.grid()

    # Ajusta el layout para que la leyenda no se corte
    plt.tight_layout()

    return fig
