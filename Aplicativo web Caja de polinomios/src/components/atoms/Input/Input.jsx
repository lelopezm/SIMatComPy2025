import React, { forwardRef } from 'react';
import './Input.css';

const Input = forwardRef(({ 
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  onFocus,
  onBlur,
  disabled = false,
  error,
  helperText,
  className = '',
  variant = 'default',
  size = 'medium',
  icon,
  ...props 
}, ref) => {
  const inputClasses = [
    'input',
    `input--${variant}`,
    `input--${size}`,
    error && 'input--error',
    icon && 'input--with-icon',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label className="input__label">
          {label}
        </label>
      )}
      
      <div className="input__container">
        {icon && (
          <span className="input__icon">
            {icon}
          </span>
        )}
        
        <input
          ref={ref}
          type={type}
          className={inputClasses}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onFocus={onFocus}
          onBlur={onBlur}
          disabled={disabled}
          {...props}
        />
      </div>
      
      {error && (
        <span className="input__error">
          {error}
        </span>
      )}
      
      {helperText && !error && (
        <span className="input__helper">
          {helperText}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';

export default Input;
