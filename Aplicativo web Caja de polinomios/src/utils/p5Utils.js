// Utilidades específicas para p5.js

// Función para convertir coordenadas del canvas a coordenadas matemáticas
export const canvasToMath = (canvasX, canvasY, canvasWidth, canvasHeight, zoom = 1, panX = 0, panY = 0) => {
  const centerX = canvasWidth / 2;
  const centerY = canvasHeight / 2;
  
  const mathX = ((canvasX - centerX - panX) / zoom) / 20; // 20 pixels por unidad
  const mathY = -((canvasY - centerY - panY) / zoom) / 20; // Invertir Y para matemáticas
  
  return { x: mathX, y: mathY };
};

// Función para convertir coordenadas matemáticas a coordenadas del canvas
export const mathToCanvas = (mathX, mathY, canvasWidth, canvasHeight, zoom = 1, panX = 0, panY = 0) => {
  const centerX = canvasWidth / 2;
  const centerY = canvasHeight / 2;
  
  const canvasX = centerX + (mathX * 20 * zoom) + panX;
  const canvasY = centerY - (mathY * 20 * zoom) + panY; // Invertir Y
  
  return { x: canvasX, y: canvasY };
};

// Crear ficha de polinomio
export const createPolynomialChip = (term, position = { x: 0, y: 0 }) => {
  const chip = {
    id: Date.now() + Math.random(),
    type: getChipType(term),
    label: formatTermLabel(term),
    coefficient: term.coefficient,
    variable: term.variable,
    exponent: term.exponent,
    x: position.x,
    y: position.y,
    size: getChipSize(term),
    color: getChipColor(term),
    isSelected: false,
    isDragging: false,
    createdAt: Date.now()
  };
  
  return chip;
};

// Determinar tipo de ficha basado en el término
const getChipType = (term) => {
  if (term.exponent === 0) return 'constant';
  if (term.exponent === 1) return 'x';
  if (term.exponent === 2) return 'x2';
  return 'polynomial';
};

// Formatear etiqueta de la ficha
const formatTermLabel = (term) => {
  if (term.exponent === 0) {
    return term.coefficient.toString();
  }
  
  const coeff = Math.abs(term.coefficient) === 1 ? '' : Math.abs(term.coefficient);
  const sign = term.coefficient < 0 ? '-' : '';
  
  if (term.exponent === 1) {
    return `${sign}${coeff}${term.variable}`;
  }
  
  return `${sign}${coeff}${term.variable}²`;
};

// Obtener tamaño de ficha
const getChipSize = (term) => {
  if (term.exponent === 0) return 30; // Constantes más pequeñas
  if (term.exponent === 1) return 40; // Lineales medianas
  if (term.exponent === 2) return 50; // Cuadráticas más grandes
  return 35;
};

// Obtener color de ficha
const getChipColor = (term) => {
  const colors = {
    constant: '#f59e0b', // Orange
    x: '#10b981',        // Green
    x2: '#2563eb',       // Blue
    polynomial: '#8b5cf6' // Purple
  };
  
  return colors[getChipType(term)] || '#6b7280';
};

// Determinar cuadrante basado en coordenadas
export const getQuadrant = (x, y) => {
  if (x >= 0 && y >= 0) return 1; // I
  if (x < 0 && y >= 0) return 2;  // II
  if (x < 0 && y < 0) return 3;   // III
  if (x >= 0 && y < 0) return 4;  // IV
  return 0; // En los ejes
};

// Verificar si un punto está dentro de una ficha
export const isPointInChip = (pointX, pointY, chip) => {
  const distance = Math.sqrt(
    Math.pow(pointX - chip.x, 2) + Math.pow(pointY - chip.y, 2)
  );
  return distance <= chip.size / 2;
};

// Calcular posición inicial para fichas según la operación
export const calculateInitialPositions = (polynomial, operation, isFirst = true) => {
  const positions = [];
  const terms = polynomial.terms;
  
  switch (operation) {
    case 'addition':
    case 'subtraction':
      // Para suma/resta: primer polinomio arriba, segundo abajo
      const yOffset = isFirst ? -100 : 100;
      terms.forEach((term, index) => {
        const x = (index - terms.length / 2) * 80;
        const y = yOffset;
        positions.push({ x, y });
      });
      break;
      
    case 'multiplication':
      // Para multiplicación: formar base y altura
      if (isFirst) {
        // Base horizontal
        terms.forEach((term, index) => {
          const x = (index - terms.length / 2) * 60;
          const y = 0;
          positions.push({ x, y });
        });
      } else {
        // Altura vertical
        terms.forEach((term, index) => {
          const x = -120;
          const y = (index - terms.length / 2) * 60;
          positions.push({ x, y });
        });
      }
      break;
      
    case 'division':
      // Para división: dividendo distribuido, divisor como base
      if (isFirst) {
        // Dividendo distribuido en cuadrantes superiores
        terms.forEach((term, index) => {
          const x = (index - terms.length / 2) * 70;
          const y = -80;
          positions.push({ x, y });
        });
      } else {
        // Divisor como base
        terms.forEach((term, index) => {
          const x = (index - terms.length / 2) * 50;
          const y = 80;
          positions.push({ x, y });
        });
      }
      break;
      
    default:
      // Posición por defecto
      terms.forEach((term, index) => {
        const x = (index - terms.length / 2) * 60;
        const y = isFirst ? -50 : 50;
        positions.push({ x, y });
      });
  }
  
  return positions;
};

