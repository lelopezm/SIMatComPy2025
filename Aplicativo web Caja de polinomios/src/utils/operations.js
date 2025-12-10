import { parsePolynomial, normalizePolynomial } from './polynomialParser';

// Realizar suma de polinomios
export const addPolynomials = (poly1Str, poly2Str) => {
  try {
    const poly1 = parsePolynomial(poly1Str);
    const poly2 = parsePolynomial(poly2Str);
    
    // Combinar todos los términos
    const allTerms = [...poly1.terms, ...poly2.terms];
    
    // Crear polinomio temporal para normalizar
    const tempPolyStr = allTerms
      .map(term => term.toString())
      .join(' + ')
      .replace(/\+ -/g, '- ');
    
    const result = normalizePolynomial(tempPolyStr);
    
    return {
      result: result.toString(),
      steps: generateAdditionSteps(poly1, poly2, result)
    };
  } catch (error) {
    throw new Error('Error en la suma de polinomios: ' + error.message);
  }
};

// Realizar resta de polinomios
export const subtractPolynomials = (poly1Str, poly2Str) => {
  try {
    const poly1 = parsePolynomial(poly1Str);
    const poly2 = parsePolynomial(poly2Str);
    
    // Cambiar signos del segundo polinomio
    const negatedPoly2Terms = poly2.terms.map(term => ({
      ...term,
      coefficient: -term.coefficient
    }));
    
    // Combinar términos
    const allTerms = [...poly1.terms, ...negatedPoly2Terms];
    
    const tempPolyStr = allTerms
      .map(term => term.toString())
      .join(' + ')
      .replace(/\+ -/g, '- ');
    
    const result = normalizePolynomial(tempPolyStr);
    
    return {
      result: result.toString(),
      steps: generateSubtractionSteps(poly1, poly2, result)
    };
  } catch (error) {
    throw new Error('Error en la resta de polinomios: ' + error.message);
  }
};

// Realizar multiplicación de polinomios
export const multiplyPolynomials = (poly1Str, poly2Str) => {
  try {
    const poly1 = parsePolynomial(poly1Str);
    const poly2 = parsePolynomial(poly2Str);
    
    const resultTerms = [];
    
    // Multiplicar cada término de poly1 con cada término de poly2
    for (const term1 of poly1.terms) {
      for (const term2 of poly2.terms) {
        const newCoeff = term1.coefficient * term2.coefficient;
        const newVar = term1.variable || term2.variable;
        const newExp = term1.exponent + term2.exponent;
        
        resultTerms.push({
          coefficient: newCoeff,
          variable: newVar,
          exponent: newExp,
          toString() {
            if (this.exponent === 0) return this.coefficient.toString();
            const coeff = this.coefficient === 1 ? '' : 
                         this.coefficient === -1 ? '-' : 
                         this.coefficient.toString();
            const exp = this.exponent === 1 ? '' : `^${this.exponent}`;
            return `${coeff}${this.variable}${exp}`;
          }
        });
      }
    }
    
    const tempPolyStr = resultTerms
      .map(term => term.toString())
      .join(' + ')
      .replace(/\+ -/g, '- ');
    
    const result = normalizePolynomial(tempPolyStr);
    
    return {
      result: result.toString(),
      steps: generateMultiplicationSteps(poly1, poly2, result, resultTerms)
    };
  } catch (error) {
    throw new Error('Error en la multiplicación de polinomios: ' + error.message);
  }
};

// Realizar división de polinomios (división sintética básica)
export const dividePolynomials = (dividendStr, divisorStr) => {
  try {
    const dividend = parsePolynomial(dividendStr);
    const divisor = parsePolynomial(divisorStr);
    
    if (divisor.getDegree() > dividend.getDegree()) {
      return {
        quotient: '0',
        remainder: dividendStr,
        steps: [{
          title: 'División no posible',
          description: 'El grado del divisor es mayor que el del dividendo',
          action: 'El cociente es 0 y el residuo es el dividendo original'
        }]
      };
    }
    
    // Implementación básica de división polinomial
    // Por simplicidad, implementamos casos básicos
    
    return {
      quotient: 'x + 1', // Placeholder
      remainder: '0',
      steps: generateDivisionSteps(dividend, divisor)
    };
  } catch (error) {
    throw new Error('Error en la división de polinomios: ' + error.message);
  }
};

