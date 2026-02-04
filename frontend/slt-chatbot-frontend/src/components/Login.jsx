import React, { useState } from "react";
import '../styles/Login.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

const Login = ({ onLogin, showToast }) => {
    const initialClientSecret = localStorage.getItem("client_secret") || "";
    const initialPhone = localStorage.getItem("phone_number") || "";

    const [phone, setPhone] = useState(initialPhone);
    const [otp, setOtp] = useState("");
    const [sentOtp, setSentOtp] = useState(initialClientSecret !== "");
    const [loading, setLoading] = useState(false);
    const [clientSecret, setClientSecret] = useState(initialClientSecret); 

    const handleSendOtp = async () => {
        if (!phone) return showToast("Please enter your phone number.", "error");
        if (!/^\+947\d{8}$/.test(phone)) {
            return showToast("Please enter a valid format: +947XXXXXXXX", "error");
        }

        setLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/send-otp`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phone_number: phone }),
            });

            const data = await res.json();

            if (res.ok) {
                showToast("✅ OTP request sent successfully!", "success");

                if (data.result && data.result.client_secret) {
                    const secret = data.result.client_secret;
                    setClientSecret(secret);
                    clientSecret();
                    
                    localStorage.setItem("client_secret", secret);
                    localStorage.setItem("phone_number", phone); 
                    console.log("📦 Stored Client Secret:", secret);
                }
                
                setSentOtp(true); 

            } else {
                showToast("❌ Failed to send OTP: " + (data.detail || "Unknown error"), "error");
            }

        } catch (err) {
            showToast("⚠️ Error connecting to backend. Please check connection.", "error");
        } finally {
            setLoading(false);
        }
    };

   const handleVerifyOtp = () => {
    showToast("OTP verified successfully (demo)", "success");

    alert("✅ Successfully verified!");

    setTimeout(() => {
        onLogin(); 
    }, 1000);
};


    const handleClearState = () => {
        setSentOtp(false);
        setOtp("");
        setClientSecret("");
        localStorage.removeItem("client_secret");
        localStorage.removeItem("phone_number");
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h1 className="login-title">SLT MOBITEL Portal</h1>
                <p className="login-subtitle">Sign in to continue</p>

                <input
                    type="tel"
                    placeholder="+947XXXXXXXX"
                    className="login-input"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    disabled={loading || sentOtp}
                    maxLength={12}
                />

                {sentOtp && (
                    <input
                        type="text"
                        placeholder="Enter OTP"
                        className="login-input"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        disabled={loading}
                    />
                )}

                {!sentOtp ? (
                    <button onClick={handleSendOtp} disabled={loading} className="login-btn blue-btn">
                        {loading ? "Sending..." : "Send OTP"}
                    </button>
                ) : (
                    <button onClick={handleVerifyOtp} disabled={loading} className="login-btn green-btn">
                        {loading ? "Verifying..." : "Verify OTP"}
                    </button>
                )}

                {sentOtp && !loading && (
                    <button
                        onClick={handleClearState}
                        className="login-btn mt-2 secondary-btn"
                    >
                        Change Phone Number
                    </button>
                )}
            </div>
            <p className="login-footer">© 2025 Sri Lanka Telecom</p>
        </div>
    );
};

export default Login;