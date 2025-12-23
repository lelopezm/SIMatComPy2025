import React from 'react';
import CartesianPlane from '../../organisms/CartesianPlane/CartesianPlane';
import { useApp } from '../../../contexts/AppContext';
import './Home.css';

const Home = () => {
  const { state } = useApp();
  const { currentOperation, result, stepByStep, currentStep } = state;

  return (
    <div className="home">
      {/* Área principal del plano cartesiano */}
      <section className="home__main-area">
        <div className="home__plane-container">
          <CartesianPlane className="home__cartesian-plane" />
        </div>
        
        {/* Panel de información superpuesto */}
        {(currentOperation || result) && (
          <div className="home__info-panel">
            {currentOperation && (
              <div className="home__operation-info">
                <h3 className="home__operation-title">
                  Operación Actual: {getOperationDisplayName(currentOperation)}
                </h3>
                
                {stepByStep.length > 0 && (
                  <div className="home__step-indicator">
                    <span className="home__step-text">
                      Paso {currentStep + 1} de {stepByStep.length}
                    </span>
                    <div className="home__step-progress">
                      <div 
                        className="home__step-progress-fill"
                        style={{ width: `${((currentStep + 1) / stepByStep.length) * 100}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {result && (
              <div className="home__result-info">
                <h4 className="home__result-title">Resultado:</h4>
                <div className="home__result-expression">
                  {result}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* Área de estado y estadísticas */}
      <section className="home__status-area">
        <div className="home__status-cards">
          <div className="status-card">
            <div className="status-card__icon">📐</div>
            <div className="status-card__content">
              <h4 className="status-card__title">Plano Cartesiano</h4>
              <p className="status-card__value">
                Zoom: {Math.round(state.plane.zoom * 100)}%
              </p>
            </div>
          </div>
          
          <div className="status-card">
            <div className="status-card__icon">🧮</div>
            <div className="status-card__content">
              <h4 className="status-card__title">Fichas Activas</h4>
              <p className="status-card__value">
                {state.plane.chips.length} fichas
              </p>
            </div>
          </div>
          
          <div className="status-card">
            <div className="status-card__icon">⚡</div>
            <div className="status-card__content">
              <h4 className="status-card__title">Estado</h4>
              <p className="status-card__value">
                {getStatusText(state)}
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

// Función auxiliar para obtener el nombre de la operación
const getOperationDisplayName = (operation) => {
  const names = {
    addition: 'Suma',
    subtraction: 'Resta',
    multiplication: 'Multiplicación',
    division: 'División'
  };
  return names[operation] || operation;
};

// Función auxiliar para obtener el texto de estado
const getStatusText = (state) => {
  const { polynomials, currentOperation, result } = state;
  
  if (result) return 'Completado';
  if (currentOperation) return 'Operando';
  if (polynomials.first.trim() && polynomials.second.trim()) return 'Listo para operar';
  if (polynomials.first.trim() || polynomials.second.trim()) return 'Ingresando datos';
  return 'Esperando entrada';
};

export default Home;
