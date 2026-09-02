# equilibrium.py
# ============================================================================
# Este archivo calcula los puntos de equilibrio de ambos subsistemas y los
# puntos tangentes sobre la frontera de conmutacion.
#
# Puntos de equilibrio: donde f(x,y) = 0 (el sistema no cambia).
#   - Para f1: se resuelve dS/dt = 0 y dI/dt = 0 simultaneamente.
#   - Para f2: se resuelve dS/dt = 0 y dI/dt - u = 0 simultaneamente.
#
# Puntos tangentes: donde un campo vectorial es tangente a la frontera y = w.
#   - T1: f1_y(x, w) = 0 (el Sistema 1 es tangente)
#   - T2: f2_y(x, w) = 0 (el Sistema 2 es tangente)
#
# Estos puntos son criticos porque delimitan las zonas de sliding.
# ============================================================================

from dataclasses import dataclass  # Para crear estructuras de datos

import numpy as np  # Para operaciones matematicas (sqrt, nan)

from parameters import FilippovParams  # Parametros del modelo


# ----------------------------------------------------------------------------
# Equilibria: Almacena los puntos de equilibrio de ambos subsistemas
# ----------------------------------------------------------------------------
# x1, y1: Equilibrio del Sistema 1 (endemico)
# x2_1, y2_1: Primer equilibrio del Sistema 2 (raiz positiva de la cuadratica)
# x2_2, y2_2: Segundo equilibrio del Sistema 2 (raiz negativa)
# discriminante: Discriminante de la ecuacion cuadratica de f2.
#     Si disc < 0, no existen equilibrios reales para f2.
@dataclass
class Equilibria:
    x1: float       # Coordenada x del equilibrio de f1 (S*)
    y1: float       # Coordenada y del equilibrio de f1 (I*)
    x2_1: float     # Coordenada x del primer equilibrio de f2
    y2_1: float     # Coordenada y del primer equilibrio de f2
    x2_2: float     # Coordenada x del segundo equilibrio de f2
    y2_2: float     # Coordenada y del segundo equilibrio de f2
    discriminante: float  # Discriminante de la ecuacion cuadratica


# ----------------------------------------------------------------------------
# TangentPoints: Almacena los puntos tangentes T1 y T2
# ----------------------------------------------------------------------------
# Cada punto tangente es una tupla (x, y) donde y = w.
@dataclass
class TangentPoints:
    T1: tuple[float, float]  # Punto tangente del Sistema 1: (1/R0, w)
    T2: tuple[float, float]  # Punto tangente del Sistema 2: ((1/R0)*(1+u/((mu+theta)*w)), w)


