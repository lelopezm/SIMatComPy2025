# 📦 Caja de Polinomios

Una aplicación web interactiva diseñada para hacer más intuitivo el aprendizaje de las operaciones algebraicas para niños y adolescentes, utilizando un enfoque visual y dinámico basado en un plano cartesiano.

## 🎯 Descripción del Proyecto

**Caja de Polinomios** es una aplicación educativa que transforma la comprensión de las operaciones algebraicas en una experiencia visual e interactiva. A través de un plano cartesiano dinámico y un sistema de "fichas" virtuales, los estudiantes pueden visualizar y comprender cómo funcionan la suma, resta, multiplicación y división de polinomios.

## ✨ Características Principales

### 🎨 Interfaz de Usuario
- **Plano Cartesiano Interactivo**: Superficie principal donde se visualizan las operaciones
- **Sidebar Dinámico**: Panel lateral para entrada de polinomios y control de operaciones
- **Navegación Intuitiva**: Barra de navegación con acceso rápido a todas las funcionalidades
- **Diseño Responsivo**: Optimizado para diferentes dispositivos y tamaños de pantalla

### 🔧 Funcionalidades Avanzadas
- **Reconocimiento de Patrones**: Identificación automática de polinomios mediante expresiones regulares (RegEx)
- **Zoom Dinámico**: Capacidad de hacer zoom sobre el plano cartesiano para mejor visualización
- **Importación/Exportación**: Guardar y cargar configuraciones de trabajo
- **Paso a Paso**: Generación automática de soluciones detalladas para cada operación
- **Sistema de Ayuda**: Asistente contextual que explica cada paso del proceso

### 📱 Componentes de la Interfaz

#### Plano Cartesiano
- Visualización de polinomios como figuras geométricas
- Cuadrantes diferenciados por signos
- Sistema de fichas interactivas
- Zoom y navegación fluida

#### Sidebar
- **Entrada de Polinomios**: Campo de texto con validación en tiempo real
- **Selector de Operaciones**: Botones para suma, resta, multiplicación y división
- **Generador de Pasos**: Botón para mostrar la solución paso a paso
- **Lista de Figuras**: Visualización de todos los elementos en el plano

#### Navbar
- **Toggle Sidebar**: Mostrar/ocultar panel lateral
- **Banco de Figuras**: Acceso rápido a figuras predefinidas
- **Ayuda Contextual**: Sistema de ayuda inteligente
- **Configuraciones**: Opciones de personalización

## 🧮 Reglas de Operaciones

### ➕ Adición de Polinomios

1. **Preparación del Plano**: Dividir los cuadrantes del plano cartesiano por signos
2. **Primer Polinomio**: Ubicar las fichas en los dos cuadrantes superiores según los signos de cada término
3. **Segundo Polinomio**: Ubicar las fichas en los dos cuadrantes inferiores según los signos de cada término
4. **Traslado Diagonal**: Mover las fichas del polinomio inferior hacia arriba cruzándolas en diagonal
5. **Eliminación de Opuestos**: Remover las fichas similares que se encuentren en lados opuestos
6. **Lectura del Resultado**: Interpretar el polinomio resultante considerando los signos

### ➖ Sustracción de Polinomios

1. **Pasos Iniciales**: Seguir los primeros tres pasos de la adición
2. **Cambio de Lado**: Invertir la posición de las fichas del polinomio a restar (izquierda ↔ derecha)
3. **Finalización**: Repetir los pasos 4, 5 y 6 de la adición

### ✖️ Multiplicación de Polinomios

**Objetivo**: Formar un rectángulo de base P(x) y altura Q(x), con área P(x) · Q(x)

1. **Preparación de Fichas**: Tomar fichas para formar P(x) usando solo un lado de cada ficha
2. **Disposición Horizontal**: Ubicar las fichas de P(x) horizontalmente, considerando signos y que la altura coincida con un término de Q(x)
3. **Formación de Altura**: Agregar fichas para formar un rectángulo de altura Q(x)
4. **Completar Rectángulo**: Rellenar espacios vacíos hasta formar un rectángulo completo de base P(x) y altura Q(x)
5. **Análisis de Área**: Considerar el área y signo de cada ficha según su cuadrante
6. **Simplificación**: Eliminar términos semejantes y leer el resultado

### ➗ División de Polinomios

**Objetivo**: Construir un rectángulo con base Q(x) y altura desconocida usando las fichas del dividendo P(x)

1. **Preparación del Dividendo**: Tomar las fichas necesarias para formar P(x)
2. **Ubicación Inicial**: Colocar fichas en los dos cuadrantes superiores según signos
3. **Base del Rectángulo**: Formar un rectángulo de base Q(x) usando fichas de mayor grado
4. **Construcción Completa**: Completar el rectángulo con las fichas restantes, agregando ceros si es necesario
5. **Resultado**: El cociente será la altura del rectángulo construido, con posibles restos de grado menor a Q(x)

