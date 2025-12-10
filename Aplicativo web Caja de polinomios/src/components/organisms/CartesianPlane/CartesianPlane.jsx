import React, { useRef, useEffect, useState } from 'react';
import Sketch from 'react-p5';
import { useApp } from '../../../contexts/AppContext';
import './CartesianPlane.css';

const CartesianPlane = ({ className = '' }) => {
  const { state, actions } = useApp();
  const { plane } = state;
  const sketchRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  // Configuración del plano
  const config = {
    width: dimensions.width,
    height: dimensions.height,
    gridSize: Math.max(20, Math.min(40, dimensions.width / 20)), // Grilla adaptativa
    axisColor: [55, 65, 81], // gray-700
    gridColor: [229, 231, 235], // gray-200
    positiveColor: [16, 185, 129], // success-color
    negativeColor: [239, 68, 68], // error-color
  };

  // Effect para redimensionar el canvas cuando cambie el contenedor
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setDimensions({
          width: rect.width || 800,
          height: rect.height || 600
        });
      }
    };

    // Actualizar dimensiones iniciales
    updateDimensions();

    // Agregar listener para resize
    window.addEventListener('resize', updateDimensions);
    
    // Observer para cambios en el contenedor
    const resizeObserver = new ResizeObserver(updateDimensions);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      window.removeEventListener('resize', updateDimensions);
      resizeObserver.disconnect();
    };
  }, []);

  const setup = (p5, canvasParentRef) => {
    const canvas = p5.createCanvas(config.width, config.height);
    canvas.parent(canvasParentRef);
    p5.background(255);
    
    // Configurar el canvas para que sea responsivo
    canvas.style('width', '100%');
    canvas.style('height', '100%');
    canvas.style('display', 'block');
  };

  // Effect para redimensionar el canvas cuando cambien las dimensiones
  useEffect(() => {
    if (sketchRef.current && sketchRef.current.resizeCanvas) {
      sketchRef.current.resizeCanvas(config.width, config.height);
    }
  }, [config.width, config.height]);

  const draw = (p5) => {
    p5.background(255);
    
    // Dibujar elementos del plano infinito
    drawGrid(p5);
    drawAxes(p5);
    drawQuadrants(p5);
    
    // Aplicar transformaciones solo para las fichas de polinomios
    p5.push();
    p5.translate(config.width / 2 + plane.panX, config.height / 2 + plane.panY);
    p5.scale(plane.zoom);
    drawPolynomialChips(p5);
    p5.pop();
    
    // Dibujar controles de zoom (sin transformaciones)
    drawZoomControls(p5);
    
    // Dibujar información del estado (sin transformaciones)
    drawStateInfo(p5);
  };

  const drawGrid = (p5) => {
    p5.stroke(...config.gridColor);
    p5.strokeWeight(1);
    
    const halfWidth = config.width / 2;
    const halfHeight = config.height / 2;
    
    // Calcular el tamaño efectivo de la grilla
    const effectiveGridSize = config.gridSize;
    
    // Calcular cuántas líneas necesitamos en cada dirección
    const linesX = Math.ceil(config.width / effectiveGridSize) + 2;
    const linesY = Math.ceil(config.height / effectiveGridSize) + 2;
    
    // Calcular el offset basado en el pan
    const offsetX = (plane.panX % effectiveGridSize);
    const offsetY = (plane.panY % effectiveGridSize);
    
    // Dibujar líneas verticales
    for (let i = -1; i <= linesX; i++) {
      const x = i * effectiveGridSize + offsetX;
      if (x >= 0 && x <= config.width) {
        p5.line(x, 0, x, config.height);
      }
    }
    
    // Dibujar líneas horizontales
    for (let i = -1; i <= linesY; i++) {
      const y = i * effectiveGridSize + offsetY;
      if (y >= 0 && y <= config.height) {
        p5.line(0, y, config.width, y);
      }
    }
  };

  const drawAxes = (p5) => {
    p5.stroke(...config.axisColor);
    p5.strokeWeight(3);
    
    // Calcular la posición del origen en coordenadas de pantalla
    const originX = config.width / 2 + plane.panX;
    const originY = config.height / 2 + plane.panY;
    
    // Dibujar eje X (horizontal) - siempre visible si el Y=0 está en pantalla
    if (originY >= -5 && originY <= config.height + 5) {
      const clampedY = Math.max(0, Math.min(originY, config.height));
      p5.line(0, clampedY, config.width, clampedY);
      
      // Flecha derecha del eje X
      if (config.width > 30) {
        drawArrow(p5, config.width - 15, clampedY, config.width - 5, clampedY);
      }
      
      // Etiqueta X
      if (config.width > 50 && clampedY > 20 && clampedY < config.height - 20) {
        p5.fill(...config.axisColor);
        p5.noStroke();
        p5.textAlign(p5.CENTER, p5.CENTER);
        p5.textSize(16);
        p5.text('X', config.width - 25, clampedY + 20);
      }
    }
    
    // Dibujar eje Y (vertical) - siempre visible si el X=0 está en pantalla
    if (originX >= -5 && originX <= config.width + 5) {
      const clampedX = Math.max(0, Math.min(originX, config.width));
      p5.line(clampedX, 0, clampedX, config.height);
      
      // Flecha arriba del eje Y
      if (config.height > 30) {
        drawArrow(p5, clampedX, 15, clampedX, 5);
      }
      
      // Etiqueta Y
      if (config.height > 50 && clampedX > 20 && clampedX < config.width - 20) {
        p5.fill(...config.axisColor);
        p5.noStroke();
        p5.textAlign(p5.CENTER, p5.CENTER);
        p5.textSize(16);
        p5.text('Y', clampedX + 20, 25);
      }
    }
    
    // Dibujar números en los ejes si están visibles
    drawAxisNumbers(p5);
  };

  const drawArrow = (p5, x1, y1, x2, y2) => {
    p5.line(x1, y1, x2, y2);
    
    const angle = Math.atan2(y2 - y1, x2 - x1);
    const arrowLength = 8;
    
    p5.line(
      x2,
      y2,
      x2 - arrowLength * Math.cos(angle - Math.PI / 6),
      y2 - arrowLength * Math.sin(angle - Math.PI / 6)
    );
    
    p5.line(
      x2,
      y2,
      x2 - arrowLength * Math.cos(angle + Math.PI / 6),
      y2 - arrowLength * Math.sin(angle + Math.PI / 6)
    );
  };

  const drawAxisNumbers = (p5) => {
    const originX = config.width / 2 + plane.panX;
    const originY = config.height / 2 + plane.panY;
    const effectiveGridSize = config.gridSize * plane.zoom;
    
    p5.fill(...config.axisColor);
    p5.noStroke();
    p5.textAlign(p5.CENTER, p5.CENTER);
    p5.textSize(Math.max(10, Math.min(14, 12 * plane.zoom)));
    
    // Números en el eje X (si el eje Y está visible o cerca)
    if (originY >= -20 && originY <= config.height + 20 && effectiveGridSize > 15) {
      const clampedY = Math.max(15, Math.min(originY + 15, config.height - 5));
      const startNum = Math.floor(-originX / effectiveGridSize);
      const endNum = Math.ceil((config.width - originX) / effectiveGridSize);
      
      for (let i = startNum; i <= endNum; i++) {
        if (i !== 0) { // No dibujar el 0
          const x = originX + i * effectiveGridSize;
          if (x >= 10 && x <= config.width - 10) {
            p5.text(i.toString(), x, clampedY);
          }
        }
      }
    }
    
    // Números en el eje Y (si el eje X está visible o cerca)
    if (originX >= -20 && originX <= config.width + 20 && effectiveGridSize > 15) {
      const clampedX = Math.max(15, Math.min(originX - 15, config.width - 15));
      const startNum = Math.floor((config.height - originY) / effectiveGridSize);
      const endNum = Math.ceil(-originY / effectiveGridSize);
      
      for (let i = startNum; i >= endNum; i--) {
        if (i !== 0) { // No dibujar el 0
          const y = originY - i * effectiveGridSize;
          if (y >= 10 && y <= config.height - 10) {
            p5.text(i.toString(), clampedX, y);
          }
        }
      }
    }
    
    // Dibujar el origen (0,0) si está visible o cerca
    if (originX >= -20 && originX <= config.width + 20 && 
        originY >= -20 && originY <= config.height + 20) {
      const labelX = Math.max(10, Math.min(originX - 10, config.width - 20));
      const labelY = Math.max(15, Math.min(originY + 15, config.height - 5));
      p5.text('0', labelX, labelY);
    }
  };

  const drawQuadrants = (p5) => {
    const originX = config.width / 2 + plane.panX;
    const originY = config.height / 2 + plane.panY;
    
    // Solo dibujar cuadrantes si el origen está visible o cerca
    if (originX >= -50 && originX <= config.width + 50 && 
        originY >= -50 && originY <= config.height + 50) {
      
      // Cuadrante I (x > 0, y < 0) - positivo (arriba derecha)
      if (originX < config.width && originY > 0) {
        p5.fill(16, 185, 129, 15);
        p5.noStroke();
        p5.rect(
          Math.max(originX, 0), 
          0, 
          Math.min(config.width - originX, config.width), 
          Math.min(originY, config.height)
        );
      }
      
      // Cuadrante II (x < 0, y < 0) - negativo (arriba izquierda)
      if (originX > 0 && originY > 0) {
        p5.fill(239, 68, 68, 15);
        p5.rect(
          0, 
          0, 
          Math.min(originX, config.width), 
          Math.min(originY, config.height)
        );
      }
      
      // Cuadrante III (x < 0, y > 0) - positivo (abajo izquierda)
      if (originX > 0 && originY < config.height) {
        p5.fill(16, 185, 129, 15);
        p5.rect(
          0, 
          Math.max(originY, 0), 
          Math.min(originX, config.width), 
          Math.min(config.height - originY, config.height)
        );
      }
      
      // Cuadrante IV (x > 0, y > 0) - negativo (abajo derecha)
      if (originX < config.width && originY < config.height) {
        p5.fill(239, 68, 68, 15);
        p5.rect(
          Math.max(originX, 0), 
          Math.max(originY, 0), 
          Math.min(config.width - originX, config.width), 
          Math.min(config.height - originY, config.height)
        );
      }
      
      // Etiquetas de cuadrantes (solo si hay suficiente espacio y están visibles)
      if (plane.zoom > 0.3) {
        p5.fill(55, 65, 81);
        p5.textAlign(p5.CENTER, p5.CENTER);
        p5.textSize(Math.max(10, 12 * plane.zoom));
        
        const labelOffset = Math.max(30, 50 * plane.zoom);
        
        // Cuadrante I (arriba derecha)
        if (originX + labelOffset <= config.width && originY - labelOffset >= 0) {
          p5.text('I (+)', originX + labelOffset, originY - labelOffset);
        }
        
        // Cuadrante II (arriba izquierda)
        if (originX - labelOffset >= 0 && originY - labelOffset >= 0) {
          p5.text('II (-)', originX - labelOffset, originY - labelOffset);
        }
        
        // Cuadrante III (abajo izquierda)
        if (originX - labelOffset >= 0 && originY + labelOffset <= config.height) {
          p5.text('III (+)', originX - labelOffset, originY + labelOffset);
        }
        
        // Cuadrante IV (abajo derecha)
        if (originX + labelOffset <= config.width && originY + labelOffset <= config.height) {
          p5.text('IV (-)', originX + labelOffset, originY + labelOffset);
        }
      }
    }
  };

  const drawPolynomialChips = (p5) => {
    plane.chips.forEach(chip => {
      drawChip(p5, chip);
    });
  };

  const drawChip = (p5, chip) => {
    p5.push();
    p5.translate(chip.x, chip.y);
    
    // Color según el tipo de ficha
    const colors = {
      'x2': [37, 99, 235], // primary-color
      'x': [16, 185, 129], // success-color
      'constant': [249, 115, 22], // orange
    };
    
    const color = colors[chip.type] || [107, 114, 128];
    
    // Dibujar ficha
    p5.fill(...color, 180);
    p5.stroke(255);
    p5.strokeWeight(2);
    
    if (chip.type === 'x2') {
      // Cuadrado para x²
      p5.rect(-chip.size/2, -chip.size/2, chip.size, chip.size);
    } else if (chip.type === 'x') {
      // Rectángulo para x
      p5.rect(-chip.size/2, -chip.size/4, chip.size, chip.size/2);
    } else {
      // Círculo pequeño para constantes
      p5.circle(0, 0, chip.size/2);
    }
    
    // Etiqueta de la ficha
    p5.fill(255);
    p5.noStroke();
    p5.textAlign(p5.CENTER, p5.CENTER);
    p5.textSize(12);
    p5.text(chip.label, 0, 0);
    
    p5.pop();
  };

  const drawZoomControls = (p5) => {
    // Botones de zoom en la esquina superior derecha
    const x = config.width - 60;
    const y = 20;
    
    // Solo mostrar controles si hay suficiente espacio
    if (config.width > 120 && config.height > 100) {
      // Zoom in
      p5.fill(255);
      p5.stroke(200);
      p5.strokeWeight(1);
      p5.rect(x, y, 30, 30);
      p5.fill(0);
      p5.noStroke();
      p5.textAlign(p5.CENTER, p5.CENTER);
      p5.textSize(16);
      p5.text('+', x + 15, y + 15);
      
      // Zoom out
      p5.fill(255);
      p5.stroke(200);
      p5.strokeWeight(1);
      p5.rect(x, y + 35, 30, 30);
      p5.fill(0);
      p5.noStroke();
      p5.text('-', x + 15, y + 50);
    }
  };

  const drawStateInfo = (p5) => {
    // Información del estado actual en la esquina superior izquierda
    // Solo mostrar si hay suficiente espacio
    if (config.width > 250 && config.height > 120) {
      p5.fill(255, 255, 255, 200);
      p5.noStroke();
      p5.rect(10, 10, 220, 100, 5);
      
      p5.fill(0);
      p5.textAlign(p5.LEFT, p5.TOP);
      p5.textSize(12);
      
      let y = 20;
      p5.text(`Zoom: ${(plane.zoom * 100).toFixed(0)}%`, 15, y);
      y += 15;
      
      // Mostrar coordenadas del centro visible
      const centerX = (-plane.panX / config.gridSize).toFixed(1);
      const centerY = (plane.panY / config.gridSize).toFixed(1);
      p5.text(`Centro: (${centerX}, ${centerY})`, 15, y);
      y += 15;
      
      p5.text(`Fichas: ${plane.chips.length}`, 15, y);
      y += 15;
      p5.text(`Operación: ${state.currentOperation || 'Ninguna'}`, 15, y);
      y += 15;
      
      // Mostrar rango visible
      const rangeX = (config.width / (config.gridSize * 2)).toFixed(1);
      const rangeY = (config.height / (config.gridSize * 2)).toFixed(1);
      p5.text(`Rango: ±${rangeX}x, ±${rangeY}y`, 15, y);
    }
  };

  const mousePressed = (p5) => {
    // Manejar clics en controles de zoom (solo si son visibles)
    if (config.width > 120 && config.height > 100) {
      const x = config.width - 60;
      const y = 20;
      
      if (p5.mouseX >= x && p5.mouseX <= x + 30) {
        if (p5.mouseY >= y && p5.mouseY <= y + 30) {
          // Zoom in
          actions.setZoom(Math.min(plane.zoom * 1.2, 3));
        } else if (p5.mouseY >= y + 35 && p5.mouseY <= y + 65) {
          // Zoom out
          actions.setZoom(Math.max(plane.zoom * 0.8, 0.3));
        }
      }
    }
  };

  const mouseDragged = (p5) => {
    // Pan del plano
    const controlsWidth = config.width > 120 ? 100 : 0;
    if (p5.mouseX < config.width - controlsWidth) { // No interferir con controles
      const deltaX = p5.mouseX - p5.pmouseX;
      const deltaY = p5.mouseY - p5.pmouseY;
      actions.setPan(plane.panX + deltaX, plane.panY + deltaY);
    }
  };

  const keyPressed = (p5) => {
    const stepSize = config.gridSize * plane.zoom;
    
    // Controles de teclado
    if (p5.key === 'r' || p5.key === 'R') {
      // Reset zoom y pan (volver al origen)
      actions.setZoom(1);
      actions.setPan(0, 0);
    } else if (p5.key === 'c' || p5.key === 'C') {
      // Limpiar plano
      actions.clearPlane();
    } else if (p5.key === '+' || p5.key === '=') {
      // Zoom in con teclado
      actions.setZoom(Math.min(plane.zoom * 1.2, 5));
    } else if (p5.key === '-' || p5.key === '_') {
      // Zoom out con teclado
      actions.setZoom(Math.max(plane.zoom * 0.8, 0.1));
    }
    
    // Navegación con flechas
    if (p5.keyCode === p5.UP_ARROW) {
      actions.setPan(plane.panX, plane.panY + stepSize);
    } else if (p5.keyCode === p5.DOWN_ARROW) {
      actions.setPan(plane.panX, plane.panY - stepSize);
    } else if (p5.keyCode === p5.LEFT_ARROW) {
      actions.setPan(plane.panX + stepSize, plane.panY);
    } else if (p5.keyCode === p5.RIGHT_ARROW) {
      actions.setPan(plane.panX - stepSize, plane.panY);
    }
  };

  const windowResized = (p5) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const newWidth = rect.width || 800;
      const newHeight = rect.height || 600;
      
      p5.resizeCanvas(newWidth, newHeight);
      setDimensions({ width: newWidth, height: newHeight });
    }
  };

  return (
    <div className={`cartesian-plane ${className}`}>
      <div 
        className="cartesian-plane__canvas"
        ref={containerRef}
      >
        <Sketch
          ref={sketchRef}
          setup={setup}
          draw={draw}
          mousePressed={mousePressed}
          mouseDragged={mouseDragged}
          keyPressed={keyPressed}
          windowResized={windowResized}
        />
      </div>
      
      <div className="cartesian-plane__controls">
        <div className="cartesian-plane__help">
          <p><strong>Controles del Plano Infinito:</strong></p>
          <ul>
            <li>🖱️ Arrastra para navegar por el plano</li>
            <li>➕➖ Botones para zoom in/out</li>
            <li>⌨️ +/- en teclado para zoom</li>
            <li>🏠 Tecla 'R' para volver al origen (0,0)</li>
            <li>🧹 Tecla 'C' para limpiar fichas</li>
            <li>⬅️➡️⬆️⬇️ Flechas para navegación precisa</li>
            <li>🧭 El plano se extiende infinitamente en todas las direcciones</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CartesianPlane;
