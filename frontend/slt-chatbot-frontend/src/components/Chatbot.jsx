import React, { useState, useEffect } from "react";
import '../styles/Chatbot.css';

const BotIcon = () => <span className="text-xl">🤖</span>;
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

const Chatbot = ({ onLogout, showToast }) => {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "👋 Hello! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
 const [isTyping, setIsTyping] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.content }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
         role: "assistant",
          content: data.reply || "⚠️ No response received. Check backend logs." 
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Error connecting to AI service." },
      ]);
      showToast("Chat service connection failed.", "error");
    } finally {
        setIsTyping(false);
    }
  };


  useEffect(() => {
    const main = document.querySelector('.chatbot-main');
    if (main) {
        main.scrollTop = main.scrollHeight;
    }
  }, [messages, isTyping]);


  return (
    <div className="chatbot-wrapper">
      <div className="chatbot-card">
        <header className="chatbot-header">
          <span className="chatbot-title"><BotIcon /> SLT MOBITEL Assistant</span>
          <button onClick={onLogout} className="logout-btn">
            Logout
          </button>
        </header>

        <main className="chatbot-main">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-message ${msg.role === "user" ? "user-msg" : "assistant-msg"}`}
            >
              {msg.content}
            </div>
          ))}
         {isTyping && (
            <div className="chat-message assistant-msg typing-indicator">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
            </div>
          )}
        </main>

       <footer className="chatbot-footer">
          <input
            type="text"
            placeholder="Type your message..."
           value={input}
            onChange={(e) => setInput(e.target.value)}
           onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="chat-input"
            disabled={isTyping}
          />
          <button onClick={handleSend} className="send-btn" disabled={isTyping || !input.trim()}>
            ➤
          </button>
        </footer>
      </div>

      <p className="chatbot-footer-text">© 2025 Sri Lanka Telecom</p>
    </div>
  );
};

export default Chatbot;