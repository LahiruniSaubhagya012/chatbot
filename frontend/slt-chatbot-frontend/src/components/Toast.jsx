import React, { useEffect } from "react";

const Toast = ({ message, type, onClose }) => {
  const baseClasses = "fixed bottom-5 right-5 p-4 rounded-xl shadow-2xl transition-opacity duration-300 z-50 transform translate-y-0";
  let colorClasses = "";

  switch (type) {
    case "success":
      colorClasses = "bg-green-500 text-white";
      break;
    case "error":
       colorClasses = "bg-red-600 text-white";
      break;
    default:
      colorClasses = "bg-gray-800 text-white";
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 4000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`${baseClasses} ${colorClasses} font-semibold`}>
      <div className="flex items-center justify-between">
        <span>{message}</span>
        <button onClick={onClose} className="ml-4 font-bold">
          &times;
        </button>
      </div>
    </div>
  );
};

export default Toast;