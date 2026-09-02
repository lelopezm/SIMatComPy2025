# parameters.py
# ============================================================================
# Este archivo define las configuraciones del sistema Filippov usando
# dataclasses de Python. Las dataclasses generan automaticamente __init__,
# __repr__ y __eq__ a partir de las anotaciones de tipo de los atributos.
# Usamos frozen=True para hacer las instancias inmutables (como constantes).
# ============================================================================

from dataclasses import dataclass  # Decorador que convierte una clase en una dataclass


# ----------------------------------------------------------------------------
# FilippovParams: Parametros biologicos/epidemiologicos del modelo SI
# ----------------------------------------------------------------------------
@dataclass(frozen=True)  # frozen=True impide modificar los atributos despues de crear la instancia
class FilippovParams:
    # R0: Numero basico de reproduccion. Indica cuantas personas infecta
    #     en promedio cada individuo infeccioso en una poblacion totalmente
    #     suceptible. Si R0 > 1, la enfermedad se propaga.
    R0: float = 1.5

    # mu: Tasa de nacimiento/muerte natural de la poblacion.
    #     En el modelo SI, los individuos nacen y mueren a esta tasa.
    mu: float = 0.2

    # theta: Tasa de muerte adicional por la enfermedad.
    #     Representa la virulencia del patogeno.
    theta: float = 0.15

    # u: Intensidad del control (vacunacion, tratamiento, cuarentena).
    #     Solo se aplica cuando la infeccion supera el umbral w.
    u: float = 0.1

    # w: Umbral de conmutacion (frontera de Filippov).
    #     Cuando I > w, se activa el control u.
    #     La frontera es la recta H(x,y) = y - w = 0.
    w: float = 0.3


# ----------------------------------------------------------------------------
# DomainParams: Limites del plano de fase [ax, bx] x [ay, by]
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class DomainParams:
    # ax, bx: Limites horizontales (poblacion suceptible S).
    #     En un modelo normalizado, S varia entre 0 y 1.
    ax: float = 0.0  # limite inferior de S
    bx: float = 1.0  # limite superior de S

    # ay, by: Limites verticales (poblacion infectada I).
    #     En un modelo normalizado, I varia entre 0 y 1.
    ay: float = 0.0  # limite inferior de I
    by: float = 1.0  # limite superior de I


# ----------------------------------------------------------------------------
# SolverParams: Parametros del integrador numerico
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class SolverParams:
    # tiempo_max: Tiempo maximo de integracion para cada segmento de trayectoria.
    #     Cada vez que se integra un subsistema, se integra hasta este tiempo
    #     o hasta que se detecte un evento de cruce de frontera.
    tiempo_max: float = 50.0

    # max_switches: Numero maximo de commutaciones (cambios de sistema)
    #     permitidos antes de detener la simulacion. Evita bucles infinitos.
    max_switches: int = 8

    # max_step: Paso maximo de integracion para solve_ivp.
    #     Un paso pequeno asegura que el integrador no "salte" la frontera
    #     sin detectar el evento de cruce.
    #     NOTA: Cambiar este valor altera los resultados de la simulacion.
    #     Se recomienda no modificarlo para mantener consistencia con el articulo.
    max_step: float = 0.01

    # rtol: Tolerancia relativa del integrador (solve_ivp).
    #     Controla la precision relativa de cada paso. Un valor mas pequeno
    #     significa mayor precision pero mas tiempo de ejecucion.
    #     Valor por defecto: 1e-3 (identico a solve_ivp, sin cambio en resultados).
    #     Para mayor precision: 1e-6. Para mas rapidez: 1e-2.
    rtol: float = 1e-3

    # atol: Tolerancia absoluta del integrador (solve_ivp).
    #     Controla la precision absoluta (independiente del tamano del estado).
    #     Valor por defecto: 1e-6 (identico a solve_ivp, sin cambio en resultados).
    atol: float = 1e-6

    # eps: Perturbacion infinitesimal para empujar la trayectoria fuera
    #     de la frontera despues de un cruce o sliding. Sin este empujon,
    #     el integrador quedaria exactamente en y = w y no sabria que
    #     subsistema usar en la siguiente iteracion.
    eps: float = 1e-6

    # tol: Tolerancia para detectar puntos tangentes.
    #     Si |f_y| < tol, se considera que el campo vectorial es tangente
    #     a la frontera (una de las proyecciones es practicamente cero).
    tol: float = 1e-8
