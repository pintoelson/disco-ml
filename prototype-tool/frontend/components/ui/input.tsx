import React, { InputHTMLAttributes, forwardRef } from "react";


interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={`fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg w-[90vw] max-w-md ${className}`}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";
