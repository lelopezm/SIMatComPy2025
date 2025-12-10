import React from 'react';
import Button from '../../atoms/Button/Button';
import PolynomialInput from '../../molecules/PolynomialInput/PolynomialInput';
import OperationSelector from '../../molecules/OperationSelector/OperationSelector';
import HelpTooltip from '../../molecules/HelpTooltip/HelpTooltip';
import { useApp } from '../../../contexts/AppContext';
import './Sidebar.css';

const Sidebar = ({ className = '' }) => {
  const { state, actions } = useApp();
  const { ui, currentOperation, stepByStep, currentStep } = state;

  const handleClearAll = () => {
    actions.setPolynomial('first', '');
    actions.setPolynomial('second', '');
    actions.setOperation(null);
    actions.clearPlane();
  };

  const handleExport = () => {
    const data = {
      polynomials: state.polynomials,
      operation: state.currentOperation,
      result: state.result,
      timestamp: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `caja-polinomios-${Date.now()}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
  };

  const handleImport = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        
        if (data.polynomials) {
          actions.setPolynomial('first', data.polynomials.first || '');
          actions.setPolynomial('second', data.polynomials.second || '');
        }
        
        if (data.operation) {
          actions.setOperation(data.operation);
        }
        
        console.log('Datos importados correctamente');
      } catch (error) {
        console.error('Error al importar el archivo:', error);
        alert('Error al importar el archivo. Verifica que sea un archivo JSON válido.');
      }
    };
    
    reader.readAsText(file);
    // Reset the input
    event.target.value = '';
  };

  return (
    <aside className={`sidebar ${!ui.sidebarVisible ? 'sidebar--hidden' : ''} ${className}`}>
      <div className="sidebar__header">
        <div className="sidebar__title-group">
          <h2 className="sidebar__title">
            Caja de Polinomios
          </h2>
          <HelpTooltip
            title="¿Qué es la Caja de Polinomios?"
            content="Una herramienta interactiva para visualizar y aprender operaciones algebraicas usando un plano cartesiano y fichas virtuales."
            position="bottom"
          >
            <Button variant="ghost" size="small" icon="?" />
          </HelpTooltip>
        </div>
        
        <Button
          variant="ghost"
          size="small"
          icon="×"
          onClick={actions.toggleSidebar}
          className="sidebar__close-btn"
          aria-label="Cerrar panel"
        />
      </div>

      <div className="sidebar__content">
        <section className="sidebar__section">
          <div className="sidebar__section-header">
            <h3 className="sidebar__section-title">
              Entrada de Polinomios
            </h3>
            <HelpTooltip
              title="Formato de Polinomios"
              content={(
                <div>
                  <p>Ejemplos de formatos válidos:</p>
                  <ul>
                    <li><code>3x² + 2x - 1</code></li>
                    <li><code>x^2 - 4</code></li>
                    <li><code>2*x + 5</code></li>
                    <li><code>x² + 3x + 2</code></li>
                  </ul>
                </div>
              )}
              position="right"
            />
          </div>
          
          <div className="sidebar__polynomials">
            <PolynomialInput
              type="first"
              placeholder="Ejemplo: 3x² + 2x - 1"
            />
            
            <PolynomialInput
              type="second"
              placeholder="Ejemplo: x² - 4"
            />
          </div>
        </section>

        <section className="sidebar__section">
          <OperationSelector />
        </section>

        {stepByStep.length > 0 && (
          <section className="sidebar__section">
            <div className="sidebar__section-header">
              <h3 className="sidebar__section-title">
                Paso a Paso
              </h3>
              <span className="sidebar__step-counter">
                {currentStep + 1} de {stepByStep.length}
              </span>
            </div>
            
            <div className="sidebar__steps">
              <div className="step-viewer">
                <div className="step-viewer__content">
                  <h4 className="step-viewer__title">
                    {stepByStep[currentStep]?.title}
                  </h4>
                  <p className="step-viewer__description">
                    {stepByStep[currentStep]?.description}
                  </p>
                </div>
                
                <div className="step-viewer__controls">
                  <Button
                    variant="outline"
                    size="small"
                    onClick={() => actions.setCurrentStep(Math.max(0, currentStep - 1))}
                    disabled={currentStep === 0}
                  >
                    Anterior
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="small"
                    onClick={() => actions.setCurrentStep(Math.min(stepByStep.length - 1, currentStep + 1))}
                    disabled={currentStep === stepByStep.length - 1}
                  >
                    Siguiente
                  </Button>
                </div>
              </div>
            </div>
          </section>
        )}

        <section className="sidebar__section">
          <div className="sidebar__section-header">
            <h3 className="sidebar__section-title">
              Herramientas
            </h3>
          </div>
          
          <div className="sidebar__tools">
            <Button
              variant="outline"
              size="medium"
              onClick={handleClearAll}
              className="sidebar__tool-btn"
            >
              Limpiar Todo
            </Button>
            
            <div className="sidebar__file-tools">
              <Button
                variant="secondary"
                size="medium"
                onClick={handleExport}
                className="sidebar__tool-btn"
              >
                Exportar
              </Button>
              
              <div className="sidebar__import-wrapper">
                <input
                  type="file"
                  accept=".json"
                  onChange={handleImport}
                  className="sidebar__import-input"
                  id="import-file"
                />
                <label htmlFor="import-file" className="sidebar__import-label">
                  <Button
                    variant="secondary"
                    size="medium"
                    as="span"
                    className="sidebar__tool-btn"
                  >
                    Importar
                  </Button>
                </label>
              </div>
            </div>
          </div>
        </section>
      </div>

      <div className="sidebar__footer">
        <div className="sidebar__status">
          <div className="sidebar__status-item">
            <span className="sidebar__status-label">Estado:</span>
            <span className="sidebar__status-value">
              {currentOperation ? `Operando (${currentOperation})` : 'Esperando entrada'}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
