import React, { useState } from 'react';
import Button from '../../atoms/Button/Button';
import HelpTooltip from '../../molecules/HelpTooltip/HelpTooltip';
import { useApp } from '../../../contexts/AppContext';
import './Navbar.css';

const Navbar = ({ className = '' }) => {
  const { state, actions } = useApp();
  const { ui } = state;
  const [showFiguresPanel, setShowFiguresPanel] = useState(false);

  const predefinedFigures = [
    {
      id: 'x2',
      name: 'x²',
      description: 'Término cuadrático',
      color: '#2563eb'
    },
    {
      id: 'x',
      name: 'x',
      description: 'Término lineal',
      color: '#10b981'
    },
    {
      id: 'constant',
      name: '1',
      description: 'Término constante',
      color: '#f59e0b'
    }
  ];

  const handleAddFigure = (figure) => {
    const chip = {
      id: Date.now(),
      type: figure.id,
      label: figure.name,
      x: Math.random() * 200 - 100,
      y: Math.random() * 200 - 100,
      size: 40,
      color: figure.color
    };
    
    actions.addChip(chip);
    setShowFiguresPanel(false);
  };

  const handleReset = () => {
    if (window.confirm('¿Estás seguro de que quieres reiniciar todo?')) {
      actions.setPolynomial('first', '');
      actions.setPolynomial('second', '');
      actions.setOperation(null);
      actions.setResult(null);
      actions.setStepByStep([]);
      actions.clearPlane();
      actions.setZoom(1);
      actions.setPan(0, 0);
    }
  };

  return (
    <nav className={`navbar ${className}`}>
      <div className="navbar__container">
        {/* Logo y título */}
        <div className="navbar__brand">
          <div className="navbar__logo">
            📦
          </div>
          <h1 className="navbar__title">
            Caja de Polinomios
          </h1>
        </div>

        {/* Controles principales */}
        <div className="navbar__controls">
          {/* Toggle sidebar */}
          <Button
            variant={ui.sidebarVisible ? 'primary' : 'outline'}
            size="medium"
            icon="☰"
            onClick={actions.toggleSidebar}
            className="navbar__control-btn"
            aria-label={ui.sidebarVisible ? 'Ocultar panel' : 'Mostrar panel'}
          />

          {/* Banco de figuras */}
          <div className="navbar__figures-wrapper">
            <Button
              variant="outline"
              size="medium"
              onClick={() => setShowFiguresPanel(!showFiguresPanel)}
              className="navbar__control-btn"
              icon="🔧"
            >
              Figuras
            </Button>
            
            {showFiguresPanel && (
              <div className="figures-panel">
                <div className="figures-panel__header">
                  <h3 className="figures-panel__title">
                    Banco de Figuras
                  </h3>
                  <Button
                    variant="ghost"
                    size="small"
                    icon="×"
                    onClick={() => setShowFiguresPanel(false)}
                    aria-label="Cerrar panel de figuras"
                  />
                </div>
                
                <div className="figures-panel__content">
                  {predefinedFigures.map(figure => (
                    <button
                      key={figure.id}
                      className="figure-item"
                      onClick={() => handleAddFigure(figure)}
                      style={{ borderColor: figure.color }}
                    >
                      <div 
                        className="figure-item__icon"
                        style={{ backgroundColor: figure.color }}
                      >
                        {figure.name}
                      </div>
                      <div className="figure-item__info">
                        <span className="figure-item__name">
                          {figure.name}
                        </span>
                        <span className="figure-item__description">
                          {figure.description}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Zoom controls */}
          <div className="navbar__zoom-controls">
            <Button
              variant="ghost"
              size="small"
              icon="+"
              onClick={() => actions.setZoom(Math.min(state.plane.zoom * 1.2, 3))}
              aria-label="Aumentar zoom"
            />
            <span className="navbar__zoom-display">
              {Math.round(state.plane.zoom * 100)}%
            </span>
            <Button
              variant="ghost"
              size="small"
              icon="−"
              onClick={() => actions.setZoom(Math.max(state.plane.zoom * 0.8, 0.3))}
              aria-label="Reducir zoom"
            />
          </div>

          {/* Reset button */}
          <Button
            variant="outline"
            size="medium"
            onClick={handleReset}
            className="navbar__control-btn"
            icon="↻"
          >
            Reset
          </Button>
        </div>

        {/* Ayuda */}
        <div className="navbar__help">
          <HelpTooltip
            title="Guía Rápida"
            trigger="click"
            position="bottom"
            content={(
              <div className="help-content">
                <h4>Controles Principales:</h4>
                <ul>
                  <li><strong>Panel:</strong> Mostrar/ocultar sidebar</li>
                  <li><strong>Figuras:</strong> Agregar fichas al plano</li>
                  <li><strong>Zoom:</strong> Ajustar vista del plano</li>
                  <li><strong>Reset:</strong> Reiniciar todo</li>
                </ul>
                
                <h4>Operaciones:</h4>
                <ul>
                  <li><strong>Suma:</strong> Mover fichas diagonalmente</li>
                  <li><strong>Resta:</strong> Cambiar de lado las fichas</li>
                  <li><strong>Multiplicación:</strong> Formar rectángulos</li>
                  <li><strong>División:</strong> Construir con base conocida</li>
                </ul>
                
                <h4>Atajos de Teclado:</h4>
                <ul>
                  <li><strong>R:</strong> Reset zoom y pan</li>
                  <li><strong>C:</strong> Limpiar plano</li>
                  <li><strong>H:</strong> Mostrar/ocultar ayuda</li>
                </ul>
              </div>
            )}
          >
            <Button
              variant="primary"
              size="medium"
              icon="?"
              className="navbar__help-btn"
            >
              Ayuda
            </Button>
          </HelpTooltip>
        </div>
      </div>

      {/* Overlay para cerrar panel de figuras */}
      {showFiguresPanel && (
        <div 
          className="figures-panel-overlay"
          onClick={() => setShowFiguresPanel(false)}
        />
      )}
    </nav>
  );
};

export default Navbar;
