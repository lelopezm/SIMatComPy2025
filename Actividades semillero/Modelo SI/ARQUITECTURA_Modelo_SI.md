# Arquitectura del Modelo SI con Control de Filippov

## 1. Resumen del sistema que se modela

El código implementa un **modelo epidemiológico SI con control discontinuo (sistema de Filippov)**. La población se divide en **Suceptibles (S)** e **Infectados (I)**. El plano de fase está dividido por una **frontera de conmutación** recta:

```
H(x, y) = y - w = 0      con w = umbral (0.3)
```

- Si `I < w` → rige el **Sistema 1** (sin control).
- Si `I > w` → rige el **Sistema 2** (con control `u`).

El control `u` (vacunación/tratamiento/aislamiento) se activa únicamente cuando la infección supera el umbral `w`.

### Ecuaciones del modelo

**Sistema 1** (región inferior, `y < w`):

```
f1:  dx/dt = μ(1 - x) - (μ + θ)·R0·x·y
     dy/dt = (μ + θ)·y·(R0·x - 1)
```

**Sistema 2** (región superior, `y > w`):

```
f2:  dx/dt = μ(1 - x) - (μ + θ)·R0·x·y
     dy/dt = (μ + θ)·y·(R0·x - 1) - u
```

**Observación clave:** la ecuación de `S` (la componente `x`) es **idéntica en ambos sistemas**. Solo cambia la ecuación de `I` por el término constante `-u`. Esta propiedad permite reducir la dinámica de deslizamiento a una ODE unidimensional.

### Parámetros

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| `R0` | 1.5 | Número básico de reproducción |
| `μ` | 0.2 | Tasa de natalidad/mortalidad |
| `θ` | 0.15 | Tasa de muerte por enfermedad |
| `u` | 0.1 | Intensidad del control |
| `w` | 0.3 | Umbral de conmutación (frontera) |

---

## 2. Arquitectura de software: **Arquitectura Modular por Capas**

La arquitectura es una **arquitectura modular por capas de responsabilidad única** (Single Responsibility). El código está separado en **módulos independientes**, organizados en **capas** según su función, y orquestados por un único **punto de entrada** (`main.py`).

No es un monolito: cada archivo encapsula una tarea bien delimitada y expone funciones/clases reutilizables. La **separación de responsabilidades** permite modificar, probar y documentar cada pieza de forma aislada.

### Diagrama de capas

```
                    ┌─────────────────────────┐
                    │        main.py          │   PUNTO DE ENTRADA
                    │  (orquestador/pipeline) │
                    └───────────┬─────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
     ┌─────────┐          ┌──────────┐          ┌──────────────┐
     │solver.py│          │visualiza-│          │              │
     │ (motor  │─────────▶│ tion.py  │          │              │
     │event-   │          │(capas de │          │              │
     │driven)  │          │ gráfica) │          │              │
     └────┬────┘          └──────────┘          └──────────────┘
          │
    ┌─────┼────────┐
    ▼     ▼        ▼
┌────────┐ ┌────────────┐ ┌──────────────┐
│dynamics│ │  switching │ │   sliding    │
│ (ODE)  │ │(clasifica) │ │(deslizamiento)│
└────────┘ └─────┬──────┘ └──────────────┘
                 ▼
         ┌─────────────┐
         │ equilibrium │  (tangentes, equilibrio)
         └─────────────┘
                 │
                 ▼
         ┌─────────────┐
         │ parameters  │  (dataclasses de configuración)
         └─────────────┘
```

---

## 3. Módulos y capas

### Capa 1 — Configuración: `parameters.py`
Define **dataclasses inmutables** (`frozen=True`) que centralizan toda la configuración:
- **`FilippovParams`**: parámetros del modelo (`R0, μ, θ, u, w`).
- **`DomainParams`**: límites del dominio `[0,1]×[0,1]`.
- **`SolverParams`**: opciones del integrador (`tiempo_max`, `max_switches`, `max_step`, `rtol`, `atol`, `eps`, `tol`).

