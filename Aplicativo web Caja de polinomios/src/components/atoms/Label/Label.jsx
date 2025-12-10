import React from 'react';
import './Label.css';

const Label = ({ 
  children, 
  htmlFor, 
  required = false, 
  className = '',
  variant = 'default',
  size = 'medium',
  ...props 
}) => {
  const labelClasses = [
    'label',
    `label--${variant}`,
    `label--${size}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <label 
      htmlFor={htmlFor} 
      className={labelClasses}
      {...props}
    >
      {children}
      {required && (
        <span className="label__required" aria-label="Campo requerido">
          *
        </span>
      )}
    </label>
  );
};

export default Label;
