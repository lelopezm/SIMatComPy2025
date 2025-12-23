import React from 'react';
import { AppProvider } from './contexts/AppContext';
import MainLayout from './components/templates/MainLayout/MainLayout';
import Home from './components/pages/Home/Home';
import './App.css';

/**
 * Componente principal de la aplicación Caja de Polinomios
 * 
 * Esta aplicación educativa permite a niños y adolescentes
 * aprender sobre operaciones algebraicas de manera visual e interactiva.
 * 
 * Características principales:
 * - Visualización gráfica de polinomios en un plano cartesiano
 * - Interface intuitiva para introducir polinomios
 * - Operaciones algebraicas básicas (suma, resta, multiplicación)
 * - Diseño responsivo y accesible
 * - Retroalimentación visual en tiempo real
 */
function App() {
  return (
    <div className="app">
      <AppProvider>
        <MainLayout>
          <Home />
        </MainLayout>
      </AppProvider>
    </div>
  );
}

export default App;
