import { 
  polynomialPatterns, 
  termPatterns, 
  extractTerms, 
  validateTerm 
} from './regexPatterns';

// Clase para representar un término de polinomio
export class PolynomialTerm {
  constructor(coefficient = 1, variable = '', exponent = 0) {
    this.coefficient = coefficient;
    this.variable = variable;
    this.exponent = exponent;
  }

  toString() {
    if (this.exponent === 0) {
      return this.coefficient.toString();
    }
    
    const coeff = this.coefficient === 1 ? '' : 
                  this.coefficient === -1 ? '-' : 
                  this.coefficient.toString();
    
    const exp = this.exponent === 1 ? '' : `^${this.exponent}`;
    
    return `${coeff}${this.variable}${exp}`;
  }

  equals(other) {
    return this.variable === other.variable && this.exponent === other.exponent;
  }

  getDegree() {
    return this.variable ? this.exponent : 0;
  }

  getType() {
    if (this.exponent === 0) return 'constant';
    if (this.exponent === 1) return 'linear';
    if (this.exponent === 2) return 'quadratic';
    return 'polynomial';
  }
}

// Clase para representar un polinomio completo
export class Polynomial {
  constructor(terms = []) {
    this.terms = terms;
  }

  getDegree() {
    return Math.max(...this.terms.map(term => term.getDegree()), 0);
  }

  getTermCount() {
    return this.terms.length;
  }

  toString() {
    if (this.terms.length === 0) return '0';
    
    return this.terms
      .map((term, index) => {
        const termStr = term.toString();
        if (index === 0) return termStr;
        
        const coeff = term.coefficient;
        if (coeff >= 0) {
          return `+ ${termStr}`;
        } else {
          return `- ${termStr.substring(1)}`;
        }
      })
      .join(' ');
  }

  getTermsByType() {
    return {
      quadratic: this.terms.filter(t => t.getType() === 'quadratic'),
      linear: this.terms.filter(t => t.getType() === 'linear'),
      constant: this.terms.filter(t => t.getType() === 'constant')
    };
  }
}

// Validar un polinomio
export const validatePolynomial = (polynomialStr) => {
  try {
    if (!polynomialStr || typeof polynomialStr !== 'string') {
      return {
        isValid: false,
        error: 'Debe ingresar un polinomio válido'
      };
    }

    const cleaned = polynomialStr.trim().replace(/\s+/g, '');
    
    if (!cleaned) {
      return {
        isValid: false,
        error: 'El polinomio no puede estar vacío'
      };
    }

    // Verificar formato general
    if (!polynomialPatterns.polynomial.test(cleaned)) {
      return {
        isValid: false,
        error: 'Formato de polinomio inválido. Use formato: ax² + bx + c'
      };
    }

    // Verificar cada término
    const terms = extractTerms(cleaned);
    for (const term of terms) {
      if (!validateTerm(term)) {
        return {
          isValid: false,
          error: `Término inválido: ${term}`
        };
      }
    }

    // Verificar que tenga al menos un término válido
    if (terms.length === 0) {
      return {
        isValid: false,
        error: 'No se encontraron términos válidos'
      };
    }

    return {
      isValid: true,
      terms: terms.length,
      degree: getDegree(polynomialStr)
    };

  } catch (error) {
    return {
      isValid: false,
      error: 'Error al validar el polinomio'
    };
  }
};

// Parsear un string de polinomio a objeto Polynomial
export const parsePolynomial = (polynomialStr) => {
  try {
    const cleaned = polynomialStr.trim().replace(/\s+/g, '');
    const termStrings = extractTerms(cleaned);
    const terms = [];

    for (const termStr of termStrings) {
      const term = parseTerm(termStr);
      if (term) {
        terms.push(term);
      }
    }

    return new Polynomial(terms);
  } catch (error) {
    console.error('Error parsing polynomial:', error);
    return new Polynomial([]);
  }
};

