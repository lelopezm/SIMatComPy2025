import React from 'react';
import Navbar from '../../organisms/Navbar/Navbar';
import Sidebar from '../../organisms/Sidebar/Sidebar';
import { useApp } from '../../../contexts/AppContext';
import './MainLayout.css';

const MainLayout = ({ children, className = '' }) => {
  const { state, actions } = useApp();
  const { ui } = state;

  return (
    <div className={`main-layout ${className}`}>
      {/* Navbar fija en la parte superior */}
      <Navbar className="main-layout__navbar" />
      
      {/* Contenedor principal con sidebar y contenido */}
      <div className="main-layout__container">
        {/* Sidebar lateral como overlay */}
        <Sidebar 
          className={`main-layout__sidebar ${
            ui.sidebarVisible ? 'main-layout__sidebar--visible' : ''
          }`} 
        />
        
        {/* Área de contenido principal - siempre ocupa todo el ancho */}
        <main className="main-layout__content">
          {children}
        </main>
      </div>
      
      {/* Overlay para cuando el sidebar está abierto */}
      {ui.sidebarVisible && (
        <div 
          className="main-layout__overlay"
          onClick={() => actions.toggleSidebar()}
        />
      )}
    </div>
  );
};

export default MainLayout;
