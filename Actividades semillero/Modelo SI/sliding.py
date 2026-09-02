# sliding.py
# ============================================================================
# Este archivo implementa la integracion de la dinamica de deslizamiento.
#
# Cuando la clasificacion de Filippov indica SLIDING (l < 0), la trayectoria
# queda atrapada sobre la frontera y = w. En este caso, la dinamica se
# reduce a una ODE unidimensional:
#
#   dx/dt = f1_x(x, w) = mu*(1-x) - (mu+theta)*R0*x*w
#
# Esta ODE se integra hasta que la trayectoria alcanza un punto tangente
# (T1 o T2), donde puede escapar de la frontera.
#
# Referencia:
#   Piiroinen, P.T. & Kuznetsov, Y.A. (2008). An event-driven method
#   to simulate Filippov systems. ACM TOMS, 34(3), Art. 13, Sec. 3.
# ============================================================================

from dataclasses import dataclass  # Para crear la estructura de resultado

from scipy.integrate import solve_ivp  # Integrador de ODEs de SciPy

from dynamics import sliding_field_1d     # Campo vectorial reducido 1D
from equilibrium import TangentPoints     # Puntos tangentes T1, T2
from parameters import FilippovParams, SolverParams  # Parametros


# ----------------------------------------------------------------------------
# SlidingResult: Estructura que almacena el resultado de la integracion 1D
# ----------------------------------------------------------------------------
@dataclass
class SlidingResult:
    x_traj: list[float]   # Trayectoria x(t) sobre la frontera
    t_traj: list[float]   # Tiempos correspondientes a cada punto
    x_fin: float          # Coordenada x final (donde termina el sliding)
    reached_T1: bool      # True si se alcanzo el punto tangente T1
    reached_T2: bool      # True si se alcanzo el punto tangente T2


# ----------------------------------------------------------------------------
# integrate_sliding: Integrador de la dinamica de deslizamiento
# ----------------------------------------------------------------------------
# Funcionamiento:
#   1. Define la ODE 1D: dx/dt = f1_x(x, w) con y fijado en w
#   2. Define eventos de terminacion: llegada a T1 o T2
#   3. Integra con solve_ivp hasta que se alcance un evento o tiempo max
#   4. Determina el punto final del deslizamiento
#
# FIX: En el codigo original, se usaba sol.t_events[0] tanto para T1
#      como para T2. Ahora se usa correctamente:
#        - t_events[0] para T1
#        - t_events[1] para T2
#
# Parametros:
#   x0: Coordenada x inicial sobre la frontera
#   w: Valor de la frontera y = w
#   tangent: Objeto TangentPoints con las coordenadas de T1 y T2
#   fp: Parametros del modelo Filippov
#   sp: Parametros del integrador
#
# Retorna: Objeto SlidingResult con la trayectoria y el punto final
def integrate_sliding(x0: float, w: float, tangent: TangentPoints,
                      fp: FilippovParams, sp: SolverParams) -> SlidingResult:
    """Integra dx/dt sobre y = w hasta alcanzar T1, T2 o tiempo maximo."""

    # Extrae las coordenadas x de T1 y T2 (ignora las y con _)
    # tangent.T1 es una tupla (t1x, t1y), entonces [0] es t1x
    t1x, _ = tangent.T1  # t1x = 1/R0
    t2x, _ = tangent.T2  # t2x = (1/R0)*(1 + u/((mu+theta)*w))

    # --- ODE 1D para la dinamica de deslizamiento ---
    # state es un array de un elemento: [x]
    # state[0] es la coordenada x actual
    # Retorna [dxdt] como lista de un elemento (solve_ivp requiere array)
    def ode_1d(t, state):
        return [sliding_field_1d(state[0], w, fp)]

    # --- Evento de terminacion: llegada a T1 ---
    # El evento se activa cuando state[0] - t1x == 0, es decir,
    # cuando x alcanza la coordenada x de T1.
    # direction = 0: detectar el cero en cualquier direccion
    #              (subiendo o bajando)
    def event_T1(t, state, *_):
        return state[0] - t1x  # Retorna 0 cuando x == t1x
    event_T1.terminal = True   # Detener la integracion cuando se activa
    event_T1.direction = 0     # Detectar cruces en cualquier direccion

    # --- Evento de terminacion: llegada a T2 ---
    # Mismo principio que event_T1 pero para T2
    def event_T2(t, state, *_):
        return state[0] - t2x  # Retorna 0 cuando x == t2x
    event_T2.terminal = True   # Detener la integracion
    event_T2.direction = 0     # Cualquier direccion

    # --- Integracion numerica ---
    # solve_ivp resuelve: dy/dt = fun(t, y)
    #   fun = ode_1d (la ODE 1D)
    #   t_span = [0, tiempo_maximo]
    #   y0 = [x0] (condicion inicial, array de un elemento)
    #   events = [event_T1, event_T2] (detener al alcanzar T1 o T2)
    #   max_step = paso maximo para no saltarse la frontera
    sol = solve_ivp(
        ode_1d,                    # Funcion ODE
        [0, sp.tiempo_max],        # Intervalo de tiempo
        [x0],                      # Condicion inicial [x0]
        events=[event_T1, event_T2],  # Eventos de terminacion
        max_step=sp.max_step,      # Paso maximo de integracion
        rtol=sp.rtol,              # Tolerancia relativa
        atol=sp.atol,              # Tolerancia absoluta
    )

    # --- Determinar que evento se activo ---
    # sol.t_events es una lista de arrays. Cada array contiene los
    # tiempos en que se activo cada evento.
    # Si el array esta vacio (size == 0), ese evento no se activo.

    # FIX: t_events[0] corresponde a event_T1 (primer evento registrado)
    reached_T1 = sol.t_events[0].size > 0  # True si se llego a T1

    # FIX: t_events[1] corresponde a event_T2 (segundo evento registrado)
    # En el codigo original se usaba t_events[0] para ambos (bug)
    reached_T2 = sol.t_events[1].size > 0  # True si se llego a T2

    # --- Determinar el punto final del deslizamiento ---
    if reached_T1:
        # y_events[0] contiene el estado en el evento T1
        # [0][0] es el primer (y unico) evento, [0] es el primer elemento del estado
        x_fin = sol.y_events[0][0][0]  # x final = coordenada x en T1
    elif reached_T2:
        # FIX: Ahora se usa y_events[1] para T2 (antes era [0])
        x_fin = sol.y_events[1][0][0]  # x final = coordenada x en T2
    else:
        # Ni T1 ni T2 se alcanzaron: el sliding termino por tiempo maximo
        x_fin = sol.y[0][-1]  # Ultimo valor de x en la trayectoria

    # Retorna el resultado completo
    return SlidingResult(
        x_traj=sol.y[0].tolist(),  # Convierte array numpy a lista Python
        t_traj=sol.t.tolist(),     # Convierte array numpy a lista Python
        x_fin=x_fin,
        reached_T1=reached_T1,
        reached_T2=reached_T2,
    )
