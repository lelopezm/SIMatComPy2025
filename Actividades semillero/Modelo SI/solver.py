# solver.py
# ============================================================================
# Este archivo contiene el bucle principal de simulacion del sistema Filippov.
# Implementa el algoritmo event-driven descrito en Piiroinen & Kuznetsov (2008).
#
# El algoritmo funciona como sigue:
#   1. Determinar en que region del plano de fase esta la trayectoria
#   2. Seleccionar el campo vectorial correspondiente
#   3. Integrar la ODE hasta que se detecte un evento de cruce de frontera
#   4. Clasificar el punto de cruce (crossing, sliding o tangency)
#   5. Actuar segun la clasificacion (cruzar, deslizar, o empujar)
#   6. Repetir hasta que la trayectoria salga del dominio o se agoten
#      los switches permitidos
#
# FIX: En el codigo original (linea 225), el else del caso "frontera
#      exacta" no tenia un break correcto, causando que sol no estuviera
#      definido cuando y_act == w. Ahora se maneja correctamente con
#      un continue despues de procesar la frontera.
#
# Referencia:
#   Piiroinen, P.T. & Kuznetsov, Y.A. (2008). An event-driven method
#   to simulate Filippov systems with accurate computing of sliding
#   motions. ACM TOMS, 34(3), Art. 13.
# ============================================================================

from dataclasses import dataclass, field  # Para estructuras de datos con campos por defecto

from scipy.integrate import solve_ivp  # Integrador de ODEs

from dynamics import vector_field_1, vector_field_2  # Campos vectoriales
from equilibrium import compute_tangent_points       # Puntos tangentes
from parameters import DomainParams, FilippovParams, SolverParams  # Configuracion
from sliding import integrate_sliding               # Integracion de sliding
from switching import SwitchType, compute_switching_analysis       # Analisis de conmutacion


# ----------------------------------------------------------------------------
# TrajectorySegment: Almacena un segmento continuo de trayectoria
# ----------------------------------------------------------------------------
# Cada vez que se integra un subsistema (o se desliza sobre la frontera),
# se guarda un segmento con sus coordenadas x, y y el tipo de segmento.
@dataclass
class TrajectorySegment:
    x: list[float]           # Coordenadas x del segmento
    y: list[float]           # Coordenadas y del segmento
    segment_type: str        # "sistema1", "sistema2" o "sliding"
    switch_point: tuple[float, float] | None = None  # Punto donde ocurrio el switch


# ----------------------------------------------------------------------------
# SimulationResult: Almacena el resultado completo de una simulacion
# ----------------------------------------------------------------------------
@dataclass
class SimulationResult:
    # Lista de segmentos de trayectoria (cada uno es un tramo continuo)
    segments: list[TrajectorySegment] = field(default_factory=list)
    # Puntos donde la trayectoria toca tangencialmente la frontera
    tangent_hits: list[tuple[float, float]] = field(default_factory=list)
    # Punto inicial de la condicion inicial
    initial_point: tuple[float, float] = (0.0, 0.0)
    # Punto final de la simulacion
    final_point: tuple[float, float] = (0.0, 0.0)
    # Numero total de commutaciones realizadas
    num_switches: int = 0