// Animar movimiento de ficha
export const animateChipMovement = (chip, targetX, targetY, duration = 1000) => {
  const startX = chip.x;
  const startY = chip.y;
  const startTime = Date.now();
  
  return new Promise((resolve) => {
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Función de easing (ease-out)
      const easeOut = 1 - Math.pow(1 - progress, 3);
      
      chip.x = startX + (targetX - startX) * easeOut;
      chip.y = startY + (targetY - startY) * easeOut;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        chip.x = targetX;
        chip.y = targetY;
        resolve();
      }
    };
    
    animate();
  });
};

// Detectar colisiones entre fichas
export const detectCollisions = (chips) => {
  const collisions = [];
  
  for (let i = 0; i < chips.length; i++) {
    for (let j = i + 1; j < chips.length; j++) {
      const chip1 = chips[i];
      const chip2 = chips[j];
      
      const distance = Math.sqrt(
        Math.pow(chip1.x - chip2.x, 2) + Math.pow(chip1.y - chip2.y, 2)
      );
      
      const minDistance = (chip1.size + chip2.size) / 2;
      
      if (distance < minDistance) {
        collisions.push({ chip1, chip2, distance });
      }
    }
  }
  
  return collisions;
};

// Resolver colisiones moviendo fichas
export const resolveCollisions = (collisions) => {
  collisions.forEach(({ chip1, chip2, distance }) => {
    const minDistance = (chip1.size + chip2.size) / 2 + 5; // +5 para espacio
    const overlap = minDistance - distance;
    
    if (overlap > 0) {
      const angle = Math.atan2(chip2.y - chip1.y, chip2.x - chip1.x);
      const moveDistance = overlap / 2;
      
      chip1.x -= Math.cos(angle) * moveDistance;
      chip1.y -= Math.sin(angle) * moveDistance;
      chip2.x += Math.cos(angle) * moveDistance;
      chip2.y += Math.sin(angle) * moveDistance;
    }
  });
};

// Agrupar fichas similares
export const groupSimilarChips = (chips) => {
  const groups = {};
  
  chips.forEach(chip => {
    const key = `${chip.variable}_${chip.exponent}`;
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(chip);
  });
  
  return groups;
};

// Combinar fichas similares en una sola
export const combineSimilarChips = (chipGroup) => {
  if (chipGroup.length <= 1) return chipGroup;
  
  const combined = { ...chipGroup[0] };
  combined.coefficient = chipGroup.reduce((sum, chip) => sum + chip.coefficient, 0);
  combined.label = formatTermLabel(combined);
  combined.id = Date.now() + Math.random();
  
  // Posición promedio
  combined.x = chipGroup.reduce((sum, chip) => sum + chip.x, 0) / chipGroup.length;
  combined.y = chipGroup.reduce((sum, chip) => sum + chip.y, 0) / chipGroup.length;
  
  return combined.coefficient === 0 ? null : combined;
};

// Aplicar efecto visual a ficha
export const applyChipEffect = (p5, chip, effect) => {
  p5.push();
  p5.translate(chip.x, chip.y);
  
  switch (effect) {
    case 'highlight':
      p5.stroke(255, 255, 0);
      p5.strokeWeight(3);
      p5.noFill();
      p5.circle(0, 0, chip.size + 10);
      break;
      
    case 'pulse':
      const pulse = Math.sin(Date.now() * 0.01) * 5;
      p5.scale(1 + pulse * 0.1);
      break;
      
    case 'fade':
      p5.tint(255, 128);
      break;
      
    case 'error':
      p5.stroke(255, 0, 0);
      p5.strokeWeight(2);
      p5.noFill();
      for (let i = 0; i < 3; i++) {
        p5.circle(0, 0, chip.size + i * 5);
      }
      break;
  }
  
  p5.pop();
};

// Utilidades de dibujo matemático
export const drawMathSymbol = (p5, symbol, x, y, size = 16) => {
  p5.push();
  p5.translate(x, y);
  p5.textAlign(p5.CENTER, p5.CENTER);
  p5.textSize(size);
  p5.fill(0);
  p5.text(symbol, 0, 0);
  p5.pop();
};

export default {
  canvasToMath,
  mathToCanvas,
  createPolynomialChip,
  getQuadrant,
  isPointInChip,
  calculateInitialPositions,
  animateChipMovement,
  detectCollisions,
  resolveCollisions,
  groupSimilarChips,
  combineSimilarChips,
  applyChipEffect,
  drawMathSymbol
};
