import { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

const Input = ({ label, ...props }: InputProps) => {
  return (
    <div className="input-group">
      {label && <label>{label}</label>}
      <input {...props} />
    </div>
  );
};

export default Input;