# ----------------------------------------------------------------------------
# compute_equilibria: Calcula los puntos de equilibrio
# ----------------------------------------------------------------------------
# Sistema 1: equilibrio endemico
#   dS/dt = mu*(1-S) - (mu+theta)*R0*S*I = 0
#   dI/dt = (mu+theta)*I*(R0*S - 1) = 0
#
#   De la segunda ecuacion: I = 0 (trivial) o S = 1/R0 (endemico)
#   Si S = 1/R0, de la primera: I = mu*(R0-1)/((mu+theta)*R0)
#
# Sistema 2: equilibrio con control
#   dS/dt = mu*(1-S) - (mu+theta)*R0*S*I = 0
#   dI/dt = (mu+theta)*I*(R0*S - 1) - u = 0
#
#   De la segunda: I = (mu*(1-S) - u) / (mu+theta)
#   Sustituyendo en la primera y simplificando, se obtiene una
#   ecuacion cuadratica en S: a*S^2 + b*S + c = 0
#
#   donde:
#     a = mu*R0
#     b = -(mu + mu*R0 - u*R0)
#     c = mu
#
# FIX: Si el discriminante es negativo, ahora se asigna NaN en vez de
#      dejar variables indefinidas (que causaria NameError).
def compute_equilibria(p: FilippovParams) -> Equilibria:
    """Calcula los puntos de equilibrio de ambos subsistemas.

    f1: equilibrio endemico (S*, I*) con S* = 1/R0.
    f2: resuelve mu*(1-x) - u = 0 como ecuacion cuadratica en x.
    """

    # --- Equilibrio del Sistema 1 ---
    # S* = 1/R0: punto donde la tasa de infeccion neta es cero
    x1 = 1 / p.R0

    # I* = mu*(R0 - 1) / ((mu + theta)*R0)
    # Si R0 = 1, I* = 0 (no hay enfermedad endemica)
    # Si R0 > 1, I* > 0 (equilibrio endemico estable)
    y1 = p.mu * (p.R0 - 1) / ((p.mu + p.theta) * p.R0)

    # --- Equilibrios del Sistema 2 ---
    # Coeficientes de la ecuacion cuadratica a*x^2 + b*x + c = 0
    a = p.mu * p.R0                                    # Coeficiente de x^2
    b = -(p.mu + p.mu * p.R0 - p.u * p.R0)            # Coeficiente de x
    c = p.mu                                           # Termino independiente

    # Discriminante de la formula general: b^2 - 4*a*c
    disc = b**2 - 4 * a * c

    if disc >= 0:
        # Si el discriminante es >= 0, existen dos equilibrios reales
        # Formula general de Bhaskara: x = (-b +/- sqrt(disc)) / (2*a)
        x2_1 = (-b + np.sqrt(disc)) / (2 * a)  # Raiz positiva
        x2_2 = (-b - np.sqrt(disc)) / (2 * a)  # Raiz negativa

        # Calcula I* para cada equilibrio usando la relacion lineal
        # I = (mu*(1-S) - u) / (mu + theta)
        y2_1 = (p.mu * (1 - x2_1) - p.u) / (p.mu + p.theta)
        y2_2 = (p.mu * (1 - x2_2) - p.u) / (p.mu + p.theta)
    else:
        # FIX: Si disc < 0, no hay equilibrios reales para f2.
        # Antes este caso dejaba las variables indefinidas (NameError).
        # Ahora se asigna NaN (Not a Number) para indicar "no existe".
        x2_1 = x2_2 = y2_1 = y2_2 = float("nan")

    # Retorna todos los equilibrios en un objeto Equilibria
    return Equilibria(x1, y1, x2_1, y2_1, x2_2, y2_2, disc)


# ----------------------------------------------------------------------------
# compute_tangent_points: Calcula los puntos tangentes T1 y T2
# ----------------------------------------------------------------------------
# Un punto tangente es donde un campo vectorial es tangente a la frontera.
#
# T1: f1_y(x, w) = 0
#   (mu+theta)*w*(R0*x - 1) = 0
#   Como w != 0 y (mu+theta) != 0:
#   R0*x - 1 = 0  =>  x = 1/R0
#   Entonces T1 = (1/R0, w)
#
# T2: f2_y(x, w) = 0
#   (mu+theta)*w*(R0*x - 1) - u = 0
#   R0*x - 1 = u / ((mu+theta)*w)
#   R0*x = 1 + u / ((mu+theta)*w)
#   x = (1/R0) * (1 + u / ((mu+theta)*w))
#   Entonces T2 = ((1/R0)*(1 + u/((mu+theta)*w)), w)
#
# Entre T1 y T2 ocurre el SLIDING: los campos apuntan en direcciones
# opuestas y la trayectoria queda atrapada sobre la frontera.
def compute_tangent_points(w: float, p: FilippovParams) -> TangentPoints:
    """Puntos donde cada campo vectorial es tangente a la frontera y = w.

    T1: f1_y(x, w) = 0  =>  x = 1/R0
    T2: f2_y(x, w) = 0  =>  x = (1/R0)*(1 + u/((mu+theta)*w))
    """

    # T1: coordenada x donde f1_y se anula
    t1x = 1 / p.R0

    # T2: coordenada x donde f2_y se anula
    # El termino u/((mu+theta)*w) desplaza T2 a la derecha de T1
    t2x = (1 / p.R0) * (1 + p.u / ((p.mu + p.theta) * w))

    # Retorna ambos puntos como tuplas (x, y) con y = w
    return TangentPoints(T1=(t1x, w), T2=(t2x, w))