Al ser inmutables y centralizadas, el resto de módulos recibe los parámetros como argumentos tipados, evitando variables globales dispersas.

### Capa 2 — Motor numérico: `dynamics.py`
Define los **campos vectoriales** (las ODE del modelo):
- `vector_field_1(x, y, p)` → Sistema 1 (sin control).
- `vector_field_2(x, y, p)` → Sistema 2 (con control).
- `sliding_field_1d(x, w, p)` → dinámica reducida 1D sobre la frontera (aprovechando que `f1_x == f2_x`).

### Capa 3 — Geometría y análisis: `equilibrium.py`
Calcula los **puntos de equilibrio** y los **puntos tangentes** sobre la frontera:
- `compute_equilibria(p)` → equilibrios de ambos subsistemas (fórmula cuadrática para f2).
- `compute_tangent_points(w, p)` → puntos tangentes:
  - `T1 = (1/R0, w)` donde `f1_y = 0`.
  - `T2 = (1/R0)·(1 + u/((μ+θ)·w), w)` donde `f2_y = 0`.
  - **Entre T1 y T2** se ubica la zona de deslizamiento (sliding).

Estructuras de datos: dataclasses `Equilibria` y `TangentPoints`.

### Capa 4 — Clasificación de conmutación: `switching.py`
Implementa el **criterio de Filippov** para clasificar el comportamiento en la frontera.

Dado `H = y - w`, su gradiente es `∇H = (0, 1)`, por lo que el producto de proyecciones es:

```
l = ⟨∇H, f1⟩ · ⟨∇H, f2⟩ = f1_y · f2_y
```

Clasificación:
- **`l > 0`** → `CROSSING` (los campos apuntan al mismo lado; la trayectoria cruza).
- **`l < 0`** → `SLIDING` (los campos apuntan en direcciones opuestas; la trayectoria queda atrapada sobre la frontera).
- **`l = 0`** → `TANGENCY` (un campo es tangente a la frontera; punto T1 o T2).

Define el `Enum SwitchType` (`CROSSING`, `SLIDING`, `TANGENCY`) y la dataclass `SwitchAnalysis` (`L`, `f1_y`, `f2_y`, `switch_type`). Función principal: `compute_switching_analysis(x, w, p)`.

### Capa 5 — Dinámica de deslizamiento: `sliding.py`
Integra la **dinámica 1D** sobre la frontera cuando se detecta sliding:

```
dx/dt = sliding_field_1d(x, w) = μ(1 - x) - (μ + θ)·R0·x·w
```

Usa `solve_ivp` con **eventos de terminación** al llegar a `T1` o `T2`. Produce un `SlidingResult` con la trayectoria `x(t)` y las banderas `reached_T1` / `reached_T2`.

### Capa 6 — Motor de simulación: `solver.py`
Implementa el **bucle event-driven** de Filippov (algoritmo de **Piiroinen & Kuznetsov, 2008**). Orquesta todo el flujo:

1. Determina la región (`y < w`, `y > w`, o exactamente en la frontera).
2. Selecciona el campo vectorial correspondiente.
3. Integra con `solve_ivp` usando un **evento de cruce de frontera** (`y(t) - w = 0`, con la dirección correcta según el sistema).
4. En el punto de cruce, ejecuta `compute_switching_analysis`:
   - **Crossing** → empuja la trayectoria al otro lado (`±eps`).
   - **Sliding** → llama a `integrate_sliding`.
   - **Tangency** → registra el punto y decide a qué lado salir.
5. Repite hasta que la trayectoria sale del dominio o se agotan los `max_switches`.
6. Guarda todo en un `SimulationResult`.

Estructuras: `TrajectorySegment` (x, y, tipo de segmento) y `SimulationResult` (lista de segmentos, tangencias, punto inicial/final, nº de switches).

**La capa 6 (solver) es el núcleo del algoritmo:** integra las capas 2–5 y mantiene la lógica de control de la simulación.