// Generar pasos para suma
const generateAdditionSteps = (poly1, poly2, result) => [
  {
    id: 1,
    title: 'Paso 1: Preparación del Plano',
    description: 'Dividimos los cuadrantes del plano cartesiano por signos. Los cuadrantes I y IV representan términos positivos, mientras que los II y III representan términos negativos.',
    action: 'Configurar cuadrantes según signos',
    visualization: {
      type: 'quadrant_setup',
      data: { positive: ['I', 'IV'], negative: ['II', 'III'] }
    }
  },
  {
    id: 2,
    title: 'Paso 2: Ubicar Primer Polinomio',
    description: `Colocamos las fichas del primer polinomio P(x) = ${poly1.toString()} en los cuadrantes superiores (I y II) según el signo de cada término.`,
    action: 'Posicionar fichas del primer polinomio',
    visualization: {
      type: 'place_polynomial',
      data: { polynomial: poly1, quadrants: ['I', 'II'] }
    }
  },
  {
    id: 3,
    title: 'Paso 3: Ubicar Segundo Polinomio',
    description: `Colocamos las fichas del segundo polinomio Q(x) = ${poly2.toString()} en los cuadrantes inferiores (III y IV) según el signo de cada término.`,
    action: 'Posicionar fichas del segundo polinomio',
    visualization: {
      type: 'place_polynomial',
      data: { polynomial: poly2, quadrants: ['III', 'IV'] }
    }
  },
  {
    id: 4,
    title: 'Paso 4: Traslado Diagonal',
    description: 'Movemos las fichas del polinomio inferior hacia arriba, cruzándolas en diagonal para combinar términos similares.',
    action: 'Mover fichas diagonalmente',
    visualization: {
      type: 'diagonal_move',
      data: { direction: 'up' }
    }
  },
  {
    id: 5,
    title: 'Paso 5: Eliminación de Opuestos',
    description: 'Eliminamos del juego las fichas similares que se encuentren en lados opuestos, ya que se cancelan mutuamente.',
    action: 'Cancelar términos opuestos',
    visualization: {
      type: 'cancel_opposites',
      data: {}
    }
  },
  {
    id: 6,
    title: 'Paso 6: Lectura del Resultado',
    description: `El resultado final es: ${result.toString()}. Leemos el polinomio resultante teniendo en cuenta los signos de los cuadrantes donde quedaron las fichas.`,
    action: 'Interpretar resultado final',
    visualization: {
      type: 'final_result',
      data: { result: result.toString() }
    }
  }
];

// Generar pasos para resta
const generateSubtractionSteps = (poly1, poly2, result) => [
  {
    id: 1,
    title: 'Pasos Iniciales',
    description: 'Seguimos los primeros tres pasos de la adición para ubicar ambos polinomios en el plano.',
    action: 'Aplicar pasos 1-3 de suma',
    visualization: {
      type: 'setup_subtraction',
      data: { poly1, poly2 }
    }
  },
  {
    id: 2,
    title: 'Cambio de Lado',
    description: `Cambiamos de lado las fichas del polinomio Q(x) = ${poly2.toString()} que deseamos restar. Las fichas de la izquierda las pasamos a la derecha y viceversa.`,
    action: 'Invertir posición de fichas',
    visualization: {
      type: 'flip_sides',
      data: { polynomial: poly2 }
    }
  },
  {
    id: 3,
    title: 'Finalización',
    description: `Repetimos los pasos 4, 5 y 6 de la adición. El resultado final es: ${result.toString()}.`,
    action: 'Completar como en suma',
    visualization: {
      type: 'complete_subtraction',
      data: { result: result.toString() }
    }
  }
];

