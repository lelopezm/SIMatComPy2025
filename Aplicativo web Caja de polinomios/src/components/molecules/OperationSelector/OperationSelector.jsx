import React from 'react';
import Button from '../../atoms/Button/Button';
import { useApp } from '../../../contexts/AppContext';
import './OperationSelector.css';

const OperationSelector = ({ className = '' }) => {
  const { state, actions } = useApp();
  const { currentOperation } = state;

  const operations = [
    {
      id: 'addition',
      symbol: '+',
      name: 'Suma',
      description: 'Sumar polinomios usando cuadrantes'
    },
    {
      id: 'subtraction',
      symbol: '−',
      name: 'Resta',
      description: 'Restar polinomios cambiando signos'
    },
    {
      id: 'multiplication',
      symbol: '×',
      name: 'Multiplicación',
      description: 'Formar rectángulos de área'
    },
    {
      id: 'division',
      symbol: '÷',
      name: 'División',
      description: 'Construir rectángulos con base conocida'
    }
  ];

  const handleOperationChange = (operationId) => {
    actions.setOperation(operationId);
  };

  const canCalculate = () => {
    const { first, second } = state.polynomials;
    return first.trim() && second.trim() && currentOperation;
  };

  return (
    <div className={`operation-selector ${className}`}>
      <div className="operation-selector__header">
        <h3 className="operation-selector__title">
          Selecciona la Operación
        </h3>
        <p className="operation-selector__subtitle">
          Elige cómo quieres operar los polinomios
        </p>
      </div>

      <div className="operation-selector__grid">
        {operations.map((operation) => (
          <button
            key={operation.id}
            className={`operation-card ${
              currentOperation === operation.id ? 'operation-card--active' : ''
            }`}
            onClick={() => handleOperationChange(operation.id)}
          >
            <div className="operation-card__symbol">
              {operation.symbol}
            </div>
            
            <div className="operation-card__content">
              <h4 className="operation-card__name">
                {operation.name}
              </h4>
              <p className="operation-card__description">
                {operation.description}
              </p>
            </div>
          </button>
        ))}
      </div>

      {currentOperation && (
        <div className="operation-selector__actions">
          <Button
            variant="primary"
            size="large"
            disabled={!canCalculate()}
            onClick={() => {
              // Aquí se ejecutaría la operación
              console.log('Ejecutar operación:', currentOperation);
            }}
            className="operation-selector__calculate-btn"
          >
            Calcular {operations.find(op => op.id === currentOperation)?.name}
          </Button>
          
          <Button
            variant="outline"
            size="medium"
            onClick={() => {
              // Mostrar paso a paso
              console.log('Mostrar paso a paso');
            }}
            disabled={!canCalculate()}
          >
            Ver Paso a Paso
          </Button>
        </div>
      )}
    </div>
  );
};

export default OperationSelector;