// Parsear un término individual
export const parseTerm = (termStr) => {
  try {
    const cleaned = termStr.trim().replace(/\s+/g, '');
    
    // Término cuadrático
    let match = termPatterns.quadratic.exec(cleaned);
    if (match) {
      const coeff = parseCoefficient(match[1]);
      const variable = match[2];
      return new PolynomialTerm(coeff, variable, 2);
    }

    // Término lineal
    match = termPatterns.linear.exec(cleaned);
    if (match) {
      const coeff = parseCoefficient(match[1]);
      const variable = match[2];
      return new PolynomialTerm(coeff, variable, 1);
    }

    // Término constante
    match = termPatterns.constant.exec(cleaned);
    if (match) {
      const coeff = parseFloat(match[1]);
      return new PolynomialTerm(coeff, '', 0);
    }

    return null;
  } catch (error) {
    console.error('Error parsing term:', error);
    return null;
  }
};

// Parsear coeficiente
const parseCoefficient = (coeffStr) => {
  if (!coeffStr || coeffStr === '+') return 1;
  if (coeffStr === '-') return -1;
  
  const cleaned = coeffStr.replace(/\s+/g, '');
  const num = parseFloat(cleaned);
  return isNaN(num) ? 1 : num;
};

// Obtener el grado de un polinomio
export const getDegree = (polynomialStr) => {
  try {
    const polynomial = parsePolynomial(polynomialStr);
    return polynomial.getDegree();
  } catch (error) {
    return 0;
  }
};

// Obtener términos agrupados por tipo
export const getTermsByType = (polynomialStr) => {
  try {
    const polynomial = parsePolynomial(polynomialStr);
    return polynomial.getTermsByType();
  } catch (error) {
    return { quadratic: [], linear: [], constant: [] };
  }
};

// Normalizar polinomio (combinar términos similares)
export const normalizePolynomial = (polynomialStr) => {
  try {
    const polynomial = parsePolynomial(polynomialStr);
    const termGroups = {};

    // Agrupar términos similares
    for (const term of polynomial.terms) {
      const key = `${term.variable}_${term.exponent}`;
      if (termGroups[key]) {
        termGroups[key].coefficient += term.coefficient;
      } else {
        termGroups[key] = new PolynomialTerm(
          term.coefficient, 
          term.variable, 
          term.exponent
        );
      }
    }

    // Filtrar términos con coeficiente cero y ordenar por grado
    const normalizedTerms = Object.values(termGroups)
      .filter(term => term.coefficient !== 0)
      .sort((a, b) => b.exponent - a.exponent);

    return new Polynomial(normalizedTerms);
  } catch (error) {
    console.error('Error normalizing polynomial:', error);
    return new Polynomial([]);
  }
};

// Convertir polinomio a formato LaTeX
export const toLatex = (polynomialStr) => {
  try {
    const polynomial = parsePolynomial(polynomialStr);
    return polynomial.terms
      .map(term => {
        let result = '';
        
        if (term.coefficient !== 1 || term.exponent === 0) {
          result += term.coefficient;
        }
        
        if (term.variable) {
          result += term.variable;
          
          if (term.exponent > 1) {
            result += `^{${term.exponent}}`;
          }
        }
        
        return result;
      })
      .join(' + ')
      .replace(/\+ -/g, '- ');
  } catch (error) {
    return polynomialStr;
  }
};

// Generar sugerencias de autocompletado
export const generateSuggestions = (input) => {
  const suggestions = [];
  const inputLower = input.toLowerCase();

  // Sugerencias basadas en patrones comunes
  const commonPatterns = [
    'x²', 'x^2', '2x²', '3x²', '-x²',
    'x', '2x', '3x', '-x', '-2x',
    '+', '-', '+ x', '- x', '+ 1', '- 1'
  ];

  for (const pattern of commonPatterns) {
    if (pattern.toLowerCase().startsWith(inputLower)) {
      suggestions.push(pattern);
    }
  }

  return suggestions.slice(0, 5); // Limitar a 5 sugerencias
};

export default {
  PolynomialTerm,
  Polynomial,
  validatePolynomial,
  parsePolynomial,
  parseTerm,
  getDegree,
  getTermsByType,
  normalizePolynomial,
  toLatex,
  generateSuggestions
};
