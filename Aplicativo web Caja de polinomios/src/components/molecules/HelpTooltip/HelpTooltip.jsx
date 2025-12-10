import React, { useState, useRef, useEffect } from 'react';
import Button from '../../atoms/Button/Button';
import './HelpTooltip.css';

const HelpTooltip = ({ 
  title,
  content,
  children,
  position = 'top',
  trigger = 'hover', // 'hover', 'click'
  className = ''
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [adjustedPosition, setAdjustedPosition] = useState(position);
  const tooltipRef = useRef(null);
  const triggerRef = useRef(null);

  // Ajustar posición basado en viewport
  useEffect(() => {
    if (!isVisible || !tooltipRef.current || !triggerRef.current) return;

    const tooltip = tooltipRef.current;
    const trigger = triggerRef.current;
    const triggerRect = trigger.getBoundingClientRect();
    const viewport = {
      width: window.innerWidth,
      height: window.innerHeight
    };

    // Esperar un frame para que el tooltip esté renderizado
    requestAnimationFrame(() => {
      const tooltipRect = tooltip.getBoundingClientRect();
      const margin = 20; // Margen de seguridad
      let newPosition = position;

      // Verificar colisiones con los bordes del viewport
      switch (position) {
        case 'top':
          if (triggerRect.top - tooltipRect.height < margin) {
            newPosition = 'bottom';
          }
          // Verificar también los lados
          if (triggerRect.left + tooltipRect.width / 2 > viewport.width - margin) {
            newPosition = 'left';
          } else if (triggerRect.right - tooltipRect.width / 2 < margin) {
            newPosition = 'right';
          }
          break;
          
        case 'bottom':
          if (triggerRect.bottom + tooltipRect.height > viewport.height - margin) {
            newPosition = 'top';
          }
          // Verificar también los lados
          if (triggerRect.left + tooltipRect.width / 2 > viewport.width - margin) {
            newPosition = 'left';
          } else if (triggerRect.right - tooltipRect.width / 2 < margin) {
            newPosition = 'right';
          }
          break;
          
        case 'left':
          if (triggerRect.left - tooltipRect.width < margin) {
            newPosition = 'right';
          }
          // Verificar también arriba/abajo
          if (triggerRect.top + tooltipRect.height / 2 > viewport.height - margin) {
            newPosition = 'top';
          } else if (triggerRect.bottom - tooltipRect.height / 2 < margin) {
            newPosition = 'bottom';
          }
          break;
          
        case 'right':
          if (triggerRect.right + tooltipRect.width > viewport.width - margin) {
            newPosition = 'left';
          }
          // Verificar también arriba/abajo
          if (triggerRect.top + tooltipRect.height / 2 > viewport.height - margin) {
            newPosition = 'top';
          } else if (triggerRect.bottom - tooltipRect.height / 2 < margin) {
            newPosition = 'bottom';
          }
          break;
      }

      // Verificación final: si la nueva posición también se sale, usar fallback
      if (newPosition !== position) {
        setAdjustedPosition(newPosition);
      } else {
        // Verificar si necesitamos un fallback centrado
        const wouldOverflow = 
          (newPosition === 'top' && triggerRect.top - tooltipRect.height < margin) ||
          (newPosition === 'bottom' && triggerRect.bottom + tooltipRect.height > viewport.height - margin) ||
          (newPosition === 'left' && triggerRect.left - tooltipRect.width < margin) ||
          (newPosition === 'right' && triggerRect.right + tooltipRect.width > viewport.width - margin);
          
        if (wouldOverflow && window.innerWidth > 768) {
          // En pantallas grandes, usar la mejor posición disponible
          const positions = ['bottom', 'top', 'right', 'left'];
          for (const pos of positions) {
            const wouldFit = 
              (pos === 'top' && triggerRect.top - tooltipRect.height >= margin) ||
              (pos === 'bottom' && triggerRect.bottom + tooltipRect.height <= viewport.height - margin) ||
              (pos === 'left' && triggerRect.left - tooltipRect.width >= margin) ||
              (pos === 'right' && triggerRect.right + tooltipRect.width <= viewport.width - margin);
              
            if (wouldFit) {
              setAdjustedPosition(pos);
              break;
            }
          }
        }
      }
    });
  }, [isVisible, position]);

  const handleMouseEnter = () => {
    if (trigger === 'hover') {
      setIsVisible(true);
    }
  };

  const handleMouseLeave = () => {
    if (trigger === 'hover') {
      setIsVisible(false);
    }
  };

  const handleClick = (e) => {
    if (trigger === 'click') {
      e.stopPropagation();
      setIsVisible(!isVisible);
    }
  };

  const handleClose = () => {
    setIsVisible(false);
  };

  // Cerrar tooltip al hacer clic fuera (solo para trigger='click')
  useEffect(() => {
    if (!isVisible || trigger !== 'click') return;

    const handleClickOutside = (event) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target) &&
          triggerRef.current && !triggerRef.current.contains(event.target)) {
        setIsVisible(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isVisible, trigger]);

  return (
    <div 
      className={`help-tooltip ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div 
        ref={triggerRef}
        className="help-tooltip__trigger"
        onClick={handleClick}
      >
        {children || (
          <Button
            variant="ghost"
            size="small"
            icon="?"
            className="help-tooltip__default-trigger"
            aria-label="Ayuda"
          />
        )}
      </div>

      {isVisible && (
        <>
          <div 
            ref={tooltipRef}
            className={`help-tooltip__content help-tooltip__content--${adjustedPosition}`}
          >
            <div className="help-tooltip__arrow"></div>
            
            {title && (
              <div className="help-tooltip__header">
                <h4 className="help-tooltip__title">{title}</h4>
                {trigger === 'click' && (
                  <Button
                    variant="ghost"
                    size="small"
                    icon="×"
                    onClick={handleClose}
                    className="help-tooltip__close"
                    aria-label="Cerrar ayuda"
                  />
                )}
              </div>
            )}
            
            <div className="help-tooltip__body">
              {typeof content === 'string' ? (
                <p>{content}</p>
              ) : (
                content
              )}
            </div>
          </div>
          
          {trigger === 'click' && (
            <div 
              className="help-tooltip__overlay"
              onClick={handleClose}
            />
          )}
        </>
      )}
    </div>
  );
};

// Componente especializado para ayuda matemática
export const MathHelpTooltip = ({ operation, step, ...props }) => {
  const getHelpContent = () => {
    const helpData = {
      addition: {
        1: {
          title: "Paso 1: Preparación del Plano",
          content: (
            <div>
              <p>Divide los cuadrantes del plano cartesiano por signos:</p>
              <ul>
                <li><strong>Cuadrante I (++):</strong> Términos positivos</li>
                <li><strong>Cuadrante II (-+):</strong> Términos negativos</li>
                <li><strong>Cuadrante III (--):</strong> Términos negativos</li>
                <li><strong>Cuadrante IV (+-):</strong> Términos positivos</li>
              </ul>
            </div>
          )
        },
        2: {
          title: "Paso 2: Ubicar Primer Polinomio",
          content: "Coloca las fichas del primer polinomio P(x) en los cuadrantes superiores según el signo de cada término."
        },
        // ... más pasos
      },
      // ... más operaciones
    };

    return helpData[operation]?.[step] || {
      title: "Ayuda",
      content: "Información de ayuda no disponible para este paso."
    };
  };

  const helpContent = getHelpContent();

  return (
    <HelpTooltip
      title={helpContent.title}
      content={helpContent.content}
      {...props}
    />
  );
};

export default HelpTooltip;