// Generar pasos para multiplicación
const generateMultiplicationSteps = (poly1, poly2, result, intermediateTerms) => [
  {
    id: 1,
    title: 'Preparación de Fichas',
    description: `Tomamos las fichas necesarias para formar P(x) = ${poly1.toString()} usando sólo uno de los lados de cada ficha. El otro lado debe coincidir con términos de Q(x) = ${poly2.toString()}.`,
    action: 'Preparar fichas base',
    visualization: {
      type: 'prepare_multiplication',
      data: { base: poly1, height: poly2 }
    }
  },
  {
    id: 2,
    title: 'Disposición Horizontal',
    description: 'Ubicamos las fichas de P(x) horizontalmente, considerando los signos y que la altura coincida con términos de Q(x).',
    action: 'Formar base horizontal',
    visualization: {
      type: 'horizontal_layout',
      data: { polynomial: poly1 }
    }
  },
  {
    id: 3,
    title: 'Formación de Altura',
    description: 'Agregamos fichas para formar un rectángulo de altura Q(x), manteniendo la base P(x).',
    action: 'Construir altura',
    visualization: {
      type: 'build_height',
      data: { height: poly2 }
    }
  },
  {
    id: 4,
    title: 'Completar Rectángulo',
    description: 'Rellenamos los espacios vacíos con fichas hasta formar un rectángulo completo de base P(x) y altura Q(x).',
    action: 'Rellenar espacios',
    visualization: {
      type: 'fill_rectangle',
      data: { terms: intermediateTerms }
    }
  },
  {
    id: 5,
    title: 'Análisis de Área',
    description: 'Analizamos el área de cada ficha y su signo según el cuadrante donde se encuentre.',
    action: 'Calcular áreas',
    visualization: {
      type: 'analyze_areas',
      data: { terms: intermediateTerms }
    }
  },
  {
    id: 6,
    title: 'Simplificación',
    description: `Eliminamos términos semejantes y leemos el resultado: ${result.toString()}.`,
    action: 'Simplificar resultado',
    visualization: {
      type: 'simplify_result',
      data: { result: result.toString() }
    }
  }
];

// Generar pasos para división
const generateDivisionSteps = (dividend, divisor) => [
  {
    id: 1,
    title: 'Preparación del Dividendo',
    description: `Tomamos las fichas necesarias para formar el dividendo P(x) = ${dividend.toString()}.`,
    action: 'Preparar fichas del dividendo',
    visualization: {
      type: 'prepare_dividend',
      data: { dividend }
    }
  },
  {
    id: 2,
    title: 'Ubicación Inicial',
    description: 'Inicialmente, ubicamos las fichas en los dos cuadrantes superiores, teniendo en cuenta el signo de cada término.',
    action: 'Posicionar en cuadrantes superiores',
    visualization: {
      type: 'initial_placement',
      data: { dividend }
    }
  },
  {
    id: 3,
    title: 'Base del Rectángulo',
    description: `Sobre el eje x, formamos un rectángulo de base el divisor Q(x) = ${divisor.toString()} usando fichas de mayor grado.`,
    action: 'Formar base con divisor',
    visualization: {
      type: 'form_base',
      data: { divisor }
    }
  },
  {
    id: 4,
    title: 'Construcción Completa',
    description: 'Sin cambiar la base, construimos un rectángulo con las fichas sobrantes, agregando ceros si es necesario.',
    action: 'Completar rectángulo',
    visualization: {
      type: 'complete_division',
      data: { dividend, divisor }
    }
  }
];

// Validar operación antes de ejecutar
export const validateOperation = (poly1Str, poly2Str, operation) => {
  try {
    if (!poly1Str.trim() || !poly2Str.trim()) {
      return {
        valid: false,
        error: 'Ambos polinomios deben estar completos'
      };
    }

    const poly1 = parsePolynomial(poly1Str);
    const poly2 = parsePolynomial(poly2Str);

    if (poly1.terms.length === 0 || poly2.terms.length === 0) {
      return {
        valid: false,
        error: 'Los polinomios deben tener términos válidos'
      };
    }

    switch (operation) {
      case 'division':
        if (poly2.getDegree() === 0 && poly2.terms[0]?.coefficient === 0) {
          return {
            valid: false,
            error: 'No se puede dividir por cero'
          };
        }
        break;
      
      case 'multiplication':
        const totalDegree = poly1.getDegree() + poly2.getDegree();
        if (totalDegree > 6) {
          return {
            valid: false,
            error: 'El resultado sería demasiado complejo para visualizar'
          };
        }
        break;
    }

    return { valid: true };
  } catch (error) {
    return {
      valid: false,
      error: 'Error al validar la operación: ' + error.message
    };
  }
};

export default {
  addPolynomials,
  subtractPolynomials,
  multiplyPolynomials,
  dividePolynomials,
  validateOperation
};
