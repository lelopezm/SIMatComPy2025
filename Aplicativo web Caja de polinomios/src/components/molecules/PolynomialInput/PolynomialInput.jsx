import React, { useState, useCallback } from 'react';
import Input from '../../atoms/Input/Input';
import Label from '../../atoms/Label/Label';
import { useApp } from '../../../contexts/AppContext';
import { validatePolynomial, parsePolynomial } from '../../../utils/polynomialParser';
import './PolynomialInput.css';

const PolynomialInput = ({ 
  type = 'first', // 'first' or 'second'
  placeholder = "Ejemplo: 3x² + 2x - 1",
  className = ''
}) => {
  const { state, actions } = useApp();
  const [error, setError] = useState('');
  const [isValid, setIsValid] = useState(false);

  const polynomial = state.polynomials[type];

  const handleChange = useCallback((e) => {
    const value = e.target.value;
    actions.setPolynomial(type, value);

    // Validación en tiempo real
    if (value.trim()) {
      const validation = validatePolynomial(value);
      if (validation.isValid) {
        setError('');
        setIsValid(true);
      } else {
        setError(validation.error);
        setIsValid(false);
      }
    } else {
      setError('');
      setIsValid(false);
    }
  }, [actions, type]);

  const handleFocus = useCallback(() => {
    setError('');
  }, []);

  const getVariant = () => {
    if (error) return 'error';
    if (isValid && polynomial.trim()) return 'success';
    return 'polynomial';
  };

  const getHelperText = () => {
    if (error) return error;
    if (polynomial.trim() && isValid) {
      const parsed = parsePolynomial(polynomial);
      return `Detectado: polinomio de grado ${parsed.degree} con ${parsed.terms.length} términos`;
    }
    return 'Usa variables como x, y operadores +, -, *, ^';
  };

  return (
    <div className={`polynomial-input ${className}`}>
      <Label 
        variant="math"
        size="medium"
        htmlFor={`polynomial-${type}`}
      >
        {type === 'first' ? 'Primer Polinomio P(x)' : 'Segundo Polinomio Q(x)'}
      </Label>
      
      <Input
        id={`polynomial-${type}`}
        type="text"
        variant={getVariant()}
        size="large"
        placeholder={placeholder}
        value={polynomial}
        onChange={handleChange}
        onFocus={handleFocus}
        error={error}
        helperText={getHelperText()}
        className="polynomial-input__field"
      />
      
      {polynomial.trim() && isValid && (
        <div className="polynomial-input__preview">
          <Label variant="operation" size="small">
            Vista previa:
          </Label>
          <div className="polynomial-input__formatted">
            {formatPolynomialDisplay(polynomial)}
          </div>
        </div>
      )}
    </div>
  );
};

// Función auxiliar para formatear la visualización del polinomio
const formatPolynomialDisplay = (polynomial) => {
  return polynomial
    .replace(/\*/g, '')
    .replace(/\^/g, '')
    .replace(/(\d)([a-z])/gi, '$1$2')
    .replace(/([a-z])(\d)/gi, '$1^$2');
};

export default PolynomialInput;
