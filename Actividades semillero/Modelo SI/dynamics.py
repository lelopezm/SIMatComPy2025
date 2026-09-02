# dynamics.py
# ============================================================================
# Este archivo define los campos vectoriales (sistemas de ODE) del modelo
# Filippov. Contiene las ecuaciones diferenciales que gobiernan la dinamica
# del sistema en cada region del plano de fase.
#
# El modelo es un sistema SI (Suceptible-Infectado) con dos regimenes:
#   - Sistema 1 (y < w): sin control activo
#   - Sistema 2 (y > w): con control u aplicado
#
# Referencia teorica:
#   Filippov, A.F. (1988). Differential Equations with Discontinuous
#   Righthand Sides. Kluwer Academic Publishers.
# ============================================================================

from parameters import FilippovParams  # Importa la dataclass con los parametros del modelo


# ----------------------------------------------------------------------------
# vector_field_1: Sistema 1 (region inferior, y < w)
# ----------------------------------------------------------------------------
# Ecuaciones del modelo SI sin control:
#   dS/dt = mu*(1 - S) - (mu + theta)*R0*S*I
#   dI/dt = (mu + theta)*I*(R0*S - 1)
#
# Donde:
#   - mu*(1 - S): nacimiento de nuevos suceptibles (tasa de reclutamiento)
#   - (mu + theta)*R0*S*I: nuevos infectados (ley de mass action)
#   - (mu + theta)*I*(R0*S - 1): crecimiento/decrecimiento de infectados
#
# Parametros:
#   x: Poblacion suceptible S (escalar float)
#   y: Poblacion infectada I (escalar float)
#   p: Objeto FilippovParams con los parametros del modelo
#
# Retorna: Lista [dxdt, dydt] con las derivadas temporales
def vector_field_1(x: float, y: float, p: FilippovParams) -> list[float]:
    """Sistema 1: region inferior (y < w), sin control."""

    # dS/dt: tasa de cambio de suceptibles
    # mu*(1-x) = reclutamiento natural de suceptibles
    # (mu+theta)*R0*x*y = nuevos infectados por contacto (force of infection)
    dxdt = p.mu * (1 - x) - (p.mu + p.theta) * p.R0 * x * y

    # dI/dt: tasa de cambio de infectados
    # (mu+theta)*y = mortalidad total de infectados (natural + enfermedad)
    # R0*x - 1 = crecimiento neto: si R0*S > 1, la infeccion crece
    dydt = (p.mu + p.theta) * y * (p.R0 * x - 1)

    return [dxdt, dydt]  # Retorna las dos derivadas como lista


# ----------------------------------------------------------------------------
# vector_field_2: Sistema 2 (region superior, y > w)
# ----------------------------------------------------------------------------
# Mismo modelo SI pero con un termino de control -u en la ecuacion de I.
# El control reduce la prevalencia de la enfermedad cuando I > w.
#
# Ecuaciones:
#   dS/dt = mu*(1 - S) - (mu + theta)*R0*S*I    (igual que Sistema 1)
#   dI/dt = (mu + theta)*I*(R0*S - 1) - u        (diferencia: -u)
#
# Nota: La ecuacion de S es IDENTICA en ambos sistemas. Solo la ecuacion
# de I difiere por el termino -u. Esto es clave para la dinamica de
# deslizamiento sobre la frontera.
def vector_field_2(x: float, y: float, p: FilippovParams) -> list[float]:
    """Sistema 2: region superior (y > w), con control u."""

    # dS/dt: IDENTICO al Sistema 1 (no hay control sobre suceptibles)
    dxdt = p.mu * (1 - x) - (p.mu + p.theta) * p.R0 * x * y

    # dI/dt: igual que Sistema 1 pero con -u (el control)
    # u representa la tasa a la que los infectados son removidos
    # por intervencion (vacunacion, tratamiento, aislamiento)
    dydt = (p.mu + p.theta) * y * (p.R0 * x - 1) - p.u

    return [dxdt, dydt]


# ----------------------------------------------------------------------------
# sliding_field_1d: Dinamica reducida sobre la frontera y = w
# ----------------------------------------------------------------------------
# Cuando la trayectoria queda "atrapada" sobre la frontera y = w (sliding),
# la dinamica se reduce a una ODE unidimensional en la coordenada x.
#
# Como f1_x == f2_x (las ecuaciones de S son identicas), la dinamica
# sobre la frontera es simplemente:
#   dx/dt = mu*(1 - x) - (mu + theta)*R0*x*w
#
# Aqui y = w (constante), por lo que la ODE depende solo de x.
#
# Esta funcion es usada por sliding.py para integrar la trayectoria
# sobre la frontera hasta alcanzar un punto tangente (T1 o T2).
def sliding_field_1d(x: float, w: float, p: FilippovParams) -> float:
    """Dinamica reducida sobre la frontera y = w.
    La componente x es identica en ambos sistemas (f1_x == f2_x)."""

    # Evalua f1_x(x, w) con y fijado en w
    return p.mu * (1 - x) - (p.mu + p.theta) * p.R0 * x * w
