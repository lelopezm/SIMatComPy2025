import React, { createContext, useContext, useReducer } from 'react';

// Tipos de acciones
const ActionTypes = {
  SET_POLYNOMIAL: 'SET_POLYNOMIAL',
  SET_OPERATION: 'SET_OPERATION',
  SET_RESULT: 'SET_RESULT',
  SET_STEP_BY_STEP: 'SET_STEP_BY_STEP',
  SET_SIDEBAR_VISIBLE: 'SET_SIDEBAR_VISIBLE',
  SET_HELP_VISIBLE: 'SET_HELP_VISIBLE',
  SET_ZOOM: 'SET_ZOOM',
  SET_PAN: 'SET_PAN',
  ADD_POLYNOMIAL_CHIP: 'ADD_POLYNOMIAL_CHIP',
  REMOVE_POLYNOMIAL_CHIP: 'REMOVE_POLYNOMIAL_CHIP',
  CLEAR_PLANE: 'CLEAR_PLANE',
  SET_CURRENT_STEP: 'SET_CURRENT_STEP'
};

// Estado inicial
const initialState = {
  // Polinomios
  polynomials: {
    first: '',
    second: ''
  },
  
  // Operación actual
  currentOperation: null, // 'addition', 'subtraction', 'multiplication', 'division'
  
  // Resultado
  result: null,
  
  // Pasos de resolución
  stepByStep: [],
  currentStep: 0,
  
  // UI State
  ui: {
    sidebarVisible: true,
    helpVisible: false,
    currentView: 'input' // 'input', 'steps', 'result'
  },
  
  // Plano cartesiano
  plane: {
    zoom: 1,
    panX: 0,
    panY: 0,
    chips: []
  },
  
  // Configuraciones
  settings: {
    showGrid: true,
    showAxes: true,
    animationSpeed: 1
  }
};

// Reducer
function appReducer(state, action) {
  switch (action.type) {
    case ActionTypes.SET_POLYNOMIAL:
      return {
        ...state,
        polynomials: {
          ...state.polynomials,
          [action.payload.type]: action.payload.value
        }
      };
      
    case ActionTypes.SET_OPERATION:
      return {
        ...state,
        currentOperation: action.payload,
        result: null,
        stepByStep: [],
        currentStep: 0
      };
      
    case ActionTypes.SET_RESULT:
      return {
        ...state,
        result: action.payload
      };
      
    case ActionTypes.SET_STEP_BY_STEP:
      return {
        ...state,
        stepByStep: action.payload,
        currentStep: 0
      };
      
    case ActionTypes.SET_CURRENT_STEP:
      return {
        ...state,
        currentStep: action.payload
      };
      
    case ActionTypes.SET_SIDEBAR_VISIBLE:
      return {
        ...state,
        ui: {
          ...state.ui,
          sidebarVisible: action.payload
        }
      };
      
    case ActionTypes.SET_HELP_VISIBLE:
      return {
        ...state,
        ui: {
          ...state.ui,
          helpVisible: action.payload
        }
      };
      
    case ActionTypes.SET_ZOOM:
      return {
        ...state,
        plane: {
          ...state.plane,
          zoom: action.payload
        }
      };
      
    case ActionTypes.SET_PAN:
      return {
        ...state,
        plane: {
          ...state.plane,
          panX: action.payload.x,
          panY: action.payload.y
        }
      };
      
    case ActionTypes.ADD_POLYNOMIAL_CHIP:
      return {
        ...state,
        plane: {
          ...state.plane,
          chips: [...state.plane.chips, action.payload]
        }
      };
      
    case ActionTypes.REMOVE_POLYNOMIAL_CHIP:
      return {
        ...state,
        plane: {
          ...state.plane,
          chips: state.plane.chips.filter(chip => chip.id !== action.payload)
        }
      };
      
    case ActionTypes.CLEAR_PLANE:
      return {
        ...state,
        plane: {
          ...state.plane,
          chips: []
        }
      };
      
    default:
      return state;
  }
}

// Context
const AppContext = createContext();

// Provider
export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);
  
  // Action creators
  const actions = {
    setPolynomial: (type, value) => 
      dispatch({ type: ActionTypes.SET_POLYNOMIAL, payload: { type, value } }),
      
    setOperation: (operation) => 
      dispatch({ type: ActionTypes.SET_OPERATION, payload: operation }),
      
    setResult: (result) => 
      dispatch({ type: ActionTypes.SET_RESULT, payload: result }),
      
    setStepByStep: (steps) => 
      dispatch({ type: ActionTypes.SET_STEP_BY_STEP, payload: steps }),
      
    setCurrentStep: (step) => 
      dispatch({ type: ActionTypes.SET_CURRENT_STEP, payload: step }),
      
    toggleSidebar: () => 
      dispatch({ type: ActionTypes.SET_SIDEBAR_VISIBLE, payload: !state.ui.sidebarVisible }),
      
    setSidebarVisible: (visible) => 
      dispatch({ type: ActionTypes.SET_SIDEBAR_VISIBLE, payload: visible }),
      
    toggleHelp: () => 
      dispatch({ type: ActionTypes.SET_HELP_VISIBLE, payload: !state.ui.helpVisible }),
      
    setZoom: (zoom) => 
      dispatch({ type: ActionTypes.SET_ZOOM, payload: zoom }),
      
    setPan: (x, y) => 
      dispatch({ type: ActionTypes.SET_PAN, payload: { x, y } }),
      
    addChip: (chip) => 
      dispatch({ type: ActionTypes.ADD_POLYNOMIAL_CHIP, payload: chip }),
      
    removeChip: (chipId) => 
      dispatch({ type: ActionTypes.REMOVE_POLYNOMIAL_CHIP, payload: chipId }),
      
    clearPlane: () => 
      dispatch({ type: ActionTypes.CLEAR_PLANE })
  };
  
  return (
    <AppContext.Provider value={{ state, actions }}>
      {children}
    </AppContext.Provider>
  );
}

// Hook personalizado
export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp debe ser usado dentro de AppProvider');
  }
  return context;
}

export default AppContext;