### Capa 7 — Visualización: `visualization.py`
Genera el **retrato de fase**:
- `_make_vector_field_vectorizado` → evalúa los campos en la grilla **de forma vectorizada con NumPy** (≈50× más rápido que el bucle Python doble).
- `_plot_vector_fields` → streamplots del Sistema 1 (rojo, abajo) y Sistema 2 (azul, arriba).
- `_plot_boundary` → frontera `y = w` con 3 estilos (punteada → continua en la zona de sliding → punteada).
- `plot_phase_portrait` → función principal: campos, frontera, trayectorias por color (`darkred`/`darkblue`/`orange`), equilibrios, tangentes, condiciones iniciales, leyenda.

### Capa 8 — Punto de entrada: `main.py`
Orquesta el **pipeline completo**:
1. Crea las instancias de configuración (`FilippovParams`, `DomainParams`, `SolverParams`).
2. Define las condiciones iniciales.
3. Llama a `solver.simulate()` para cada CI.
4. Llama a `visualization.plot_phase_portrait()` para graficar.
5. Maximiza la ventana y muestra la figura.

Ejecución: `python main.py`.

---

## 4. Algoritmo event-driven (Piiroinen & Kuznetsov, 2008)

El corazón de la simulación es el **método event-driven** para sistemas de Filippov, que evita estabilizar la integración de forma manual. El flujo aproximado es:

```
inicio
  mientras (switch_count < max_switches):
    si y_act < w  → sistema 1
    si y_act > w  → sistema 2
    si y_act = w  → analizar y continuar

    integrar ODE hasta evento de cruce (y - w = 0)

    si no hubo cruce → terminar
    si hubo cruce:
        clasificar con l = f1_y * f2_y
        si l > 0  → CROSSING → empujar al otro lado
        si l < 0  → SLIDING  → integrar 1D hasta T1/T2
        si l = 0  → TANGENCY → salir por el lado adecuado
        verificar límites del dominio
fin
```

El **mecanismo de desigualdad/`eps`**: cuando la trayectoria queda exactamente en la frontera, se aplica una **perturbación infinitesimal `eps = 1e-6`** para "empujarla" fuera, de modo que el integrador no se quede atascado y pueda continuar en la región correcta en la siguiente iteración.

---

## 5. Mapa de dependencias

```
main.py ──────────────────────────────▶ parameters, solver, visualization
solver.py ────────────────────────────▶ dynamics, equilibrium, switching, sliding, parameters
switching.py ─────────────────────────▶ dynamics, parameters
sliding.py ───────────────────────────▶ dynamics, equilibrium, parameters
equilibrium.py ───────────────────────▶ parameters
dynamics.py ──────────────────────────▶ parameters
visualization.py ─────────────────────▶ equilibrium, parameters, solver
```

**Regla de capas:** ningún módulo de capa inferior importa desde una capa superior; las dependencias fluyen hacia abajo hacia `parameters.py`, que está en la base.

---

## 6. Referencias teóricas

- **Filippov, A.F. (1988).** *Differential Equations with Discontinuous Righthand Sides.* Kluwer Academic Publishers.
- **Piiroinen, P.T. & Kuznetsov, Y.A. (2008).** *An event-driven method to simulate Filippov systems with accurate computing of sliding motions.* ACM Transactions on Mathematical Software, 34(3), Art. 13.

---

## 7. Nota sobre `SImodel.py`

En la carpeta también existe `SImodel.py`, que es una **versión monolítica anterior** (todo el algoritmo, la simulación y el graficado en un solo archivo ejecutable). La arquitectura actual del proyecto es la **modular descrita en este documento**, cuyo punto de entrada es `main.py`. La evidencia es que `main.py`, `solver.py`, `dynamics.py`, `equilibrium.py`, `switching.py`, `sliding.py`, `visualization.py` y `parameters.py` son los módulos que se importan y ejecutan en conjunto, mientras que `SImodel.py` queda como pieza de referencia del enfoque monolítico.