## 🛠️ Stack Tecnológico

### Frontend
- **React.js**: Framework principal para la interfaz de usuario
- **p5.js**: Librería para renderizado gráfico y interacciones del plano cartesiano
- **react-p5**: Wrapper de React para integrar p5.js
- **CSS3**: Estilos personalizados con metodología BEM
- **JavaScript ES6+**: Lógica de aplicación moderna

### Arquitectura
- **Atomic Design**: Metodología de diseño de componentes React
  - **Átomos**: Botones, inputs, etiquetas (componentes básicos)
  - **Moléculas**: Grupos de átomos (formularios, controles)
  - **Organismos**: Componentes complejos (sidebar, navbar, plano cartesiano)
  - **Plantillas**: Layouts y estructuras de página
  - **Páginas**: Instancias específicas de plantillas

### Funcionalidades Técnicas
- **react-p5**: Para renderizado del plano cartesiano interactivo
- **React Hooks**: Para manejo de estado y efectos
- **Context API**: Para estado global de la aplicación
- **RegEx Engine**: Para reconocimiento de patrones en polinomios
- **Local Storage**: Para persistencia de datos local
- **File API**: Para importación/exportación de archivos

## 🎯 Público Objetivo

- **Estudiantes**: Niños y adolescentes aprendiendo álgebra
- **Educadores**: Profesores buscando herramientas visuales de enseñanza
- **Padres**: Apoyo en el aprendizaje en casa

## 🚀 Características del Código

- **Código Legible**: Estructura clara y comentarios explicativos
- **Componentes Reutilizables**: Arquitectura modular con React
- **Manejo de Estado**: Gestión eficiente del estado de la aplicación
- **Responsive Design**: Adaptable a diferentes dispositivos
- **Accesibilidad**: Cumple con estándares de accesibilidad web

## 📁 Estructura del Proyecto (Atomic Design + React)

```
caja-de-polinomios/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── atoms/
│   │   │   ├── Button/
│   │   │   │   ├── Button.jsx
│   │   │   │   └── Button.css
│   │   │   ├── Input/
│   │   │   │   ├── Input.jsx
│   │   │   │   └── Input.css
│   │   │   └── Label/
│   │   │       ├── Label.jsx
│   │   │       └── Label.css
│   │   ├── molecules/
│   │   │   ├── PolynomialInput/
│   │   │   │   ├── PolynomialInput.jsx
│   │   │   │   └── PolynomialInput.css
│   │   │   ├── OperationSelector/
│   │   │   │   ├── OperationSelector.jsx
│   │   │   │   └── OperationSelector.css
│   │   │   └── HelpTooltip/
│   │   │       ├── HelpTooltip.jsx
│   │   │       └── HelpTooltip.css
│   │   ├── organisms/
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Sidebar.css
│   │   │   ├── Navbar/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Navbar.css
│   │   │   └── CartesianPlane/
│   │   │       ├── CartesianPlane.jsx
│   │   │       └── CartesianPlane.css
│   │   ├── templates/
│   │   │   └── MainLayout/
│   │   │       ├── MainLayout.jsx
│   │   │       └── MainLayout.css
│   │   └── pages/
│   │       └── Home/
│   │           ├── Home.jsx
│   │           └── Home.css
│   ├── contexts/
│   │   └── AppContext.js
│   ├── utils/
│   │   ├── polynomialParser.js
│   │   ├── regexPatterns.js
│   │   ├── operations.js
│   │   └── p5Utils.js
│   ├── hooks/
│   │   ├── usePolynomial.js
│   │   └── useCartesianPlane.js
│   ├── styles/
│   │   ├── globals.css
│   │   └── variables.css
│   ├── App.jsx
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

## 🎮 Guía de Uso

### Para Estudiantes
1. **Ingresa tu polinomio** en el campo de texto del sidebar
2. **Selecciona la operación** que deseas realizar
3. **Observa la visualización** en el plano cartesiano
4. **Usa el botón "Paso a Paso"** para ver la solución detallada
5. **Experimenta con el zoom** para mejor comprensión

### Para Educadores
- Utiliza la función de ayuda para explicar conceptos
- Exporta configuraciones para reutilizar en diferentes clases
- Aprovecha las visualizaciones para explicaciones grupales

## 🔮 Características Futuras

- **Modo Multijugador**: Colaboración en tiempo real
- **Gamificación**: Sistema de puntos y logros
- **Más Operaciones**: Factorización, raíces, etc.
- **Soporte Multiidioma**: Internacionalización
- **Integración LMS**: Conexión con plataformas educativas

## 🤝 Contribuciones

Este proyecto está abierto a contribuciones de la comunidad educativa y de desarrolladores interesados en mejorar la educación matemática.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

Para preguntas, sugerencias o colaboraciones, no dudes en contactarnos.

---

**¡Hagamos que las matemáticas sean más divertidas e intuitivas! 🎓✨**
