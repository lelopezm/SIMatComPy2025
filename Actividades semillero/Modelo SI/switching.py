# switching.py
# ============================================================================
# Este archivo implementa el analisis de conmutacion de Filippov.
#
# En un sistema Filippov, la frontera H(x,y) = 0 divide el plano en
# regiones con dinamicas distintas. En cada punto de la frontera, se
# evaluan las proyecciones de ambos campos vectoriales sobre el gradiente
# de H para clasificar el comportamiento:
#
#   l = <nablaH, f(1)> * <nablaH, f(2)>
#
# Donde nablaH es el gradiente de la funcion de conmutacion H.
#
# Clasificacion (Piiroinen & Kuznetsov, 2008):
#   - l > 0: CROSSING - ambos campos apuntan al mismo lado de la frontera
#   - l < 0: SLIDING  - los campos apuntan en direcciones opuestas
#   - l = 0: TANGENCY - un campo es tangente a la frontera
#
# Referencia:
#   Piiroinen, P.T. & Kuznetsov, Y.A. (2008). An event-driven method
#   to simulate Filippov systems with accurate computing of sliding
#   motions. ACM TOMS, 34(3), Art. 13.
# ============================================================================

from dataclasses import dataclass  # Para crear la estructura de resultado
from enum import Enum              # Para crear enumeraciones tipadas

from dynamics import vector_field_1, vector_field_2  # Campos vectoriales
from parameters import FilippovParams                # Parametros del modelo


# ----------------------------------------------------------------------------
# SwitchType: Enumeracion de los tres tipos de comportamiento en la frontera
# ----------------------------------------------------------------------------
# Enum es una clase base para crear enumeraciones. Cada miembro tiene
# un nombre (CROSSING) y un valor ("crossing"). Esto permite comparaciones
# tipo-safe en vez de usar strings sueltos.
class SwitchType(Enum):
    CROSSING = "crossing"  # La trayectoria cruza la frontera sin quedar atrapada
    SLIDING = "sliding"    # La trayectoria queda atrapada sobre la frontera
    TANGENCY = "tangency"  # Un campo vectorial es tangente a la frontera


# ----------------------------------------------------------------------------
# SwitchAnalysis: Estructura que almacena el resultado del analisis
# ----------------------------------------------------------------------------
# dataclass crea automaticamente __init__, __repr__ y __eq__.
# Al no tener frozen=True, las instancias son mutables (aunque aqui
# no las modificamos despues de crearlas).
@dataclass
class SwitchAnalysis:
    L: float            # Producto de proyecciones: l = f1_y * f2_y
    f1_y: float         # Componente y del Sistema 1 evaluada en la frontera
    f2_y: float         # Componente y del Sistema 2 evaluada en la frontera
    switch_type: SwitchType  # Clasificacion: CROSSING, SLIDING o TANGENCY


# ----------------------------------------------------------------------------
# compute_switching_analysis: Funcion principal de clasificacion
# ----------------------------------------------------------------------------
# Evalua ambos campos vectoriales sobre la frontera y = w y calcula el
# producto de sus proyecciones sobre nablaH = (0, 1).
#
# Con H(x,y) = y - w:
#   nablaH = (dH/dx, dH/dy) = (0, 1)
#
# Por lo tanto:
#   <nablaH, f(1)> = 0*f1_x + 1*f1_y = f1_y
#   <nablaH, f(2)> = 0*f2_x + 1*f2_y = f2_y
#   l = f1_y * f2_y
#
# Geometricamente:
#   - f1_y > 0 y f2_y > 0: ambos apuntan hacia arriba (l > 0, crossing)
#   - f1_y > 0 y f2_y < 0: f1 arriba, f2 abajo (l < 0, sliding)
#   - f1_y = 0: f1 es tangente a la frontera (punto T1)
#   - f2_y = 0: f2 es tangente a la frontera (punto T2)
#
# Parametros:
#   x: Coordenada x del punto en la frontera
#   w: Valor de la frontera (y = w)
#   p: Parametros del modelo
#
# Retorna: Objeto SwitchAnalysis con l, las proyecciones y la clasificacion
def compute_switching_analysis(x: float, w: float, p: FilippovParams) -> SwitchAnalysis:
    """Calcula l = <nablaH, f(1)> * <nablaH, f(2)> y clasifica el punto.

    Con H = y - w, nablaH = (0, 1), entonces:
        l = f1_y(x, w) * f2_y(x, w)

    Referencia: Piiroinen & Kuznetsov (2008), Ecs. (8)-(10).
    """

    # Evalua vector_field_1 en (x, w) y toma la componente y (indice [1])
    # vector_field_1 retorna [dxdt, dydt], entonces [1] es dydt = f1_y
    f1_y = vector_field_1(x, w, p)[1]

    # Evalua vector_field_2 en (x, w) y toma la componente y (indice [1])
    # vector_field_2 retorna [dxdt, dydt], entonces [1] es dydt = f2_y
    f2_y = vector_field_2(x, w, p)[1]

    # Producto de las proyecciones: este es el criterio de Filippov
    L = f1_y * f2_y

    # Clasificacion basada en el signo de l
    if L > 0:
        # Ambos campos apuntan al mismo lado de la frontera
        stype = SwitchType.CROSSING
    elif L < 0:
        # Los campos apuntan en direcciones opuestas -> sliding
        stype = SwitchType.SLIDING
    else:
        # Al menos uno de los campos es tangente a la frontera
        stype = SwitchType.TANGENCY

    # Retorna el resultado completo del analisis
    return SwitchAnalysis(L=L, f1_y=f1_y, f2_y=f2_y, switch_type=stype)
