# 🧮 Caja de Polinomios

Una aplicación educativa interactiva diseñada para hacer más intuitivo el aprendizaje de las operaciones algebraicas para niños y adolescentes.

## 🎯 Descripción

**Caja de Polinomios** es una herramienta educativa que combina visualización gráfica con interactividad para enseñar conceptos algebraicos fundamentales. Los estudiantes pueden introducir polinomios, realizar operaciones y ver los resultados tanto algebraica como gráficamente en tiempo real.

## ✨ Características Principales

- **🎨 Visualización Interactiva**: Plano cartesiano dinámico con p5.js
- **📝 Interface Intuitiva**: Entrada de polinomios con validación en tiempo real
- **🧮 Operaciones Algebraicas**: Suma, resta y multiplicación de polinomios
- **📱 Diseño Responsivo**: Funciona en dispositivos móviles y escritorio
- **♿ Accesibilidad**: Cumple con estándares WCAG 2.1
- **🎯 Feedback Visual**: Retroalimentación inmediata y educativa

## 🛠️ Tecnologías

- **Frontend**: React 18 con Hooks y Context API
- **Visualización**: p5.js con react-p5 wrapper
- **Arquitectura**: Atomic Design (Átomos → Moléculas → Organismos → Plantillas → Páginas)
- **Estilos**: CSS3 moderno con variables personalizadas
- **Build**: Create React App con configuración personalizada

## 🏗️ Arquitectura del Proyecto

```
src/
├── components/
│   ├── atoms/          # Componentes básicos (Button, Input, Label)
│   ├── molecules/      # Componentes compuestos (PolynomialInput, OperationSelector)
│   ├── organisms/      # Componentes complejos (CartesianPlane, Sidebar, Navbar)
│   ├── templates/      # Layouts (MainLayout)
│   └── pages/          # Páginas completas (Home)
├── contexts/           # Estado global con Context API
├── utils/              # Utilidades (parsers, operaciones, p5)
└── styles/             # Sistema de estilos global
```

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Node.js 16.0.0 o superior
- npm 7.0.0 o superior

### Pasos de Instalación

1. **Clonar o crear el proyecto**
   ```bash
   mkdir caja-de-polinomios
   cd caja-de-polinomios
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Ejecutar en modo desarrollo**
   ```bash
   npm start
   ```

4. **Abrir en el navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:3000`

### Scripts Disponibles

```bash
npm start         # Servidor de desarrollo
npm run build     # Build de producción
npm test          # Ejecutar tests
npm run eject     # Exponer configuración de Webpack
```

## 🎮 Uso de la Aplicación

### Entrada de Polinomios

1. **Formato Aceptado**: Utiliza notación algebraica estándar
   - Ejemplos: `2x^2 + 3x - 1`, `x^3 - 4x + 2`, `5x^2 + 7`

2. **Validación en Tiempo Real**: 
   - ✅ Verde: Polinomio válido
   - ❌ Rojo: Error de sintaxis
   - 💡 Sugerencias automáticas

### Operaciones Disponibles

- **➕ Suma**: Combina términos semejantes
- **➖ Resta**: Resta término a término
- **✖️ Multiplicación**: Producto completo con distribución

### Visualización

- **Plano Cartesiano Interactivo**:
  - Zoom con rueda del mouse
  - Pan arrastrando
  - Grilla adaptativa
  - Múltiples colores para distintos polinomios

## 🎨 Componentes Principales

### Átomos (Atoms)
- `Button`: Botones con múltiples variantes
- `Input`: Campos de entrada con validación
- `Label`: Etiquetas descriptivas

### Moléculas (Molecules)
- `PolynomialInput`: Entrada especializada para polinomios
- `OperationSelector`: Selector visual de operaciones
- `HelpTooltip`: Ayuda contextual

### Organismos (Organisms)
- `CartesianPlane`: Visualización con p5.js
- `Sidebar`: Panel lateral con controles
- `Navbar`: Barra de navegación principal

## 🔧 Configuración Avanzada

### Variables CSS Personalizables

```css
:root {
  --primary-color: #2563eb;
  --secondary-color: #7c3aed;
  --success-color: #059669;
  --warning-color: #d97706;
  --error-color: #dc2626;
}
```

### Estado Global

El estado se maneja con `useReducer` y Context API:

```javascript
const { state, dispatch } = useAppContext();
// state.polynomials - Polinomios actuales
// state.operation - Operación seleccionada
// state.result - Resultado calculado
// state.ui - Estado de la interfaz
```

## 🧪 Testing

### Estructura de Tests

```bash
npm test                    # Ejecutar todos los tests
npm test -- --coverage     # Con reporte de cobertura
npm test -- --watch        # Modo watch para desarrollo
```

### Tipos de Tests

- **Unit Tests**: Componentes individuales
- **Integration Tests**: Flujos de usuario
- **Utils Tests**: Funciones de utilidad
- **Visual Tests**: Rendering de componentes

## 🎯 Roadmap

### Versión 1.0 (Actual)
- ✅ Entrada y validación de polinomios
- ✅ Operaciones básicas (suma, resta, multiplicación)
- ✅ Visualización gráfica interactiva
- ✅ Interface responsiva

### Versión 1.1 (Próximamente)
- 🔄 División de polinomios
- 🔄 Factorización básica
- 🔄 Historial de operaciones
- 🔄 Exportar resultados

### Versión 2.0 (Futuro)
- 📋 Modo tutorial interactivo
- 🎨 Temas personalizables
- 💾 Guardar progreso
- 👥 Modo colaborativo

## 🤝 Contribución

### Cómo Contribuir

1. **Fork** del repositorio
2. **Crear** una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** de cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abrir** un Pull Request

### Estándares de Código

- **ESLint**: Configuración estándar de React
- **Prettier**: Formateo automático
- **Atomic Design**: Estructura de componentes
- **BEM**: Metodología CSS

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Equipo

Desarrollado con ❤️ para hacer el aprendizaje algebraico más accesible y divertido.

## 🆘 Soporte

Si encuentras algún problema o tienes sugerencias:

1. **Issues**: Reporta bugs o solicita features
2. **Discusiones**: Comparte ideas y mejoras
3. **Wiki**: Documentación extendida

---

*Caja de Polinomios - Haciendo las matemáticas más visuales e interactivas* 🎓✨
