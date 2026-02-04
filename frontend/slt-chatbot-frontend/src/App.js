import React, { useState } from "react";
import Login from "./components/Login";
import Chatbot from "./components/Chatbot";
import Toast from "./components/Toast";
import './App.css'; 

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = "info") => {
    setToast({ message, type });
 };

  const handleLogin = () => {
    setIsLoggedIn(true);
    showToast("Welcome! You are logged in.", "success");
  };

  const handleLogout = () => {
    console.log("✅ handleLogin triggered!");
    setIsLoggedIn(false);
    showToast("You have been logged out.", "info");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      {isLoggedIn ? (
        <Chatbot onLogout={handleLogout} showToast={showToast} />
      ) : (
        <Login onLogin={handleLogin} showToast={showToast} />
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default App;