# ----------------------------------------------------------------------------
# simulate: Bucle event-driven principal
# ----------------------------------------------------------------------------
# Implementa el algoritmo de Piiroinen & Kuznetsov (2008), Algorithm 1.
#
# Parametros:
#   x0, y0: Condicion inicial (S0, I0)
#   fp: Parametros del modelo Filippov
#   dp: Limites del dominio
#   sp: Parametros del integrador
#
# Retorna: SimulationResult con todos los segmentos y metadatos
def simulate(x0: float, y0: float, fp: FilippovParams,
             dp: DomainParams, sp: SolverParams) -> SimulationResult:
    """Bucle event-driven de Filippov.

    Implementacion del algoritmo descrito en:
    Piiroinen & Kuznetsov (2008), "An event-driven method to simulate
    Filippov systems with accurate computing of sliding motions",
    ACM TOMS, 34(3), Art. 13.
    """

    # Pre-calcula los puntos tangentes (se usan como objetivos del sliding)
    tangent = compute_tangent_points(fp.w, fp)

    # Inicializa el resultado con el punto inicial
    result = SimulationResult(initial_point=(x0, y0))

    # Coordenadas actuales de la trayectoria
    x_act, y_act = x0, y0

    # --- BUCLE PRINCIPAL DE CONMUTACION ---
    # Cada iteracion integra un subsistema hasta detectar un evento
    for switch_count in range(sp.max_switches):

        # ================================================================
        # PASO 1: Determinar en que region estamos y seleccionar el ODE
        # ================================================================
        if y_act < fp.w:
            # Region inferior: Sistema 1 (sin control)
            # lambda crea una funcion anonima compatible con solve_ivp
            # La firma debe ser (t, V) donde V = [x, y]
            vf = lambda t, V: vector_field_1(V[0], V[1], fp)
            seg_type = "sistema1"

        elif y_act > fp.w:
            # Region superior: Sistema 2 (con control u)
            vf = lambda t, V: vector_field_2(V[0], V[1], fp)
            seg_type = "sistema2"

        else:
            # ============================================================
            # CASO ESPECIAL: Exactamente en la frontera y = w
            # ============================================================
            # FIX: En el codigo original, este caso imprimia un mensaje
            # pero no hacia break ni continue, causando que sol estuviera
            # indefinido en la linea 230. Ahora se procesa y se continua.

            # Clasificar el punto en la frontera
            analysis = compute_switching_analysis(x_act, fp.w, fp)

            if analysis.switch_type == SwitchType.SLIDING:
                # Estamos en la frontera y es zona de sliding
                # Integrar la dinamica reducida 1D
                slide = integrate_sliding(x_act, fp.w, tangent, fp, sp)

                # Guardar el segmento de deslizamiento
                result.segments.append(TrajectorySegment(
                    x=slide.x_traj,                              # Trayectoria x(t)
                    y=[fp.w] * len(slide.x_traj),               # y = w constante
                    segment_type="sliding",
                ))

                # Actualizar posicion al final del sliding
                x_act = slide.x_fin

                # Evaluar la frontera en el punto final para decidir a que lado salir
                l_after = compute_switching_analysis(x_act, fp.w, fp)
                if l_after.f1_y > 0:
                    y_act = fp.w + sp.eps  # f1 apunta hacia arriba -> salir arriba
                else:
                    y_act = fp.w - sp.eps  # f1 apunta hacia abajo -> salir abajo

            elif analysis.switch_type == SwitchType.TANGENCY:
                # Punto tangente exacto: decidir a que lado salir
                result.tangent_hits.append((x_act, fp.w))

                # Determinar cual campo esta mas cerca de ser tangente
                # y usar el signo del otro para decidir la direccion
                if abs(analysis.f1_y) < abs(analysis.f2_y):
                    # f1 es mas tangente -> usar el signo de f2
                    y_act = fp.w + sp.eps if analysis.f2_y > 0 else fp.w - sp.eps
                else:
                    # f2 es mas tangente -> usar el signo de f1
                    y_act = fp.w + sp.eps if analysis.f1_y > 0 else fp.w - sp.eps

            else:
                # Crossing en la frontera: empujar al otro lado
                if analysis.f1_y > 0:
                    y_act = fp.w + sp.eps  # Empujar hacia arriba
                else:
                    y_act = fp.w - sp.eps  # Empujar hacia abajo

            # IMPORTANTE: continue evita que el codigo llegue a los
            # pasos 2-8 que requieren que sol este definido
            continue

        # ================================================================
        # PASO 2: Definir evento de cruce de frontera
        # ================================================================
        # El evento detecta cuando y(t) cruza w.
        # make_crossing_event es una fabrica de funciones que genera
        # eventos con la direccion correcta segun el sistema actual.
        def make_crossing_event(direction):
            # Crea una funcion de evento para solve_ivp
            # La funcion retorna y(t) - w; se activa cuando es 0
            def event(t, V, w=fp.w):
                return V[1] - w  # Retorna 0 cuando y == w
            event.terminal = True     # Detener integracion al activarse
            event.direction = direction  # 1 = cruza hacia arriba, -1 = hacia abajo
            return event

        # Selecciona la direccion del evento:
        #   Si estamos abajo (y < w), buscamos cruce hacia arriba (direction=1)
        #   Si estamos arriba (y > w), buscamos cruce hacia abajo (direction=-1)
        crossing_event = make_crossing_event(
            direction=1 if y_act < fp.w else -1
        )

        # ================================================================
        # PASO 3: Integrar la ODE hasta el proximo evento
        # ================================================================
        sol = solve_ivp(
            vf,                           # Campo vectorial (Sistema 1 o 2)
            [0, sp.tiempo_max],           # Intervalo de tiempo [t0, tf]
            [x_act, y_act],              # Condicion inicial [x0, y0]
            events=crossing_event,        # Evento de cruce de frontera
            max_step=sp.max_step,         # Paso maximo (precision)
            rtol=sp.rtol,                # Tolerancia relativa
            atol=sp.atol,                # Tolerancia absoluta
        )

        # Verificar si la integracion fallo o no produjo puntos suficientes
        if sol.status < 0 or len(sol.y[0]) <= 1:
            break  # Integracion fallida o trivial

        # ================================================================
        # PASO 4: Guardar el segmento de trayectoria
        # ================================================================
        result.segments.append(TrajectorySegment(
            x=sol.y[0].tolist(),     # Coordenadas x (convierte numpy a lista)
            y=sol.y[1].tolist(),     # Coordenadas y (convierte numpy a lista)
            segment_type=seg_type,   # "sistema1" o "sistema2"
        ))

        # ================================================================
        # PASO 5: Detectar si hubo cruce de frontera
        # ================================================================
        # sol.t_events es una lista de arrays. Cada array contiene los
        # tiempos en que se activo cada evento.
        # any() retorna True si al menos un evento se activo
        event_ocurrido = any(len(ev) > 0 for ev in sol.t_events)

        if not event_ocurrido:
            # No hubo cruce: la trayectoria se quedo en la misma region
            break  # Terminar esta condicion inicial

        # ================================================================
        # PASO 6: Obtener el punto de cruce
        # ================================================================
        # El ultimo punto de la solucion es el punto de cruce
        # (porque el evento es terminal y detuvo la integracion)
        x_act = sol.y[0][-1]  # Ultimo valor de x
        y_act = sol.y[1][-1]  # Ultimo valor de y (deberia ser ~ w)

        # ================================================================
        # PASO 7: Clasificar el punto de cruce en la frontera
        # ================================================================
        analysis = compute_switching_analysis(x_act, fp.w, fp)

        if analysis.switch_type == SwitchType.CROSSING:
            # CRUZAR: ambos campos apuntan al mismo lado
            # Empujar la trayectoria al otro lado de la frontera
            # Si venia de sistema1 (abajo), empujar arriba
            # Si venia de sistema2 (arriba), empujar abajo
            y_act = fp.w + sp.eps if seg_type == "sistema1" else fp.w - sp.eps

        elif analysis.switch_type == SwitchType.SLIDING:
            # SLIDING: los campos apuntan en direcciones opuestas
            # Integrar la dinamica reducida sobre la frontera
            slide = integrate_sliding(x_act, fp.w, tangent, fp, sp)

            # Guardar el segmento de deslizamiento
            result.segments.append(TrajectorySegment(
                x=slide.x_traj,
                y=[fp.w] * len(slide.x_traj),
                segment_type="sliding",
            ))

            # Actualizar posicion al final del sliding
            x_act = slide.x_fin

            # Evaluar donde termino el sliding para decidir a que lado salir
            l_fin = compute_switching_analysis(x_act, fp.w, fp)
            if l_fin.f1_y > 0:
                y_act = fp.w + sp.eps  # Salir hacia arriba
            else:
                y_act = fp.w - sp.eps  # Salir hacia abajo

        elif analysis.switch_type == SwitchType.TANGENCY:
            # TANGENCIA: un campo es tangente a la frontera
            result.tangent_hits.append((x_act, fp.w))

            # Decidir a que lado salir basandose en el signo del otro campo
            if abs(analysis.f1_y) < abs(analysis.f2_y):
                y_act = fp.w + sp.eps if analysis.f2_y > 0 else fp.w - sp.eps
            else:
                y_act = fp.w + sp.eps if analysis.f1_y > 0 else fp.w - sp.eps

        # Incrementar contador de switches
        result.num_switches += 1

        # ================================================================
        # PASO 8: Verificar que la trayectoria este dentro del dominio
        # ================================================================
        if not (dp.ax <= x_act <= dp.bx and dp.ay <= y_act <= dp.by):
            break  # La trayectoria salio del plano de fase

    # Guardar el punto final de la simulacion
    result.final_point = (x_act, y_act)
    return result
