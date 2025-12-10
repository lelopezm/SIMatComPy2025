// Expresiones regulares para validar polinomios
export const polynomialPatterns = {
  // Término completo: coeficiente opcional + variable + exponente opcional
  term: /([+-]?\s*\d*\.?\d*)\s*([a-zA-Z])?\s*(\^?\s*\d+)?/g,
  
  // Validación general de polinomio
  polynomial: /^[+-]?\s*(\d*\.?\d*\s*[a-zA-Z]?\s*(\^?\s*\d+)?|[a-zA-Z]\s*(\^?\s*\d+)?|\d+\.?\d*)\s*([+-]\s*(\d*\.?\d*\s*[a-zA-Z]?\s*(\^?\s*\d+)?|[a-zA-Z]\s*(\^?\s*\d+)?|\d+\.?\d*))*$/,
  
  // Coeficiente
  coefficient: /^[+-]?\d*\.?\d*$/,
  
  // Variable con exponente
  variable: /^[a-zA-Z](\^?\d+)?$/,
  
  // Número constante
  constant: /^[+-]?\d+\.?\d*$/,
  
  // Operadores
  operator: /^[+-]$/
};

// Patrones específicos para diferentes tipos de términos
export const termPatterns = {
  // x^2, 2x^2, -3x^2, etc.
  quadratic: /([+-]?\s*\d*\.?\d*)\s*([a-zA-Z])\s*\^?\s*2/,
  
  // x, 2x, -3x, etc.
  linear: /([+-]?\s*\d*\.?\d*)\s*([a-zA-Z])(?!\s*\^)/,
  
  // 5, -3, 2.5, etc.
  constant: /([+-]?\s*\d+\.?\d*)(?!\s*[a-zA-Z])/
};

// Validar formato de polinomio completo
export const validatePolynomialFormat = (polynomial) => {
  if (!polynomial || typeof polynomial !== 'string') {
    return false;
  }
  
  const cleaned = polynomial.replace(/\s/g, '');
  return polynomialPatterns.polynomial.test(cleaned);
};

// Extraer términos individuales
export const extractTerms = (polynomial) => {
  const terms = [];
  const cleaned = polynomial.replace(/\s/g, '');
  
  // Dividir por operadores manteniendo el signo
  const parts = cleaned.split(/([+-])/).filter(part => part !== '');
  
  let currentTerm = '';
  for (let i = 0; i < parts.length; i++) {
    if (polynomialPatterns.operator.test(parts[i]) && i > 0) {
      if (currentTerm) {
        terms.push(currentTerm);
      }
      currentTerm = parts[i];
    } else {
      currentTerm += parts[i];
    }
  }
  
  if (currentTerm) {
    terms.push(currentTerm);
  }
  
  return terms;
};

// Validar un término individual
export const validateTerm = (term) => {
  const cleaned = term.replace(/\s/g, '');
  
  return (
    termPatterns.quadratic.test(cleaned) ||
    termPatterns.linear.test(cleaned) ||
    termPatterns.constant.test(cleaned)
  );
};

// Patrones para operaciones específicas
export const operationPatterns = {
  addition: {
    step1: /preparación.*plano/i,
    step2: /primer.*polinomio.*superior/i,
    step3: /segundo.*polinomio.*inferior/i,
    step4: /diagonal.*arriba/i,
    step5: /eliminar.*opuestos/i,
    step6: /leer.*resultado/i
  },
  
  subtraction: {
    step1: /tres.*primeros.*pasos/i,
    step2: /cambiar.*lado.*fichas/i,
    step3: /repetir.*pasos/i
  },
  
  multiplication: {
    step1: /fichas.*formar.*lado/i,
    step2: /horizontal.*signos/i,
    step3: /altura.*rectángulo/i,
    step4: /rellenar.*espacios/i,
    step5: /área.*signo/i,
    step6: /eliminar.*términos/i
  },
  
  division: {
    step1: /fichas.*dividendo/i,
    step2: /cuadrantes.*superiores/i,
    step3: /base.*mayor.*grado/i,
    step4: /rectángulo.*fichas.*sobrantes/i
  }
};

// Validar sintaxis específica para cada operación
export const validateOperationSyntax = (polynomial, operation) => {
  if (!validatePolynomialFormat(polynomial)) {
    return { valid: false, error: 'Formato de polinomio inválido' };
  }
  
  const terms = extractTerms(polynomial);
  
  switch (operation) {
    case 'addition':
    case 'subtraction':
      // Para suma y resta, cualquier polinomio válido es aceptable
      return { valid: true };
    
    case 'multiplication':
      // Para multiplicación, verificar que sea factorizable
      if (terms.length < 2) {
        return { 
          valid: false, 
          error: 'Para multiplicación se necesitan al menos 2 términos' 
        };
      }
      return { valid: true };
    
    case 'division':
      // Para división, verificar estructura apropiada
      if (terms.length < 2) {
        return { 
          valid: false, 
          error: 'Para división se necesita un polinomio divisible' 
        };
      }
      return { valid: true };
    
    default:
      return { valid: true };
  }
};

// Generar regex dinámico para autocompletado
export const generateAutocompletePattern = (input) => {
  const escaped = input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`^${escaped}`, 'i');
};

// Sugerencias de autocompletado
export const autocompleteSuggestions = [
  'x²', 'x^2', '2x²', '3x²', '-x²', '-2x²',
  'x', '2x', '3x', '-x', '-2x', '-3x',
  '1', '2', '3', '-1', '-2', '-3',
  'x² + x + 1', 'x² - 1', '2x² + 3x - 5',
  'x² + 2x + 1', 'x² - 4x + 4', 'x² - 2x - 3'
];

export default {
  polynomialPatterns,
  termPatterns,
  validatePolynomialFormat,
  extractTerms,
  validateTerm,
  operationPatterns,
  validateOperationSyntax,
  generateAutocompletePattern,
  autocompleteSuggestions
};
